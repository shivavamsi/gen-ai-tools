# CLion workflow

## Make the IDE reflect the real build

* Open the project root that contains the CMake model, presets, and dependency manifests. Treat CLion as a client of the build configuration, never as a second source of truth.
* Commit shareable configuration in `CMakePresets.json`, CMake, toolchain files, and dependency profiles/manifests. Keep local paths, credentials, and experiments in `CMakeUserPresets.json` or local IDE settings.
* Configure a toolchain that matches CI/production: compiler, CMake, builder, debugger, and environment. Verify the compiler and CMake command in CMake output instead of trusting a UI label.
* Restore dependencies before configuration according to the project workflow. Set `CMAKE_TOOLCHAIN_FILE` from the project preset; never hard-code a developer cache path in `CMakeLists.txt`.

## Use profiles and presets safely

* Use CMake profiles to bind an IDE toolchain, generator, build type, environment, and CMake options. Use CMake presets to share configuration independent of IDE debugger choices.
* Prefer importing repository presets. CLion supports a limited CMake Presets schema/version range and selected preset kinds, so check the installed CLion version if a recent preset is ignored.
* Keep distinct configurations and binary directories for Debug, RelWithDebInfo, Release, ASan/UBSan, TSan, compiler, architecture, and dependency variants. Never point Debug and Release (or incompatible toolchains) at the same build directory.
* Reset/reconfigure CMake after changing compiler, generator, toolchain file, build type, or package-manager configuration. Do not use `CMAKE_BUILD_TYPE` as a global controller for multi-config generators.

| Purpose | Build type/tooling | Use |
| --- | --- | --- |
| Debug | Debug, symbols, assertions | stepping, unit tests, diagnosis |
| Production diagnosis | RelWithDebInfo/optimized symbols | representative profiles and crashes |
| Release candidate | exact release flags | packaging and acceptance checks |
| Memory/UB analysis | separate Clang/GCC sanitizer build | ASan/UBSan tests and repros |
| Race analysis | separate ThreadSanitizer build | stress and concurrent integration tests |

## Run, test, and debug

* Create configurations that launch the actual CMake-produced target. Set deterministic working directories, input fixtures, and non-secret environment variables.
* Use dedicated GoogleTest, Catch2, doctest, or CTest configurations where available, but keep every check runnable in a terminal/CI. The project's `ctest --preset ...` or stated test command remains authoritative.
* Build symbols, reproduce with the smallest input, then inspect call stacks, threads, locals, disassembly, and memory as needed. Capture toolchain, preset, arguments, environment, and a symbolized trace for native crashes.
* Use breakpoints cautiously in concurrent code. For deadlocks, capture all threads and their held/waited locks, then compare them against the documented lock order and shutdown state.

## Use inspections and dynamic analysis

* Enable the repository `.clang-format` and `.clang-tidy`; use IDE quick-fixes as suggestions and review their diff. Run the same configured formatter/linter outside the IDE before accepting a change.
* Keep sanitizer, Valgrind, profiler, and coverage instrumentation in targets or presets so results reproduce outside CLion. Compile and link sanitizer flags consistently; run TSan separately from ASan/UBSan.
* Generate a compilation database for aligned CLI and IDE tooling:

```cmake
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)
```

* If code insight disagrees with the compiler, inspect active-profile CMake output and `compile_commands.json` before invalidating IDE caches.

## Work remotely without changing semantics

* Choose WSL, Docker, a remote toolchain, or Gateway based on where sources, build tools, and the target binary must run. Build against the real target toolchain and debugger, not host headers that happen to parse.
* Record image/remote compiler, CMake, package-manager, and dependency-lock versions. Confirm source/path mappings, generated headers, debug symbols, runtime libraries, and architecture.
* For embedded or separate target devices, validate deploy/run/debug separately from cross compilation. A successful host or container build is not target validation.

## Diagnose common failures

| Symptom | Check first | Safe response |
| --- | --- | --- |
| Reload fails | first CMake error, profile, dependency restore | fix root config; reset only the affected cache if invalid |
| Headers/index wrong | active profile, compile database, generated headers | correct target usage requirements, then reload |
| Link only fails in one profile | target visibility, ABI/runtime, triplet/profile | fix target dependencies; do not add global link flags |
| Sanitizer lacks symbols/runtime | compiler and compile/link flags, symbolizer path | use a dedicated compatible preset/toolchain |
| Debug opens wrong binary | CMake target, working directory, mappings | recreate config against the actual target |
| Remote differs from CI | compiler/CMake/lock/environment/arch | reproduce CI preset/container instead of source hacks |

## Primary sources

* [CLion CMake profiles](https://www.jetbrains.com/help/clion/cmake-profile.html)
* [CLion CMake presets](https://www.jetbrains.com/help/clion/cmake-presets.html)
* [CLion toolchains](https://www.jetbrains.com/help/clion/how-to-create-toolchain-in-clion.html)
* [CLion CTest support](https://www.jetbrains.com/help/clion/ctest-support.html)
* [CLion clang-tidy integration](https://www.jetbrains.com/help/clion/clang-tidy-checks-support.html)
* [CLion remote development](https://www.jetbrains.com/help/clion/remote-development.html)
