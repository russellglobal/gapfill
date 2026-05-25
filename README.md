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

| Before | After |
|--------|-------|
| Run `git init` manually | `gapfill init` sets up repo, config, and auto-commits for empty repos (or skips for existing projects) |
| Manually click "Allow" for every command | Pre-configured permissions reduce confirmations by ~80% |
| Copy `settings.local.json` from old projects | One `gapfill init` creates safe defaults |
| Write CLAUDE.md from scratch | `gapfill init --stack spring-boot` creates it during init, or `gapfill stack-claude-md` for existing projects |
| Commit without checking for issues | `gapfill review` runs 7 pre-commit checks in seconds |
| Manually audit 10 projects for dangerous permissions | `gapfill scan` audits all projects in seconds |

## Subcommands

### `init` — Project Bootstrap

**Use when:** Starting a new project.

```
gapfill init                           # basic init
gapfill init ./my-project              # init in specific dir
gapfill init --stack spring-boot       # init + CLAUDE.md in one step
gapfill init --stack spring-boot --lang zh  # init + Chinese CLAUDE.md
```

Creates `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt`.
Auto-detects git and SSH key status.
With `--stack`, also generates a tech-stack-specific CLAUDE.md.

1. **Environment check** — Detects git, SSH key availability
2. **Git init** — Initializes `.git` if the directory has no repo
3. **Scaffold files** — `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt`
4. **Permission preset** — Pre-configures basic + low-risk permissions to reduce AI interaction rounds
5. **Environment probe** — Records available tools and versions
6. **Initial commit** — Auto-commits all scaffolded files

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
| MVP | `init` (project initialization) |
| v2 | `sync` (cross-project config sync, done), `perm` (permission management), `lang` (language settings), `feedback` (one-click feedback) |
| v3 | `roadmap` (automatic decision logging) |
| v4 | `capture` (high-value interaction recording) |
| v5 | `audit` (skill security scanning), `publish` (multi-language README sync & consistency check) |

## License

Apache 2.0

---

For Chinese documentation, see [README_zh.md](README_zh.md).
For terminology glossary, see [docs/glossary.md](docs/glossary.md).
