# CMake, dependencies, packaging, and delivery

## Contents

- [Model the build with targets](#model-the-build-with-targets)
- [Use reproducible presets](#use-reproducible-presets)
- [Speed up the build](#speed-up-the-build)
- [Manage dependencies deliberately](#manage-dependencies-deliberately)
- [Install and export a library](#install-and-export-a-library)
- [Build across platforms](#build-across-platforms)
- [Release safely](#release-safely)

## Model the build with targets

Write target-based CMake. Create libraries/executables, attach their sources,
usage requirements, compile features, options, and dependencies directly to the
target. Never use directory-wide include directories, definitions, link flags,
or global `CMAKE_CXX_FLAGS` for ordinary project policy.

```cmake
cmake_minimum_required(VERSION 3.24)
project(acme_widget VERSION 1.2.0 LANGUAGES CXX)

add_library(acme_widget src/widget.cpp)
add_library(Acme::widget ALIAS acme_widget)
target_compile_features(acme_widget PUBLIC cxx_std_20)
target_include_directories(acme_widget
  PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
    $<INSTALL_INTERFACE:include>)
target_link_libraries(acme_widget PUBLIC fmt::fmt PRIVATE Threads::Threads)

add_executable(widget_cli apps/widget_cli.cpp)
target_link_libraries(widget_cli PRIVATE Acme::widget)
```

Use `PRIVATE` for an implementation-only dependency, `PUBLIC` only if consumers
must also compile/link against it, and `INTERFACE` for header-only/transitive
requirements. Link imported targets rather than raw library filenames or manual
include paths. Do not glob production source files: explicit lists make changes
and configure-time behavior reliable.

Keep options target-scoped. Separate project warning/sanitizer targets from
third-party code. Use generator expressions for configuration/platform-specific
requirements instead of `if()` branches that rewrite global flags.

Generate `compile_commands.json` for Clang tooling when supported:

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

## Use reproducible presets

Commit `CMakePresets.json` for shared configurations; reserve
`CMakeUserPresets.json` for developer-local paths/secrets/toolchains. Define
hidden base presets and derive ordinary developer/CI presets from them. Use
distinct binary directories per compiler, architecture, sanitizer, and build
type. Avoid changing a configured build directory's toolchain or generator.

```json
{
  "version": 6,
  "configurePresets": [{
    "name": "base", "hidden": true, "generator": "Ninja",
    "binaryDir": "${sourceDir}/build/${presetName}",
    "cacheVariables": {"CMAKE_EXPORT_COMPILE_COMMANDS": "ON"}
  }, {
    "name": "clang-debug", "inherits": "base",
    "cacheVariables": {
      "CMAKE_BUILD_TYPE": "Debug",
      "CMAKE_CXX_COMPILER": "clang++"
    }
  }],
  "buildPresets": [{"name": "clang-debug", "configurePreset": "clang-debug"}],
  "testPresets": [{"name": "clang-debug", "configurePreset": "clang-debug"}]
}
```

Run `cmake --preset <name>`, `cmake --build --preset <name>`, and
`ctest --preset <name>`. Pin the minimum CMake version to capabilities actually
used; do not set it merely to the newest local installation.

## Speed up the build

Adopt build-speed tooling in order of effort-to-impact, and verify each change
still produces the same warnings/behavior before trusting the speedup.

1. Build with Ninja rather than a Make-family generator; it parallelizes and
   tracks dependencies more efficiently.
2. Add a compiler cache so incremental and CI rebuilds reuse prior object
   files:

   ```cmake
   find_program(CCACHE_PROGRAM ccache)
   if(CCACHE_PROGRAM)
     set(CMAKE_C_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
     set(CMAKE_CXX_COMPILER_LAUNCHER "${CCACHE_PROGRAM}")
   endif()
   ```

   Use `sccache` instead where a shared/cloud cache or first-class Windows/MSVC
   support is required. Key CI caches by compiler, flags, and dependency lock
   so a hit stays valid.
3. Add precompiled headers for stable, heavily included headers only:

   ```cmake
   target_precompile_headers(acme_widget PRIVATE
     <vector> <string> "${CMAKE_CURRENT_SOURCE_DIR}/src/pch.hpp")
   ```

   Keep the PCH set small and stable. A header that changes often invalidates
   the cache and makes builds slower, not faster; mismatched compiler flags
   silently disable the PCH.
4. Enable unity builds for CI/clean-build speed once one-definition-rule
   conflicts (anonymous namespaces, `static` globals, macro leakage across
   translation units) are fixed:

   ```cmake
   set_target_properties(acme_widget PROPERTIES
     UNITY_BUILD ON UNITY_BUILD_BATCH_SIZE 8)
   ```

   Keep a non-unity CI job too; unity builds can hide a missing include that a
   normal per-translation-unit build would catch.
5. Switch the link step to `lld` or `mold` for large binaries or frequent
   incremental linking:

   ```cmake
   target_link_options(acme_widget PRIVATE
     $<$<CXX_COMPILER_ID:Clang,GNU>:-fuse-ld=lld>)
   ```

Measure wall-clock clean and incremental build time on the same machine/CI
runner before and after each change; do not stack all of the above blindly and
assume published percentages add up.

## Manage dependencies deliberately

Pick one primary acquisition path per deliverable. Record direct dependencies,
versions/revisions, licenses, supported configurations, and binary/runtime
compatibility. Prefer package-provided CMake config targets with
`find_package(... CONFIG REQUIRED)`.

| Situation | Prefer | Notes |
| --- | --- | --- |
| Cross-platform C++ applications/libraries, internal binary repos | Conan 2 profiles + lockfiles | Use `CMakeToolchain` and `CMakeConfigDeps`/`CMakeDeps`; install before configure. |
| vcpkg ecosystem/Windows integration | vcpkg manifest mode | Commit `vcpkg.json` and baseline/version constraints; set its toolchain in presets. |
| Tiny, tightly controlled build-only dependency | pinned `FetchContent` | Pin immutable revision and hash where applicable; do not silently download in restricted/offline CI. |
| Vendor patch or no package support | vendored source/submodule | Isolate it, preserve provenance/license, and define an update/security process. |
| System/SDK dependency | `find_package`/toolchain | Document system package and supported versions; do not copy flags from a developer machine. |

Use package-manager profiles/triplets for OS, architecture, compiler, standard
library/runtime, build type, and cross-compilation. Never mix artifacts built
with incompatible CRT, compiler, C++ ABI, architecture, or sanitizer settings.
Commit lockfiles/baselines for release and CI reproducibility; update them in
reviewed dependency-refresh changes. Generate an SBOM and run license/
vulnerability review for shipped products where policy requires it.

## Install and export a library

Install targets, public header file sets, and a namespaced export. Generate a
`<Package>Config.cmake` and version file so a consumer can use
`find_package(AcmeWidget CONFIG REQUIRED)` and `Acme::widget`. Do not export
absolute build-machine paths in installed interfaces.

```cmake
include(GNUInstallDirs)
install(TARGETS acme_widget
  EXPORT AcmeWidgetTargets
  FILE_SET HEADERS
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
install(EXPORT AcmeWidgetTargets
  FILE AcmeWidgetTargets.cmake
  NAMESPACE Acme::
  DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/AcmeWidget)
```

Test the installed package in a clean consumer project, not only the build tree.
Use `CMAKE_INSTALL_PREFIX` in a staging location and CPack only after install
rules work. Package runtime dependencies, licenses/notices, configuration
defaults, platform signing/notarization, and upgrade/uninstall behavior as part
of the deliverable.

## Build across platforms

Make host/target/tool distinctions explicit. Cross compilation needs an actual
CMake toolchain file or package-manager profile, a clean target build directory,
and tests executed on the target/emulator/device when possible. Avoid detecting
the host via ad-hoc shell commands in `CMakeLists.txt`.

Test the promised matrix: at least supported operating systems, compilers,
architectures, Debug/Release, shared/static linkage where shipped, and feature
or dependency variants that alter behavior. Keep a fast PR matrix and a broader
nightly/release matrix; cache build artifacts only with keys that include the
compiler, dependency lock/baseline, target architecture, and relevant flags.

## Release safely

Version public API changes according to the project contract. Build from a clean
checkout and locked dependency graph, archive compiler/CMake/package-manager
versions and artifact hashes, verify package installation with a consumer, and
retain test/sanitizer/scan reports. Sign artifacts where the delivery channel
requires it. Never promote a local developer build merely because its tests pass.

## Primary sources

- [CMake user interaction and presets](https://cmake.org/cmake/help/latest/guide/user-interaction/index.html)
- [CMake dependency guide](https://cmake.org/cmake/help/latest/guide/using-dependencies/index.html)
- [CMake package/export guide](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html)
- [Conan 2 CMake integration](https://docs.conan.io/2/integrations/cmake.html)
- [Conan lockfiles](https://docs.conan.io/2/tutorial/versioning/lockfiles.html)
- [vcpkg manifest mode](https://learn.microsoft.com/en-us/vcpkg/consume/manifest-mode)
- [vcpkg versioning](https://learn.microsoft.com/en-us/vcpkg/users/versioning)
- [ccache manual](https://ccache.dev/manual/latest.html)
- [mold linker](https://github.com/rui314/mold)
