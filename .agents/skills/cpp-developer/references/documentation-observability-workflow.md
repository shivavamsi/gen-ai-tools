# Documentation, observability, and workflow

## Contents

- [Document public APIs](#document-public-apis)
- [Instrument for observability](#instrument-for-observability)
- [Establish git workflow and review discipline](#establish-git-workflow-and-review-discipline)

## Document public APIs

Document the public interface in headers; keep implementation comments in
`src/` explaining *why*, not restating *what* the code already says. Pick one
Doxygen comment style per repository (Javadoc-style `/** */` is the common
default) and enforce it in review, not just at adoption time.

```cpp
/**
 * @brief Parses a widget descriptor from a validated byte buffer.
 *
 * @param bytes Contiguous, validated descriptor bytes; must outlive the call.
 * @param opts  Parsing options; see WidgetParseOptions for defaults.
 * @return Parsed widget on success.
 * @throws WidgetParseError if the buffer is malformed.
 */
[[nodiscard]] std::expected<Widget, WidgetParseError>
parse_widget(std::span<const std::byte> bytes, const WidgetParseOptions& opts);
```

- Document ownership, lifetime requirements, thread-safety, and failure modes
  on every public function; these are the parts callers get wrong, not the
  algorithm.
- Skip a doc comment where the signature is already unambiguous (a trivial
  getter). Do not pad every declaration with a comment that restates its name.
- Generate docs from the same headers CI compiles against, so drift shows up
  as a stale-docs review comment, not a separate task:

  ```cmake
  find_package(Doxygen)
  if(DOXYGEN_FOUND)
    doxygen_add_docs(docs include/ src/ ALL)
  endif()
  ```

- Keep a top-level `docs/architecture.md` and a per-module `README.md` for
  ownership boundaries, invariants, and rationale that Doxygen cannot express
  (why a module exists, deployment topology, deprecation plans). Doxygen
  documents the API surface; it does not replace architecture docs.

## Instrument for observability

Choose a structured logging library deliberately; do not thread `printf`/
`std::cout` through production code. Log structured fields (event, ids,
duration), not formatted prose, so downstream tooling can filter and
aggregate.

| Library | Prefer when | Note |
| --- | --- | --- |
| spdlog | new projects, header-only or compiled, need speed and pattern-based sinks | uses `libfmt`-style formatting; call `set_level` explicitly, the default is `info` |
| glog | need built-in crash/signal handling (SIGSEGV, SIGABRT, ...) alongside logging | still C++14-oriented; heavier footprint |
| Boost.Log | already depend on Boost; need fine-grained filtering/sinks | eager-evaluates disabled log statements unless guarded; do not put an expensive expression directly in a log call without a level check |

- Log at the boundary that has context (request/task start), not deep inside
  helpers that don't know the caller's intent. Attach a correlation/request id
  and propagate it explicitly through async/thread-pool boundaries; it is not
  free.
- Never log secrets, tokens, PII, or full request/response bodies by default.
  Treat log output as an external boundary for injection (CRLF/format-string
  injection) whenever it includes untrusted data.
- Use asynchronous logging (spdlog's `async_factory`, or an equivalent queue)
  on a hot path so a slow sink cannot block application threads; bound the
  queue and choose an overflow policy (block vs. drop-oldest) deliberately.
- For services, add tracing/metrics via OpenTelemetry C++ (traces, metrics,
  and logs are all stable there) instead of a bespoke wire format: create one
  `TracerProvider`/`MeterProvider`, export via OTLP to a local collector, and
  keep the SDK footprint out of hot inner loops by sampling at the entry span.
  Wire exporters up once at the composition root; do not scatter exporter
  configuration through library code.
- Keep logging/tracing off the measured path when benchmarking (see
  `performance-concurrency.md`); instrumentation overhead is easy to mistake
  for an algorithmic regression.

## Establish git workflow and review discipline

Keep formatting/linting out of human review: run `clang-format` and
`clang-tidy` before a commit reaches a reviewer, either via the `pre-commit`
framework (`pocc/pre-commit-hooks` or `cpp-linter-hooks`) or an equivalent CI
gate that blocks on the diff, not on reviewer opinion.

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pocc/pre-commit-hooks
    rev: v1.3.5
    hooks:
      - id: clang-format
        args: [-i]
      - id: clang-tidy
```

- Use a documented branching model (trunk-based with short-lived feature
  branches is the default unless the project states otherwise) and keep diffs
  small and reviewable; a reviewer cannot reliably hold more than roughly
  400-600 lines or a dozen classes in one pass.
- Write commit messages that state intent and, for a fix, the failure mode.
  Adopt Conventional Commits (`fix:`, `feat:`, `refactor:`, `perf:`) only if
  the project already has changelog/release tooling that consumes it; do not
  impose the convention without a consumer.
- Gate merges on the verification ladder in `quality-testing-security.md`
  (format, build with warnings, `clang-tidy`, relevant sanitizers) passing in
  CI before human review starts. Humans should review design, ownership, and
  correctness, not formatting or a warning a linter would have caught.
- Apply the review order from `quality-testing-security.md` (behavior and
  compatibility; lifetime/ownership; thread safety; input/overflow/UB; build
  and dependency impact; tests; then style) consistently, and flag template-
  heavy or concurrent diffs explicitly for a second reviewer rather than
  approving on trust.

## Primary sources

- [Doxygen manual: documenting the code](https://www.doxygen.nl/manual/docblocks.html)
- [spdlog](https://github.com/gabime/spdlog)
- [OpenTelemetry C++](https://opentelemetry.io/docs/languages/cpp/)
- [pre-commit framework](https://pre-commit.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)