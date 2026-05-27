# gapfill Philosophy

## Positioning: Filling the "Management Vacuum" of AI Coding Assistants

Claude Code is great at writing code, but it doesn't manage the project. gapfill fills that gap — permission presets, documentation scaffolding, git workflows, pre-commit checks. It doesn't write a single line of business code, yet it makes Claude Code safe and productive in every project.

**In one sentence: gapfill is infrastructure for Claude Code, not a competitor.**

## Core Principles

### 1. Zero Token Consumption

Every gapfill operation — init, review, scan — runs locally. No LLM API calls, no code or config sent externally.

**Why it matters:** Your code and permission configs are sensitive. They shouldn't leave your machine just to "generate a project skeleton." Zero token also means zero cost, zero latency, zero network dependency.

### 2. Determinism

Same input, same output. No randomness, no "AI hallucinations," no irreproducible results. gapfill is a deterministic tool — it works the same today as it will next year.

**Why it matters:** Project initialization is infrastructure behavior. It should not have "creativity." Leave creativity to Claude, leave determinism to gapfill.

### 3. Security First

- Permission templates only include safe operations (read/git/build), no high-risk rules like `Write(/**)`
- Never overwrites user-owned files (CLAUDE.md, settings.local.json)
- No auto-commit on existing projects
- Dangerous operations require explicit user confirmation

**Why it matters:** Permission config is a security boundary — once widened, it's hard to roll back. Safe by default beats convenient by default.

### 4. Minimalism

- Zero external dependencies — just Python 3.8+ and git
- No config files, no database, no background services
- One command, done, gone — nothing lingers

**Why it matters:** A management tool shouldn't itself need to be managed.

### 5. Respect User Sovereignty

- Existing configs get asked about, not overwritten
- Non-interactive mode defaults to conservative (skip, don't force)
- All output is readable, auditable, rejectable
- Git history is sacred — no force commits on existing repos

**Why it matters:** Tools should amplify user control, not replace user decisions.

## The Name

**gapfill** — filling the gaps. Filling the space between Claude Code's capabilities and actual project management needs.

**溜缝儿** — a Chinese colloquialism for filling small cracks in walls or objects. Extended meaning: fixing those "not-quite-problems-but-still-annoying" details. Not a renovation — a fine-tuning.

## What It Is Not

- **Not** a Claude Code replacement — it's the prep and follow-through for Claude Code
- **Not** a project scaffolder (like create-react-app) — it doesn't generate business code or framework templates
- **Not** a config manager (like Ansible) — it doesn't do system-level config, only Claude Code project config
- **Not** an AI tool — it calls no models, pure local deterministic execution

## Value Proposition

| Dimension | Without gapfill | With gapfill |
|-----------|----------------|--------------|
| New project setup | ~15 min manual config | 1 command, ~5 sec |
| Token consumption | May consume tokens (if AI-generated) | 0 |
| Security risk | Manual config may miss or misconfigure | Unified templates, auditable |
| Permission management | Click "Allow" on every command | Preset permissions, ~80% fewer confirmations |
| Pre-commit checks | Based on experience or forgotten | 7 automated checks |
| Multi-project consistency | Each project configured differently | Unified templates, guaranteed consistency |
