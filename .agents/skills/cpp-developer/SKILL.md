---
name: cpp-developer
description: Build, review, refactor, debug, test, profile, secure, package, document, or architect production C++ applications and libraries. Use for modern C++ (C++17/20/23), CMake, Conan, vcpkg, CLion, compiler and linker issues, public APIs/ABIs, RAII and memory safety, templates and concepts, data structures, multithreading, sanitizers, static analysis, benchmarking, build-speed tuning (ccache/PCH/unity/mold), Doxygen documentation, structured logging/OpenTelemetry instrumentation, git workflow and code review, CI, cross-platform delivery, and large or performance-sensitive C++ codebases.
---

# C++ Developer

Use this skill as a router for production C++ work. Preserve the repository's
documented toolchain, coding rules, supported platforms, and C++ language
level; do not replace them with generic defaults. Treat C++20 as a reasonable
baseline only for a new project with no stated compatibility constraint. Adopt
C++23/26 features only after verifying the required compilers, standard
library, and target platforms support them.

## Start every task deliberately

1. Read repository instructions and inspect `CMakePresets.json`,
   `CMakeLists.txt`, package manifests/lockfiles, CI, and existing tests before
   changing code.
2. Establish the target(s), compiler versions, language standard, build preset,
   dependency manager, platform/architecture, and success criteria. Preserve
   ABI/API compatibility where the project promises it.
3. For a bug, obtain a minimal reproducer, failing test, sanitizer trace, or
   profiler sample first. For an optimization, record a representative baseline
   and a measurable budget before proposing a change.
4. Change the narrowest coherent ownership/API boundary. Update the CMake target
   model and tests with the implementation; do not leave build configuration as
   an afterthought.
5. Run the project's prescribed checks. At minimum, build and test the affected
   preset; add static analysis and relevant sanitizers for new or changed C++.
   Report exact commands run, configuration, and any checks not run.

## Reference router

Read only the reference(s) that govern the current work. Combine them when a
task crosses concerns, such as a concurrent public library (architecture,
quality, and performance).

| Task | Read |
| --- | --- |
| Design a component, modernize C++, choose an idiom (PImpl/type erasure/CRTP/policy-based), set ownership/errors, define a public API/ABI, or organize a large codebase | `references/architecture-and-language.md` |
| Add targets, configure CMake, speed up builds (ccache/PCH/unity/lld/mold), choose Conan/vcpkg, export/install a library, cross-compile, or package/release | `references/build-dependencies-packaging.md` |
| Configure warnings, formatting, static/dynamic analysis, tests, fuzzing, code review, or CI security | `references/quality-testing-security.md` |
| Select containers, eliminate a hot path, manage allocation/cache/SIMD, or design/diagnose concurrency | `references/performance-concurrency.md` |
| Configure or troubleshoot CLion profiles, toolchains, CMake Presets, tests, debugger, clang-tidy, or sanitizers | `references/clion-workflow.md` |
| Document a public API (Doxygen), add structured logging/tracing, or set up git workflow and code-review process | `references/documentation-observability-workflow.md` |

## Non-negotiable engineering defaults

- Model ownership and lifetime in types. Use values and RAII first; express
  exclusive ownership with `std::unique_ptr`, shared lifetime only when it is
  genuinely shared, and non-owning nullable links with raw pointers/references
  where their lifetime contract is obvious. Never use `new`/`delete` in ordinary
  application logic.
- Follow the rule of zero. If a type owns a non-standard resource, implement the
  complete special-member policy deliberately, make moves `noexcept` when
  correct, and test failure paths. Do not hand-roll a resource wrapper when a
  standard one exists.
- Make interfaces precise: pass read-only contiguous sequences as
  `std::span<const T>` where appropriate; use `std::string_view` only when the
  caller's storage demonstrably outlives use; do not return views/references to
  temporaries or unstable container elements.
- Prefer simple, explicit code over clever template machinery. Constrain public
  templates with concepts where available; provide readable diagnostics and a
  non-template overload or type-erased seam where compile time or ABI demands
  it.
- Use `const`, `constexpr`, `noexcept`, `[[nodiscard]]`, scoped enums, and
  standard algorithms when their contracts are true. Do not add annotations just
  to look modern.
- Keep a single consistent error model at each boundary. Translate exceptions,
  error codes, `std::expected`, or status objects at process/plugin/FFI/API
  boundaries; never let exceptions cross an ABI boundary unless that ABI
  explicitly guarantees it.
- Keep headers self-sufficient, minimal, and namespace-qualified. Avoid
  `using namespace` in headers, cyclic includes, hidden globals, and macros in
  public interfaces. Prefer forward declarations only when they preserve the
  real ownership and completeness requirements.
- Treat warnings as defects in changed code. Enable a maintainable warning set
  per compiler, and do not globally suppress diagnostics or mark every warning
  as an error without addressing third-party/generated code separately.
- Treat undefined behavior, races, dangling views, unchecked integer/bounds
  conversions, and unvalidated external input as correctness and security bugs.
  Use sanitizers and static analysis to expose them; do not merely silence them.

## Delivery expectations

For an implementation, deliver the smallest complete change: affected public
headers and sources, target-local CMake updates, focused tests, and any required
docs or migration notes. Explain ownership, error/concurrency behavior, and
observable API/ABI impact when they are non-obvious.

For a review, distinguish blocking correctness/safety/compatibility findings
from improvements. Give each finding a file and location, a concrete failure
mode, and a safe remediation. Do not claim performance gains without a measured
representative workload.

For a new library or application, create targets rather than a directory of
globally configured sources. Start with a small layered layout, reproducible
presets/dependencies, unit and integration tests, and a CI matrix matching the
promised compiler/platform support. Expand architecture only when a real module
or deployment boundary requires it.

## Verification ladder

Run the cheapest relevant checks first, then broaden until risk is covered:

1. Format and compile the affected target with warnings.
2. Run focused unit/integration tests through CTest or the project's runner.
3. Run `clang-tidy`/compiler static analysis against the compilation database.
4. Run AddressSanitizer + UndefinedBehaviorSanitizer for memory/UB-sensitive
   code. Run ThreadSanitizer in a separate build for concurrent code; do not
   combine incompatible sanitizer configurations.
5. Add fuzz/property tests for parsers, protocol decoders, and complex state
   machines. Exercise error, cancellation, shutdown, and allocation-failure
   paths.
6. Profile and benchmark only with an optimized configuration and realistic
   data/load; retain a regression test or benchmark for a fixed performance bug.

## Sources and adaptation

The references synthesize the C++ Core Guidelines, CMake, Clang/LLVM, Conan,
vcpkg, GoogleTest, JetBrains, Doxygen, spdlog, OpenTelemetry, and pre-commit
documentation, plus the supplied C++ Pro material. Follow upstream
documentation linked in each reference for version-sensitive commands. If a
project deliberately differs, document the conflict and follow the project
unless the difference creates a correctness or security risk.
