---
name: import-claude-command
description: Use when converting a legacy Claude CLI Markdown command into a model-agnostic Codex skill.
---

# Import Claude Command

Read the prompt in [the legacy conversion instructions](references/source.toml). Convert the supplied Claude command into `.agents/skills/<skill-name>/SKILL.md` with valid YAML frontmatter and any needed skill-local references.

Supersede the legacy target format: do not create a Gemini or Claude command file. Preserve the task intent, replace `$ARGUMENTS` with normal conversational input, and remove all model, temperature, and runtime-selection settings.

For software prompts, include these engineering guardrails:

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.
