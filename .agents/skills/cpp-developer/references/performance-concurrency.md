# Data structures, performance, and concurrency

## Contents

- [Choose data structures from access patterns](#choose-data-structures-from-access-patterns)
- [Optimize by measurement](#optimize-by-measurement)
- [Control memory and data layout](#control-memory-and-data-layout)
- [Design concurrency for ownership and shutdown](#design-concurrency-for-ownership-and-shutdown)
- [Use atomics and locks correctly](#use-atomics-and-locks-correctly)

## Choose data structures from access patterns

Select a representation after stating data size, lookup/update/iteration ratio,
ordering, invalidation rules, allocation budget, locality, and concurrency
model. Big-O alone does not decide a machine-level workload.

| Workload | Default candidate | Reconsider when |
| --- | --- | --- |
| append and scan, fixed-ish elements | `std::vector<T>` | stable addresses/iterator validity or mid-sequence insertion dominates |
| FIFO/LIFO adaptation | `std::deque`, `std::queue`, `std::stack` | profiling shows a custom ring buffer is needed |
| ordered lookup/range queries | sorted `vector` for read-mostly; `std::map` for frequent ordered mutation | key count, mutation rate, and cache behavior differ |
| key lookup | `std::unordered_map` | adversarial keys, deterministic order, memory pressure, or small N matters |
| dense boolean flags | `std::vector<bool>` only after accepting its proxy semantics; otherwise bytes/bitset | atomic/element-address needs exist |
| heterogeneous alternatives | `std::variant` | extensibility or ABI/plugin boundary requires type erasure |
| polymorphism in a hot loop | contiguous tagged data/`variant` where suitable | flexibility outweighs dispatch/locality cost |

Reserve capacity when cardinality is known. Prefer contiguous storage and batch
work where it improves locality. Establish iterator/reference invalidation
contracts; do not retain pointers into a container across modifications that may
invalidate them. For `unordered_*`, reserve/adjust load factor and validate
inputs if untrusted keys can cause collision attacks.

## Optimize by measurement

Start with a user-visible budget: latency percentile, throughput, memory,
startup, binary size, energy, or build time. Form a falsifiable hypothesis and
collect a baseline under a representative optimized configuration, data set,
CPU affinity/load, and compiler flags.

1. Verify algorithmic complexity, unnecessary work, I/O, contention, and memory
   allocation before micro-optimizing instructions.
2. Profile with platform tools (for example perf, Instruments, Visual Studio
   Profiler, or a sampling profiler) and inspect call stacks, allocations,
   cache misses, syscalls, and lock waits. Distinguish wall time from CPU time.
3. Change one cause at a time. Benchmark enough iterations to expose variance,
   warm-up effects, cache state, and allocator behavior; compare distributions,
   not a single fastest run.
4. Re-profile, validate all behavior, and retain the benchmark/regression test if
   the performance defect mattered. Report configuration, data, metrics, and
   trade-offs honestly.

Do not presume that `inline`, `constexpr`, `std::move`, `reserve`, a custom
allocator, a lock-free queue, or SIMD is faster. Inspect generated code or
profile evidence only after the algorithm and data layout are credible.

## Control memory and data layout

- Minimize allocation count and ownership complexity before introducing pools.
  Use `std::pmr` only when an allocation domain, resource lifetime, and failure
  behavior are explicit; ensure objects do not outlive their memory resource.
- Keep hot data compact and contiguous. Split hot/cold fields, use structure of
  arrays for vectorized column-like operations when profiling supports it, and
  avoid false sharing between frequently written thread-local counters.
- Move cheaply movable resources; do not add `std::move` to a `const` object or
  return expression where it defeats NRVO. Design value types with correct move
  semantics rather than forcing moves at every call site.
- Use SIMD through a portable, tested abstraction or compiler-supported path
  only after scalar correctness and profiling. Provide CPU feature dispatch and
  a correct fallback; verify alignment, tails, overflow, FP semantics, and
  determinism requirements.
- Separate release profiling from debug/sanitizer observations. Optimizers alter
  layout, inlining, and timings; sanitizer overhead can invert bottlenecks.

## Design concurrency for ownership and shutdown

Prefer eliminating shared mutable state: partition data by owner, pass immutable
messages, batch work, or use an actor/queue boundary. Choose a concurrency model
before adding threads: CPU-bound parallel work, I/O waiting, single-threaded
event loop, or a producer/consumer pipeline have different cancellation and
backpressure needs.

Every concurrent component must document:

- who starts it and who owns/join-stops it;
- which thread/executor may access or mutate each field;
- synchronization that protects each shared invariant;
- queue capacity, backpressure/drop policy, ordering, cancellation, and failure;
- shutdown ordering, timeout/escalation policy, and behavior of in-flight work.

Use `std::jthread` and `std::stop_token` where their cooperative cancellation
model fits. Never detach threads as a way to avoid lifetime design. Join before
destroying data used by worker tasks; prevent callbacks from using a destroyed
owner. Bound executors/queues and handle overload deliberately rather than
creating unbounded threads/tasks/buffers.

## Use atomics and locks correctly

Use a mutex when protecting a multi-field invariant, complex state transition,
or nontrivial container. A lock is often clearer and faster enough than a
lock-free alternative. Guard a mutex with RAII (`std::scoped_lock`,
`std::lock_guard`, `std::unique_lock`); establish and document a global lock
order when operations acquire more than one lock.

Use condition variables with a predicate loop; allow spurious wakeups and define
what shutdown does to waiters. Do not call user code while holding an internal
lock unless re-entrancy and latency are intentional.

Use atomics only for a precisely stated atomic invariant. Begin with sequential
consistency unless a proven data-flow argument needs weaker ordering. Document
the release/acquire relationship and the object lifetime it publishes. Atomics
do not make compound operations, containers, or lifetime safe. Avoid premature
lock-free structures: they introduce ABA, reclamation, fairness, and diagnostic
complexity. Validate with stress tests, TSan, and performance measurement.

## Primary sources

- [C++ Core Guidelines: concurrency and performance](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#S-concurrency)
- [C++ standard library concurrency support](https://en.cppreference.com/w/cpp/thread)
- [Clang Thread Safety Analysis](https://clang.llvm.org/docs/ThreadSafetyAnalysis.html)
- [ThreadSanitizer](https://clang.llvm.org/docs/ThreadSanitizer.html)
