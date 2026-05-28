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

## Product Strategy

### We Are Not "Enterprise-Grade" — We Are Irreplaceable

Five expert perspectives converge on one answer: "enterprise-grade" is not gapfill's direction. Not because the problem is unimportant, but because the wedge is wrong.

- **Product Strategy**: The enterprise market for "CLI tool procurement" doesn't exist. The play is to become the default configuration layer for AI-assisted development — the husky/prettier of the Claude Code ecosystem.
- **Security / Compliance**: Security teams buy demonstrable compliance, not safe defaults. Gapfill's role is the "developer workstation compliance layer" — referenced in AI usage policies, not purchased as a dashboard.
- **Developer Experience**: The best tools are ruthlessly opinionated about one thing. "Enterprise-grade" would destroy gapfill's rarest qualities: zero tokens, determinism, user sovereignty.
- **China Market**: "企业级" in the Chinese dev community means "expensive, heavy, hard to use." "溜缝儿" is the differentiator — warm, humble, practical, aligned with the "别整虚的，能跑就行" ethos.
- **Ecosystem Defense**: Platform absorption risk exists, but the cross-platform governance layer is the moat. Become the ESLint of AI coding tools — not glamorous, but indispensable once a team scales.

### The Path

1. **Deepen developer experience first** — more stack templates (Next.js, FastAPI, Go, Rust), make `gapfill init` the fastest path from `mkdir` to a working AI coding session.
2. **Abstract to cross-platform** — not bound to Claude Code alone. Support Cursor, Copilot, and others. Become the universal governance layer for AI coding tools.
3. **Enterprise adoption bottoms-up** — developers install it, managers can't stop it. Not sold as licenses, adopted as baseline infrastructure.

**One sentence: Don't chase enterprise-grade. Chase irreplaceability. When every AI coding user runs gapfill, enterprise-grade arrives on its own.**
