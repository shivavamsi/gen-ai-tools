# Quality, testing, diagnostics, and security

## Contents

- [Set enforceable standards](#set-enforceable-standards)
- [Use layered analysis](#use-layered-analysis)
- [Test behavior and failure modes](#test-behavior-and-failure-modes)
- [Harden inputs and delivery](#harden-inputs-and-delivery)
- [Review C++ changes](#review-c-changes)

## Set enforceable standards

Adopt a documented style, formatter version, naming convention, supported
language level, error policy, and API/ABI policy. Store formatter and linter
configuration at the repository root (`.clang-format`, `.clang-tidy`) and run
them in CI. Do not ask reviewers to enforce formatting manually.

Compile every owned target with a maintainable warning set. Start from a clean
baseline, distinguish first-party from third-party/generated sources, and fix
or locally justify warnings instead of globally disabling categories.

| Toolchain | Sensible starting policy | Do not assume |
| --- | --- | --- |
| Clang/GCC | `-Wall -Wextra -Wpedantic`, then selectively add conversion, shadow, format, virtual-dtor, and implicit-fallthrough diagnostics | identical warning names/behavior across Clang and GCC |
| MSVC | `/W4` and modern conformance options appropriate to the project | `/Wall` is a low-noise default |
| All | keep CI diagnostics visible; promote reviewed, actionable warnings to errors incrementally | third-party warnings should break the project |

Place compiler-specific flags in CMake generator expressions or a dedicated
interface target. Keep warning policy independent from optimization, sanitizer,
and production-release flags. Enable `CMAKE_EXPORT_COMPILE_COMMANDS` for Clang
tooling when supported.

## Use layered analysis

Run complementary checks; no one tool proves C++ code correct.

1. Format changed code with `clang-format`; preserve intentional generated or
   external code boundaries.
2. Build all affected configurations with compiler warnings.
3. Run `clang-tidy` using the project's `compile_commands.json`. Start with
   compiler/static-analyzer, bug-prone, performance, readability, and selected
   modernize checks; adopt guideline check sets gradually and configure known
   exceptions narrowly. Review automated fixes before applying them.
4. Run compiler-specific analysis where material: Clang Static Analyzer,
   MSVC `/analyze`, and optional `cppcheck` can find different defects.
5. Run sanitizers in separate, compatible configurations. Fix a reproducible
   sanitizer report or justify a tested suppression with a linked upstream bug.

Use a target-local option so compile and link flags match. Enable it only in a
dedicated Clang/GCC debug preset; do not apply sanitizers to every build:

```cmake
target_compile_options(my_target PRIVATE
  $<$<CXX_COMPILER_ID:Clang,GNU>:-Wall;-Wextra;-Wpedantic>)

option(ACME_ENABLE_SANITIZERS "Enable ASan and UBSan" OFF)
if(ACME_ENABLE_SANITIZERS AND CMAKE_CXX_COMPILER_ID MATCHES "Clang|GNU")
  target_compile_options(my_target PRIVATE
    -fsanitize=address,undefined -fno-omit-frame-pointer -g)
  target_link_options(my_target PRIVATE -fsanitize=address,undefined)
endif()
```

| Check | Use for | Important rule |
| --- | --- | --- |
| ASan | out-of-bounds, use-after-free/return, double free | compile *and* link instrumented code; exercise the path |
| UBSan | invalid shifts, overflow categories, alignment, vptr, other UB | enable a deliberate set; some UB needs additional flags |
| TSan | data races and synchronization misuse | use a separate build; test realistic parallel scheduling |
| LSan | leaks on supported platforms | distinguish intentional process-lifetime caches from leaks |
| MSan | uninitialized reads | use only with a compatible, instrumented runtime/dependencies |

Sanitizers are test amplifiers, not release proof. Build sanitizer dependencies
compatibly where needed, symbolize reports, preserve the reproducer, and rerun
the failing test after the fix.

Use Clang thread-safety annotations plus `-Wthread-safety` in synchronization-
heavy code where its conventions can be adopted. They make lock requirements
reviewable at compile time; still validate dynamic behavior with TSan/tests.

## Test behavior and failure modes

Make tests deterministic, isolated, and behavior-oriented. Test a public API's
observable contract, not private implementation details. Use CTest as the
uniform runner and keep tests as normal CMake targets.

```cmake
include(CTest)
if(BUILD_TESTING)
  find_package(GTest CONFIG REQUIRED)
  add_executable(widget_tests tests/widget_test.cpp)
  target_link_libraries(widget_tests PRIVATE Acme::widget GTest::gtest_main)
  include(GoogleTest)
  gtest_discover_tests(widget_tests)
endif()
```

- Write fast unit tests for invariants and edge cases; add integration tests for
  filesystem, network, database, process, plugin, and ABI boundaries.
- Inject clocks, random sources, executors, I/O, and environment dependencies so
  tests do not race wall time or share mutable global state.
- Cover invalid input, errors, cancellation, retry, shutdown, boundary sizes,
  integer limits, allocation failure when relevant, and move/copy behavior of
  resource types.
- Add regression tests for every fixed defect that can be reproduced cheaply.
  Avoid brittle tests that assert exact log formatting, allocation counts, or
  internal call sequences unless that is the contract.
- Use property-based tests or fuzzing for parsers, serializers, protocol frames,
  file decoders, allocators, and state machines. Define a small oracle/property,
  seed corpus, size/time limits, and a way to promote findings to regressions.
- Treat coverage as a gap-finding signal, not a quality score. Target untested
  error branches and high-risk state transitions rather than maximizing a number.

## Harden inputs and delivery

Assume every byte, length, identifier, configuration value, file path, network
response, and deserialized field is untrusted until validated at its boundary.

- Validate size/range before allocation, multiplication, narrowing conversion,
  indexing, pointer arithmetic, and cast. Define behavior for overflow rather
  than relying on signed overflow or implementation quirks.
- Parse into bounded types; reject malformed/ambiguous encodings. Prevent path
  traversal, command injection, unsafe temporary-file use, and TOCTOU issues.
- Do not write cryptography, authentication, random-number generation, or
  protocol framing from scratch. Use maintained libraries and current platform
  APIs; keep secrets out of source, logs, and crash reports.
- Pin/review dependencies, track licenses and known vulnerabilities, verify
  provenance/checksums, and produce an SBOM when policy or distribution warrants
  it. Separate build credentials from produced artifacts.
- Fuzz boundary parsers and run sanitizers in CI. Define a disclosure/patch path
  for security findings and preserve a minimal testcase privately when needed.

## Review C++ changes

Review in this order: behavior and compatibility; lifetime/ownership and error
paths; thread safety; input/overflow/UB; build/dependency impact; tests; then
performance and style. Check the diff *and* its target configuration.

Block a change when it introduces a leak, dangling reference/view, data race,
unchecked external input, UB, broken API/ABI contract, missing synchronization/
shutdown ownership, incompatible build configuration, or a testless regression
that is readily testable. State the concrete execution path and a minimal safe
fix. Do not over-index on stylistic preferences already enforced by tooling.

## Primary sources

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [Clang-Tidy documentation](https://clang.llvm.org/extra/clang-tidy/index.html)
- [AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html) and [UndefinedBehaviorSanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html)
- [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html) and [Clang thread-safety analysis](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html)
- [GoogleTest CMake quickstart](https://google.github.io/googletest/quickstart-cmake.html)
- [OpenSSF Best Practices](https://www.bestpractices.dev/en)
