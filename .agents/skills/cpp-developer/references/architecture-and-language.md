# Architecture and modern C++

## Contents

- [Choose a project shape](#choose-a-project-shape)
- [Design interfaces and ownership](#design-interfaces-and-ownership)
- [Use modern language features carefully](#use-modern-language-features-carefully)
- [Apply proven idioms deliberately](#apply-proven-idioms-deliberately)
- [Protect public APIs and ABIs](#protect-public-apis-and-abis)
- [Handle errors and boundaries](#handle-errors-and-boundaries)
- [Evolve a large codebase](#evolve-a-large-codebase)

## Choose a project shape

Start with a target-oriented layout; do not expose internal headers by default.

```text
project/
├── CMakeLists.txt                 # project options and top-level targets
├── CMakePresets.json              # versioned, shareable configurations
├── cmake/                         # package/config and toolchain helpers
├── include/acme/widget/           # installed public headers only
├── src/                           # implementation and private headers
├── apps/                          # executable composition roots
├── tests/                         # unit/integration test targets
├── benchmarks/                    # repeatable benchmarks, optional
├── fuzz/                          # fuzz targets/corpora, optional
├── docs/                          # API, architecture, and operations docs
└── packaging/                     # distribution metadata, optional
```

Make each library own a narrow responsibility and a clear dependency direction:

```text
apps -> orchestration -> domain/services -> ports/interfaces -> infrastructure
```

Keep the composition root (`main`, service bootstrap, plugin host) responsible
for constructing concrete dependencies. Depend on small interfaces only where
substitution, test seams, or a real deployment boundary warrants it. Avoid a
universal `IThing` interface or a service locator.

For a monorepo, keep independently buildable packages/targets and their public
headers together. Use a root project only to coordinate common options,
third-party dependency policy, testing, and CI. Do not let sibling targets
include each other's `src/` directories.

## Design interfaces and ownership

Make ownership visible at function and member boundaries.

| Need | Prefer | Avoid |
| --- | --- | --- |
| Return a newly owned object | value; `std::unique_ptr<T>` for polymorphic/optional ownership | caller-managed `new` |
| Borrow a required single object for a call | `T&` or `const T&` | nullable pointer with undocumented precondition |
| Borrow an optional object | `T*` | `shared_ptr<T>` solely to say “maybe null” |
| Read a contiguous sequence | `std::span<const T>` | `(T*, size)` pairs |
| Read text without ownership | `std::string_view` for synchronous/non-retained use | storing views with unclear backing lifetime |
| Share object lifetime | `std::shared_ptr<T>` plus a documented ownership graph | a reference-counted default |
| Break a deliberate shared cycle | `std::weak_ptr<T>` | raw pointer with no lifetime proof |

Keep resource lifetime local: acquire in a constructor/factory, release in a
destructor, make the wrapper non-copyable or value-like as appropriate, and
preserve class invariants if construction fails. Prefer the rule of zero. For a
resource-owning type, explicitly choose copy/move/destructor semantics rather
than relying on accidental defaults.

Pass small trivially copyable values by value. Pass a large immutable input by
`const&` only when its lifetime need not cross the call; use a view when the
API means “a sequence,” not “this particular container.” Do not pass
`shared_ptr` by value unless the callee shares ownership.

## Use modern language features carefully

- Prefer `enum class`, `std::optional`, `std::variant`, `std::span`, standard
  algorithms/ranges, and `<chrono>` types over ad-hoc flags, sentinel values,
  pointer-and-length pairs, loops that obscure intent, and raw duration units.
- Use `auto` when the initializer makes the type obvious or retaining the exact
  spelling couples code to an implementation detail. Spell the type when it
  communicates a domain invariant or prevents accidental narrowing.
- Mark a function `noexcept` only if it cannot propagate. An incorrect
  `noexcept` converts a throw into termination; it is not a performance charm.
- Use `[[nodiscard]]` on fallible results, handles, and values whose omission is
  almost certainly a defect. Do not create warning noise for benign queries.
- Use concepts to state semantic requirements on public templates. Keep
  constraints minimal and meaningful; concepts improve diagnostics but do not
  validate an algorithm's runtime contract.
- Prefer `constexpr` for genuinely compile-time-capable pure logic, not to force
  a compile-time implementation onto I/O, dynamic resources, or confusing APIs.
- Use coroutines only with an explicit ownership, cancellation, scheduler, and
  destruction model. Never allow a coroutine to reference stack data that may
  expire before resumption.
- Introduce C++ modules only where the chosen compiler, build generator, IDE,
  package model, and consumers support them. Keep conventional headers at
  package boundaries until the delivery matrix proves module interoperability.

## Apply proven idioms deliberately

Reach for a named idiom only when the ownership/dispatch problem actually
requires it. A plain virtual interface or a `std::variant` beats a clever
idiom on both readability and compile time for most cases.

| Idiom | Solves | Prefer when | Avoid when |
| --- | --- | --- | --- |
| PImpl | ABI stability, reduced recompilation, hiding private members from headers | a public library header must not leak private types/includes | the extra indirection/allocation is measurable and the type is internal-only |
| Type erasure (`std::function`-style wrapper) | heterogeneous callable/value storage without a class hierarchy | a public API needs value semantics over "anything with this shape" | a closed, small set of concrete types already fits `std::variant` or an interface |
| `std::variant` + `std::visit` (visitor) | closed-set polymorphism, exhaustive dispatch | the set of alternatives is fixed and known at the boundary | the set grows across a plugin/ABI boundary (use a virtual interface instead) |
| CRTP / static polymorphism | compile-time dispatch, mixins (for example `enable_shared_from_this`), avoiding vtable cost | the concrete type set is known at compile time and the call is hot | runtime dispatch flexibility is actually needed, or template error noise outweighs the win |
| Policy-based design | configuring one algorithm's behavior (allocation, locking, comparison) via template parameters | the STL already models this shape (compare `std::vector`'s allocator) and callers are template-friendly | it turns into an unreadable combinatorial explosion of parameters for two call sites |
| Builder | multi-step, validated construction with many optional parameters | the constructor parameter list is unreadable or requires staged validation | a designated-initializer-friendly aggregate or a few named factory functions suffice |

Prefer a virtual interface as the default extensibility mechanism at a
plugin/ABI boundary. Reserve compile-time idioms (CRTP, policy classes, heavy
template metaprogramming) for internal, performance-critical code where the
instantiation set is closed and the compile-time cost is acceptable.

## Protect public APIs and ABIs

Treat installed headers, exported symbols, data layout, exception behavior,
allocator ownership, compiler/runtime choice, and standard-library ABI as part
of a binary-library contract. A source-compatible edit can still break ABI.

- Version source and binary compatibility separately. State supported compilers,
  runtime linkage, language level, platforms, and exception/RTTI policy.
- Export only intentional symbols. Hide implementation symbols with target-level
  visibility settings; do not make all symbols public by convenience.
- Avoid exposing mutable data members, concrete standard-library containers,
  template-heavy internals, compiler-specific types, and ownership of a
  cross-DLL allocation in a stable ABI when compatibility matters.
- Use PImpl selectively to stabilize layout or reduce recompilation; measure the
  allocation/indirection cost and retain value semantics deliberately.
- Keep exceptions from crossing C, plugin, RPC, callback, or mixed-toolchain
  boundaries. Translate at the boundary and document ownership of buffers and
  destruction functions.
- Add compatibility tests, symbol/API diff checks, and consumer examples before
  releasing a public library. Generate a relocatable CMake package; consumers
  should link `Acme::widget`, not copied include/link flags.

## Handle errors and boundaries

Choose the error model per boundary, then use it consistently inside that layer.

| Situation | Typical model | Rule |
| --- | --- | --- |
| Constructor cannot establish invariant; exceptional failure | exception or named factory result | never leave a half-valid object |
| Expected operational failure | `std::expected<T, E>` / status result | make callers handle or propagate it |
| C/OS/library boundary | error code/status translation | preserve category/context and cleanup |
| Contract violation/programmer error | assertion/termination policy | do not disguise it as recoverable I/O |
| Concurrent cancellation/shutdown | explicit cancellation result/state | make ownership and joining deterministic |

Add useful context at a translation boundary, not repeatedly at every frame.
Avoid catch-all handlers that hide defects. Preserve error category/code for
operators and tests; do not parse error strings.

## Evolve a large codebase

Map targets, public headers, ownership edges, global state, generated code, and
runtime processes before large refactors. Work in reversible slices:

1. Add characterization tests and establish build/test/sanitizer baselines.
2. Define the destination module/API and an adapter seam.
3. Move one dependency direction or call path at a time; retain compatibility
   shims with removal criteria and telemetry/usage evidence.
4. Delete dead paths only after consumers migrate and all supported configurations
   verify. Do not run two semantic implementations indefinitely.

Use dependency injection at process boundaries, deterministic clocks/executors
for tests, and structured shutdown ownership. Isolate global state behind a
small boundary; document initialization order, thread affinity, and teardown.

## Primary sources

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines)
- [CppReference: standard library](https://en.cppreference.com/w/cpp/header)
- [CMake buildsystem manual](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)
- [More C++ Idioms (Wikibooks)](https://en.wikibooks.org/wiki/More_C%2B%2B_Idioms)
