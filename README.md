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

After installation, tell Claude Code to run a gapfill subcommand.

### `init` — Project Initialization

**When to use:** Starting a new project from scratch.

**Say this:** "gapfill init" or "use gapfill to initialize ./my-project"

**What it does:**
1. Detects git, SSH key availability
2. Initializes `.git` if no repo exists
3. Scaffolds: `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt`
4. Pre-configures basic + low-risk permissions
5. Records available tools and versions
6. Auto-commits all scaffolded files

**Constraints:** Local initialization only. No remote repository creation, no framework-specific setup.

### `stack-md` — Tech-Stack-Aware CLAUDE.md

**When to use:** A new project needs a CLAUDE.md, or you want stack-specific conventions.

**Say this:** "gapfill stack-md --stack spring-boot ./my-project"

| Stack | When to use |
|-------|-------------|
| `generic` (default) | Unknown tech stack, general project |
| `spring-boot` | Java + Spring Boot 3.x project |
| `react` | React 19 + TypeScript project |

**Constraints:** Pre-defined templates only — no LLM calls. Never overwrites existing CLAUDE.md; writes suggestions to `.claude/gapfill-suggestions.md` instead.

### `review` — Pre-Commit Health Check

**When to use:** Before committing, to catch issues from recent changes (dead imports, copy drift, stale content).

**Say this:** "gapfill review"

**Checks:**
- Copy consistency (src/ vs skills/src/)
- Import validity (dead imports via AST)
- Dangerous permissions in settings templates
- Stale content (old project names, deprecated refs)

**Constraints:** Report-only. Does not modify any files.

### `scan` — Settings Compliance Audit

**When to use:** Auditing a directory of projects for dangerous permissions.

**Say this:** "gapfill scan /path/to/projects"

**Scans for:**
- **High risk**: Write(/**), Edit(/**), Bash(curl:*), Bash(wget:*), WebFetch(domain:*)
- **Low risk**: Bash(find:*), Bash(npx:*), Bash(python:*)

**Constraints:** Report-only. Reads `settings.local.json` but does not modify.

### `sync` — Cross-Project Permission Sync

**When to use:** You have multiple projects with different permission rules and want a merged configuration.

**Say this:** "gapfill sync"

**Constraints:** Report-only. Suggests a merged config but does not write to files automatically.

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

See [ROADMAP.md](ROADMAP.md).

## License

Apache 2.0

---

For Chinese documentation, see [README_zh.md](README_zh.md).
For terminology glossary, see [docs/glossary.md](docs/glossary.md).
For project philosophy, see [PHILOSOPHY.md](PHILOSOPHY.md) / [中文版](PHILOSOPHY_zh.md).
