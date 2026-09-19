---
name: github-pr-reviewer
description: Use when comprehensively reviewing a GitHub pull request and, when authorized, posting inline review comments with gh.
---

# GitHub PR Reviewer

Follow the [task instructions](references/source.md). Treat the pull-request identifier in the current conversation as input; the legacy `$ARGUMENTS` marker only denotes user input. Do not post or modify a pull request unless the user has asked for that action.

For software work, also apply these engineering guardrails:

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.
