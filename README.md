# gapfill

**Stop clicking "Allow" on Claude Code. Bootstrap projects with the right permissions, docs, and git skeleton in one command.**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache_2.0-green.svg)](LICENSE)
[![Zero deps](https://img.shields.io/badge/dependencies-0-lightgrey.svg)]()

[English](README.md) · [中文](README_zh.md)

## The Problem

Claude Code is powerful, but starting a new project means:

- 🔁 **Clicking "Allow"** on every `git status`, `npm install`, `pip show`
- 📋 **Copying `settings.local.json`** from old projects and hoping it works
- 📄 **Writing CLAUDE.md from scratch** with no template to start from
- 🔍 **Never knowing** if your permissions contain dangerous rules like `Write(/**)`

Gapfill solves all four in seconds — zero LLM calls, zero dependencies, just Python.

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
| Run `git init` manually | `gapfill init` sets up repo, config, and commits in one step |
| Manually click "Allow" for every command | Pre-configured permissions reduce confirmations by ~80% |
| Copy `settings.local.json` from old projects | One `gapfill init` creates safe defaults |
| Write CLAUDE.md from scratch | `gapfill init --stack spring-boot` creates it during init, or `gapfill stack-claude-md` for existing projects |
| Commit without checking for issues | `gapfill review` catches dead imports, stale content, permission drift |
| Manually audit 10 projects for dangerous permissions | `gapfill scan` audits all projects in seconds |

## Subcommands

### `init` — Project Bootstrap

**Use when:** Starting a new project.

```
gapfill init                           # basic init
gapfill init ./my-project              # init in specific dir
gapfill init --stack spring-boot       # init + CLAUDE.md in one step
```

Creates `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt` and commits them.
Auto-detects git and SSH key status.
With `--stack`, also generates a tech-stack-specific CLAUDE.md.

### `stack-claude-md` — CLAUDE.md Generator

**Use when:** An existing project needs a CLAUDE.md. (For new projects, use `gapfill init --stack`.)

```
gapfill stack-claude-md                  # generic template
gapfill stack-claude-md --stack spring-boot  # Spring Boot 3.x
gapfill stack-claude-md --stack react        # React 19 + TypeScript
```

Pre-defined templates — no LLM calls. Never overwrites existing CLAUDE.md.

### `review` — Pre-Commit Check

**Use when:** Before `git commit`, catch issues from recent changes.

```
gapfill review
```

Checks: copy consistency, dead imports, dangerous permissions in templates, stale project names. Exits with code 1 if errors found.

### `scan` — Permission Audit

**Use when:** Auditing a directory of projects for dangerous permissions.

```
gapfill scan /path/to/projects
```

Scans all `settings.local.json` files and flags high-risk (`Write(/**)`, `Bash(curl:*)`) and low-risk (`Bash(find:*)`, `Bash(python:*)`) permissions.

### `sync` — Permission Comparison

**Use when:** You have multiple projects with different permission rules.

```
gapfill sync
```

Shows differences and suggests a merged configuration. Report-only.

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

## Contributing

Found a bug? Open an [issue](https://github.com/russellglobal/gapfill/issues).
Want to contribute? Fork the repo and submit a PR.

If gapfill saves you time, a star ⭐ helps others find it too.

## License

Apache 2.0

---

For Chinese documentation, see [README_zh.md](README_zh.md).
For terminology glossary, see [docs/glossary.md](docs/glossary.md).
