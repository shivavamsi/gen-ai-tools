---
name: python-developer
description: Professional Python development practices — project setup (pyproject.toml, uv, ruff, mypy, pytest, pre-commit, CI), code quality and typing, testing strategy including fixtures and Hypothesis property-based tests, security auditing (Bandit, pip-audit, Semgrep, detect-secrets), performance profiling and benchmarking, API design and deprecation, CLI development with Click or Typer, MCP servers with FastMCP, docstrings and Sphinx docs, packaging and PyPI distribution, release management and changelogs, whole-library review, and web app architecture. Use this whenever writing, reviewing, refactoring, testing, structuring, packaging, profiling, securing, or debugging Python code — including choosing tooling or dependencies, configuring linters or type checkers, laying out modules, adding tests, wiring CI, or preparing a release. Consult it even when the request doesn't name a specific tool or file.
metadata:
  version: "1.0"
---

# Python Developer

Thirteen topics of Python practice, one reference file each. This page is a
router — it exists so you can pick the right file instead of loading all of
the reference material at once. Read the topic file when you're doing that
kind of work; skip it when you already know the answer.

## How to use this

1. Find your task in the routing table below.
2. Read the **Start here** file for that topic. That file alone answers most
   questions and tells you when to go deeper.
3. Read a **Deeper** file only when the start file points you at it, or when
   your task is specifically about that sub-topic.

Reference files live in `references/`. Executable helpers live in `scripts/`.
All paths below are relative to this skill's directory.

## Routing table

| If you are… | Start here | Deeper |
| --- | --- | --- |
| Creating a project, or modernizing one onto `pyproject.toml`; configuring uv, pre-commit, Makefile, or CI | `references/project-setup.md` | `references/project-setup-pyproject.md`, `references/project-setup-ci.md`, `references/project-setup-makefile.md` |
| Reviewing or refactoring for quality; adding type hints; configuring ruff or mypy | `references/code-quality.md` | `references/code-quality-ruff-config.md`, `references/code-quality-mypy-config.md`, `references/code-quality-type-patterns.md` |
| Writing tests, raising coverage, designing fixtures, or adding property-based tests | `references/testing-strategy.md` | `references/testing-strategy-fixtures.md`, `references/testing-strategy-hypothesis.md` |
| Auditing for vulnerabilities, scanning dependencies, hunting hardcoded secrets, or gating security in CI | `references/security-audit.md` | `references/security-audit-vulnerabilities.md`, `references/security-audit-ci-security.md` |
| Chasing a slow path, a memory leak, or setting up regression benchmarks | `references/performance.md` | `references/performance-profiling.md`, `references/performance-benchmarks.md` |
| Designing a public API, or managing deprecations and breaking changes | `references/api-design.md` | `references/api-design-patterns.md`, `references/api-design-evolution.md` |
| Building a command-line interface | `references/cli-development.md` | `references/cli-development-click-patterns.md`, `references/cli-development-typer-guide.md` |
| Writing an MCP server, or exposing a tool/CLI to an LLM client | `references/mcp-servers.md` | — |
| Writing docstrings, setting up Sphinx, or authoring tutorials | `references/documentation.md` | `references/documentation-sphinx-config.md`, `references/documentation-tutorials.md` |
| Packaging for distribution, publishing to PyPI, or debugging a build backend | `references/packaging.md` | `references/packaging-conda.md` |
| Cutting a release, versioning, or writing a changelog | `references/release-management.md` | `references/release-management-automation.md`, `references/release-management-migration.md` |
| Auditing a whole library's health and producing a report | `references/library-review.md` | `references/library-review-checklist.md`, `references/library-review-report-template.md` |
| Architecting a web app or SaaS backend | `references/web-app-architecture.md` | `references/web-app-architecture-stack.md`, `references/web-app-architecture-auth.md`, `references/web-app-architecture-payments.md`, `references/web-app-architecture-background-jobs.md`, `references/web-app-architecture-frontend.md`, `references/web-app-architecture-deployment.md` |

Several tasks span topics. Adding a tested, typed, linted module touches
code-quality *and* testing-strategy; hardening a release touches security-audit
*and* release-management. Read both start files rather than guessing which one
owns the question.

## Scripts

Run these directly rather than reimplementing them:

| Script | Purpose |
| --- | --- |
| `scripts/create_project.py` | Scaffold a new project with the layout and tooling from `project-setup.md`. |
| `scripts/security_scan.py` | Run Bandit, pip-audit, Semgrep, and detect-secrets together and aggregate results. |
| `scripts/bump_version.py` | Bump the version across `pyproject.toml` and `__init__.py`, and update the changelog. |

Read a script's `--help` before running it. They're upstream code, not written
for any one project — check assumptions about paths and layout before trusting
output.

## Applying this in a project

These references are deliberately generic — they describe Python practice, not
this repository. When a reference conflicts with the project's own conventions,
**the project wins**. Check `AGENTS.md` (or `CLAUDE.md`) at the repo root first;
it records the toolchain, layout, and commands that actually apply here, and an
explicit instruction from the user overrides both.

Two conflicts worth knowing about in advance:

- Much of this material assumes you are building a **public, installable
  library** — PyPI releases, semantic-version contracts with external users,
  Sphinx sites. If the project is a private application, treat the
  packaging, release-management, api-design, and library-review topics as
  background rather than requirements.
- Some files show `pip`, `requirements.txt`, or `setup.py` where those are the
  subject being discussed. That is not an endorsement over whatever the project
  actually uses.
