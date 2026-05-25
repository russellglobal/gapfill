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

After installation, tell Claude Code:

> "Initialize a new project"

Or:

> "Create a project in ./my-project"

Claude will invoke the gapfill skill to run initialization.

## What `init` Does

1. **Environment check** — Detects git, SSH key availability
2. **Git init** — Initializes `.git` if the directory has no repo
3. **Scaffold files** — `.gitignore`, `README.md`, `settings.local.json`, `env-info.txt`
4. **Permission preset** — Pre-configures basic + low-risk permissions to reduce AI interaction rounds
5. **Environment probe** — Records available tools and versions
6. **Initial commit** — Auto-commits all scaffolded files

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
| v3 | `perm` (permission management), `lang` (language settings), `feedback` (one-click feedback) |
| v4 | `capture` (high-value interaction recording) |
| v5 | `publish` (multi-language README sync & consistency check) |

### Deprioritized
- `sync` — cross-project config comparison (built, paused — user base too small currently)
- `auto-guard` — Auto Mode fallback (rejected — overlaps with init/scan, competes with Anthropic's official Auto Mode evolution)
- `roadmap` — automatic decision logging (replaced by feasibility research process)
- `audit` — skill security scanning (replaced by `scan` for settings compliance)
- Team config sync — Anthropic Enterprise Admin covers this

## License

Apache 2.0

---

For Chinese documentation, see [README_zh.md](README_zh.md).

For terminology glossary, see [docs/glossary.md](docs/glossary.md).
