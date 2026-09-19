---
name: prompt-generator
description: Use when eliciting requirements and creating a reusable, model-agnostic Codex skill from a prompt idea.
---

# Prompt Generator

Follow the discovery and quality guidance in [the legacy instructions](references/source.md), with these Codex-specific requirements replacing its artifact schema:

- Create `.agents/skills/<skill-name>/SKILL.md` with `name` and `description` YAML frontmatter.
- Keep detailed or long-lived instructions in skill-local `references/` files and link to them from `SKILL.md`.
- Treat user messages and attachments as input; do not emit `$ARGUMENTS`, vendor-specific command formats, model choices, temperature settings, or execution-mode settings.
- Include the engineering guardrails below whenever the generated skill concerns software work.

1. Don't assume. Don't hide confusion. Surface tradeoffs.
2. Minimum code that solves the problem. Nothing speculative.
3. Touch only what you must. Clean up only your own mess.
4. Define success criteria. Loop until verified.
