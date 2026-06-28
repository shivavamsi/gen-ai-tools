# Claude Skills — Full Reference

Source: https://code.claude.com/docs/en/skills

---

## What skills are

Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`.

Create a skill when you keep pasting the same instructions, checklist, or multi-step procedure into chat, or when a section of CLAUDE.md has grown into a procedure rather than a fact. Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it.

**Custom commands have been merged into skills.** A file at `.claude/commands/deploy.md` and a skill at `.claude/skills/deploy/SKILL.md` both create `/deploy` and work the same way. Skills add optional features: a directory for supporting files, frontmatter to control invocation, and the ability for Claude to load them automatically when relevant.

---

## Where skills live

| Location   | Path                                             | Applies to                     |
|:-----------|:-------------------------------------------------|:-------------------------------|
| Enterprise | See managed settings                             | All users in your organization |
| Personal   | `~/.claude/skills/<skill-name>/SKILL.md`         | All your projects              |
| Project    | `.claude/skills/<skill-name>/SKILL.md`           | This project only              |
| Plugin     | `<plugin>/skills/<skill-name>/SKILL.md`          | Where plugin is enabled        |

When skills share the same name across levels, enterprise overrides personal, and personal overrides project.

Skills also load from nested `.claude/skills/` directories below your working directory. When Claude reads or edits a file in a subdirectory, skills from that subdirectory's `.claude/skills/` become available (monorepo support).

If a nested skill shares a name with another skill, it gets a directory-qualified name, e.g. `apps/web:deploy`. Type the qualified name `/apps/web:deploy` to run it explicitly.

**Live change detection**: Adding, editing, or removing a skill takes effect within the current session without restarting.

---

## Directory structure

Each skill is a directory with `SKILL.md` as the entrypoint:

```
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

Reference supporting files from `SKILL.md` so Claude knows what they contain and when to load them:

```markdown
## Additional resources
- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files.

---

## How a skill gets its command name

The command you type comes from where the skill file lives. The frontmatter `name` field sets only the display label in skill listings.

| Skill location                                      | Command name source        | Example                                              |
|:----------------------------------------------------|:---------------------------|:-----------------------------------------------------|
| `.claude/skills/<name>/SKILL.md`                    | Directory name             | `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging` |
| Nested `.claude/skills/` (name clashes)             | Qualified path             | `apps/web/.claude/skills/deploy/SKILL.md` → `/apps/web:deploy` |
| `.claude/commands/<name>.md`                        | File name without extension| `.claude/commands/deploy.md` → `/deploy`             |
| Plugin `skills/<name>/SKILL.md`                     | Name, namespaced by plugin | `my-plugin/skills/review/SKILL.md` → `/my-plugin:review` |

---

## Frontmatter reference

All fields are optional. Only `description` is recommended.

```yaml
---
name: my-skill
description: What this skill does and when to use it
when_to_use: Additional trigger phrases or example requests
argument-hint: "[issue-number]"
arguments: [issue, branch]
disable-model-invocation: true
user-invocable: false
allowed-tools: Read Bash(git add *) Bash(git commit *)
disallowed-tools: AskUserQuestion
context: fork
agent: Explore
paths: "src/**/*.ts,apps/web/**"
model: claude-sonnet-4-6
effort: high
shell: bash
---
```

| Field | Required | Description |
|:------|:---------|:------------|
| `name` | No | Display name in skill listings. Defaults to directory name. Does not change the `/command` name. |
| `description` | Recommended | What the skill does and when to use it. Claude uses this to auto-load the skill. Put the key use case first — combined with `when_to_use`, truncated at 1,536 chars in skill listings. |
| `when_to_use` | No | Additional trigger phrases or example requests. Appended to `description` in the skill listing. |
| `argument-hint` | No | Hint shown during autocomplete. Example: `[issue-number]` or `[filename] [format]`. |
| `arguments` | No | Named positional arguments for `$name` substitution. Space-separated string or YAML list. Maps names to argument positions in order. |
| `disable-model-invocation` | No | Set `true` to prevent Claude from auto-loading this skill. Use for workflows you want to trigger manually. Also prevents preloading into subagents. Default: `false`. |
| `user-invocable` | No | Set `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`. |
| `allowed-tools` | No | Tools Claude can use without approval when this skill is active. Space- or comma-separated, or YAML list. Syntax: `Read`, `Bash(git *)`, `Bash(npm run *)`. |
| `disallowed-tools` | No | Tools removed from Claude's pool while this skill is active. Clears when you send your next message. |
| `context` | No | Set `fork` to run in an isolated subagent context. |
| `agent` | No | Subagent type when `context: fork` is set. Options: `Explore`, `Plan`, `general-purpose`, or any custom agent from `.claude/agents/`. Defaults to `general-purpose`. |
| `paths` | No | Glob patterns limiting when this skill auto-activates. Claude loads it automatically only when working with matching files. |
| `model` | No | Model override for this skill's turn. Applies for the rest of the current turn; session model resumes on next prompt. |
| `effort` | No | Effort level override: `low`, `medium`, `high`, `xhigh`, `max`. Overrides session effort level. |
| `hooks` | No | Hooks scoped to this skill's lifecycle. |
| `shell` | No | Shell for `` !`command` `` blocks: `bash` (default) or `powershell`. |

---

## String substitutions

| Variable | Description |
|:---------|:------------|
| `$ARGUMENTS` | All arguments passed at invocation. If absent from content, args are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Argument by 0-based index. Multi-word args need quotes: `/my-skill "hello world" second` → `$0` = `hello world`. |
| `$N` | Shorthand for `$ARGUMENTS[N]`. `$0` = first arg, `$1` = second. |
| `$name` | Named argument declared in `arguments` frontmatter. Maps to position in order. |
| `${CLAUDE_SKILL_DIR}` | Directory containing the skill's `SKILL.md`. Use to reference bundled scripts regardless of working directory. |
| `${CLAUDE_SESSION_ID}` | Current session ID. |
| `${CLAUDE_EFFORT}` | Active effort level: `low`, `medium`, `high`, `xhigh`, or `max`. |

To include a literal `$` before a digit, `ARGUMENTS`, or a declared arg name, escape with a backslash: `\$1.00`.

---

## Invocation control

By default, both you and Claude can invoke any skill.

| Frontmatter | You can invoke | Claude can invoke | When loaded into context |
|:------------|:---------------|:------------------|:------------------------|
| (default) | Yes | Yes | Description always in context; full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context; full skill loads when you invoke |
| `user-invocable: false` | No | Yes | Description always in context; full skill loads when invoked |

- Use `disable-model-invocation: true` for workflows with side effects: `/commit`, `/deploy`, `/send-slack-message`
- Use `user-invocable: false` for background knowledge that isn't a meaningful user action

---

## Dynamic context injection

The `` !`<command>` `` syntax runs shell commands **before** the skill content is sent to Claude. Command output replaces the placeholder — Claude only sees the rendered result.

```markdown
## Current changes
!`git diff HEAD`

## Branch status
!`git status --short`
```

The `!` must appear at the start of a line or immediately after whitespace. `` KEY=!`cmd` `` is not recognized.

For multi-line commands, use a fenced `` ```! `` block:

````markdown
## Environment
```!
node --version
npm --version
git status --short
```
````

Substitution runs once. Command output is not re-scanned for further placeholders.

To disable shell execution, set `"disableSkillShellExecution": true` in settings.

**Tip**: Include `ultrathink` anywhere in skill content to request deeper reasoning.

---

## Skill content lifecycle

When invoked, the rendered `SKILL.md` enters the conversation as a single message and stays for the rest of the session. Claude does not re-read the file on later turns.

After auto-compaction, Claude Code re-attaches the most recent invocation of each skill (first 5,000 tokens each). Re-attached skills share a combined 25,000-token budget, filled from most-recently-invoked first.

---

## Types of skill content

**Reference content** — knowledge Claude applies to your current work:
```yaml
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Task content** — step-by-step instructions for a specific action:
```yaml
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

---

## Run skills in a subagent

Add `context: fork` to run a skill in isolation. The skill content becomes the subagent's prompt — no access to conversation history.

> Only makes sense for skills with explicit task instructions. Guidelines without a task return without meaningful output.

```yaml
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:
1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

The `agent` field options: `Explore`, `Plan`, `general-purpose`, or any custom agent from `.claude/agents/`. Defaults to `general-purpose`.

---

## Pre-approve tools

`allowed-tools` grants permission for listed tools while the skill is active, without prompting:

```yaml
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

`disallowed-tools` removes tools from Claude's pool while the skill is active. Clears when you send your next message.

---

## Pass arguments

```yaml
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.
1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Positional args with named declarations:
```yaml
---
name: migrate-component
description: Migrate a component from one framework to another
arguments: [component, from_framework, to_framework]
---

Migrate the $component component from $from_framework to $to_framework.
Preserve all existing behavior and tests.
```

Run as: `/migrate-component SearchBar React Vue`

---

## Dynamic context example (full)

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request in 3-5 bullet points. Note any risks, missing tests, or breaking changes.
```

---

## Skill discovery & troubleshooting

**Skill not triggering**:
1. Check the description includes keywords users would naturally say
2. Verify it appears in `What skills are available?`
3. Try rephrasing your request to match the description
4. Invoke directly with `/skill-name` if user-invocable
5. If YAML frontmatter is malformed, Claude Code loads the body with empty metadata — `/skill-name` still works but auto-loading doesn't. Run with `--debug` to see parse errors.

**Skill triggers too often**:
1. Make the description more specific
2. Add `disable-model-invocation: true` for manual-only invocation

**Descriptions cut short**: Skill descriptions are truncated to fit a character budget (~1% of model context window). Descriptions for least-invoked skills are dropped first. Run `/doctor` to see which are affected. Trim `description` and `when_to_use`; put the key use case first.

---

## Share skills

- **Project**: commit `.claude/skills/` to version control
- **Personal**: install to `~/.claude/skills/`
- **Plugin**: create a `skills/` directory in your plugin
- **Managed**: deploy org-wide through managed settings

---

## Evaluate skills

Use the `skill-creator` plugin to automate evaluation:
```
/plugin install skill-creator@claude-plugins-official
```

It runs test cases in isolated subagents, grades assertions, benchmarks with vs. without the skill, and supports A/B version comparison.