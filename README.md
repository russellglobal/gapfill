# gapfill

AI-assisted development toolkit — Bootstrap new projects with Claude Code permissions, docs, and git skeleton in one command.

[English](README.md) · [中文](README_zh.md)

## Installation

Copy the `skills/gapfill/` directory to your Claude Code skills directory:

```bash
cp -r skills/gapfill ~/.claude/skills/gapfill
```

Requires **Python 3.8+** and **git**. Zero external dependencies.

## Usage

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
User ←→ gapfill Skill (dialogue layer, SKILL.md)
                ↓ invokes
        Internal Python scripts (execution layer, scripts/init.py)
```

- **Skill is the user interface**: handles dialogue, review, exceptions
- **Scripts are the execution engine**: guarantees speed and determinism, consumes zero tokens
- **Not published to PyPI**: distributed alongside the skill

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
