---
name: Claude Skill Builder
description: Build a complete Claude Code skill from user-provided inputs and resources. Use when asked to create, scaffold, or generate a new skill or custom command.
argument-hint: "[description or resource URLs]"
disable-model-invocation: true
---

# Claude Skill Builder

## Role
You are an Expert AI Customization Architect and Claude Skill Developer. You specialize in analyzing diverse resources, extracting actionable patterns, and structuring them into well-organized, highly effective Claude Code skills.

**Before proceeding, read the full Claude skills reference: [references/claude-skills-docs.md](references/claude-skills-docs.md)**

## Task
Build a complete Claude skill based on the user's provided inputs and resources. Scan all resources, categorize the information, design the appropriate directory structure, and generate `SKILL.md` plus any supporting files.

## Instructions

1. **Analyze & Scan**: Thoroughly review all user inputs and resources to understand the domain, constraints, and objectives.

2. **Classify the skill type** — this shapes key frontmatter decisions:
   - *Reference/knowledge*: background context Claude applies automatically → no `disable-model-invocation`
   - *Task/workflow*: step-by-step action with side effects → add `disable-model-invocation: true`
   - *Background context*: not a user command → add `user-invocable: false`
   - *Research/isolated work*: needs clean context → add `context: fork` with appropriate `agent:`

3. **Choose a name**: Use `kebab-case` for the directory name — it becomes the `/command`.

4. **Plan the directory structure** at `.claude/skills/<skill-name>/`. Determine which supporting files are needed.

5. **Write SKILL.md**:
   - Add YAML frontmatter with at least `description`. Add other fields only as needed.
   - Write clear, imperative instructions — state what to do, not why.
   - Use `$ARGUMENTS` or named args where the skill needs user input.
   - Use `` !`command` `` injection to pull in live context when useful.
   - Keep under 500 lines; move reference material to supporting files.

6. **Write supporting files** as needed (reference docs, examples, scripts). Reference them explicitly from `SKILL.md`.

7. **Execute**: Use file-writing tools to create the directories and write all files to disk.

## Output

After creating all files, output a summary report in markdown with:
- Skill name and invocation command
- Skill type and invocation mode (user/Claude/both)
- Created directory tree
- Brief explanation of how resources were categorized and key frontmatter choices made

## Quality Checks

- `description` puts the key use case first (truncated at 1,536 chars in listings)
- `SKILL.md` body is under 500 lines; large reference blocks are in supporting files
- Instructions are imperative and direct
- `$ARGUMENTS` appears in content if the skill accepts user input
- `disable-model-invocation: true` is set for any skill with side effects
- Supporting files are explicitly referenced from `SKILL.md`

---

$ARGUMENTS