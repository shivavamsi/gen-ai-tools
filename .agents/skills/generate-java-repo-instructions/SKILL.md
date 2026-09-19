---
name: generate-java-repo-instructions
description: Use when analyzing a Java or Spring Boot repository to generate concise, actionable repository instructions for Codex.
---

# Generate Java Repository Instructions

Follow the [task instructions](references/source.md), with these Codex-specific adaptations:

- Generate `AGENTS.md` at the repository root unless the user specifies another path.
- Replace references to `CLAUDE.md` or `.claude/CLAUDE.md` with `AGENTS.md`.
- Treat the repository and current conversation as input; the legacy `$ARGUMENTS` marker only denotes user input.

For software work, also apply these engineering guardrails:

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.
