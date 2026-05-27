# gapfill

**Stop clicking "Allow" on Claude Code. Bootstrap projects with the right permissions, docs, and git skeleton in one command.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)
[![Zero deps](https://img.shields.io/badge/dependencies-0-lightgrey.svg)]()
[![Zero tokens](https://img.shields.io/badge/token_cost-0-purple.svg)]()

[English](README.md) · [中文](README_zh.md)

## The Problem

Claude Code is powerful, but starting a new project means:

- 🔁 **Clicking "Allow"** on every `git status`, `npm install`, `pip show`
- 📋 **Copying `settings.local.json`** from old projects and hoping it works
- 📄 **Writing CLAUDE.md from scratch** with no template to start from
- 🔍 **Never knowing** if your permissions contain dangerous rules like `Write(/**)`

Gapfill solves all four in seconds — zero LLM calls, zero dependencies, just Python. Every operation runs locally and deterministically — **no tokens consumed** during init, review, or scan. A new project takes about 15 minutes of manual setup; gapfill does it in one command.

## Quick Start

```bash
# 1. Clone
git clone https://github.com/russellglobal/gapfill.git

# 2. Install skill
cp -r gapfill/skills/gapfill ~/.claude/skills/gapfill

# 3. Use it
cd your-project
gapfill init
```

Requires **Python 3.8+** and **git**. That's it.

## What It Does

After installation, tell Claude Code to run a gapfill subcommand:

```
gapfill init              # Initialize a new project
gapfill init ./my-project # Initialize in a specific directory
gapfill stack-md          # Generate CLAUDE.md for your tech stack
gapfill review            # Pre-commit project health check
gapfill scan              # Scan settings for dangerous permissions
gapfill sync              # Cross-project permission comparison
```

Or use the CLI directly:

```bash
python scripts/init.py [path]
python scripts/stack_md.py [path] [--stack name]
python scripts/review.py [path]
python scripts/scan.py [path]
python scripts/sync.py [root] [--base project_name]
```

## Subcommands

### `init` — Project Initialization

1. **Environment check** — Detects git, SSH key availability
2. **Git init** — Initializes `.git` if the directory has no repo
3. **Scaffold files** — `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt`
4. **Permission preset** — Pre-configures basic + low-risk permissions to reduce AI interaction rounds
5. **Environment probe** — Records available tools and versions
6. **Initial commit** — Auto-commits all scaffolded files

### `stack-md` — Tech-Stack-Aware CLAUDE.md

Generates a CLAUDE.md tailored to your project's tech stack. Pre-defined templates only — no LLM calls.

| Stack | Description |
|-------|-------------|
| `generic` (default) | General project with branch workflow and security rules |
| `spring-boot` | Spring Boot 3.x conventions, anti-patterns, build commands |
| `react` | React 19 + TypeScript conventions, anti-patterns, build commands |

If CLAUDE.md already exists, suggestions are written to `.claude/gapfill-suggestions.md` (never overwrites).

### `review` — Pre-Commit Health Check

Scans the project for:
- Copy consistency (src/ vs skills/src/)
- Import validity (dead imports via AST)
- Dangerous permissions in settings templates
- Stale content (old project names, deprecated refs)

Exits with code 1 if errors found.

### `scan` — Settings Compliance Audit

Scans a directory tree for all projects' `settings.local.json` and checks for dangerous permissions:
- **High risk**: Write(/**), Edit(/**), Bash(curl:*), Bash(wget:*), WebFetch(domain:*)
- **Low risk**: Bash(find:*), Bash(npx:*), Bash(python:*)

### `sync` — Cross-Project Permission Sync

Compares permissions across multiple projects and suggests a merged configuration.

## Architecture

```
User ←→ gapfill Skill (dialogue layer)
                ↓ invokes
        Python scripts (execution layer, zero tokens)
```

- **Skill is the UI**: handles conversation, review, exceptions
- **Scripts are the engine**: fast, deterministic, consumes no tokens
- **Not on PyPI**: distributed with the skill, always in sync

## Roadmap

| Version | Features |
|---------|----------|
| MVP | `init` (project initialization), `.gitignore`, `settings.local.json` preset |
| v2 | `stack-md` (tech-stack-aware CLAUDE.md) **DONE**, `review` (pre-commit health check) **DONE**, `scan` (settings compliance audit) **DONE** |
| v3 | _TBD_ — validate review/scan adoption first |
| v4 | _TBD_ — `publish` (multi-language doc sync) deferred |
| v5 | _TBD_ |

### Deprioritized
- `sync` — cross-project config comparison (built, paused — user base too small currently)
- `auto-guard` — Auto Mode fallback (rejected — overlaps with init/scan, competes with Anthropic's official Auto Mode evolution)
- `perm` — JSON editing doesn't need CLI wrapper (scan is sufficient)
- `feedback` — `gh issue create` already covers this
- `lang` — merged into `publish`
- `capture` — concept valuable but scope unclear; revisit with real user feedback
- `publish` — deferred to v4+; valuable but not urgent until multi-language user base grows
- `roadmap` — automatic decision logging (replaced by feasibility research process)
- `audit` — skill security scanning (replaced by `scan` for settings compliance)
- Team config sync — Anthropic Enterprise Admin covers this

## License

Apache 2.0

---

For Chinese documentation, see [README_zh.md](README_zh.md).
For terminology glossary, see [docs/glossary.md](docs/glossary.md).
For project philosophy, see [PHILOSOPHY.md](PHILOSOPHY.md) / [中文版](PHILOSOPHY_zh.md).
