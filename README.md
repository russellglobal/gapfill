# gapfill

AI-assisted development toolkit — like Hutool for the AI era. Bootstrap new projects with Claude Code permissions, docs, and git skeleton in one command.

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
3. **Scaffold files** — `.gitignore`, `README.md`, `CLAUDE.md`, `settings.local.json`, `env-info.txt`
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
| MVP | `init` (project initialization) |
| v2 | `sync` (cross-project config sync), `perm` (permission management), `lang` (language settings), `feedback` (one-click feedback) |
| v3 | `roadmap` (automatic decision logging) |
| v4 | `capture` (high-value interaction recording) |
| v5 | `audit` (skill security scanning), `skill-localize` (open-source skill localization) |

## License

MIT

---

## 中文说明

> gapfill（溜缝儿）是 AI 开发者的通用工具箱，类似 Java 生态的 Hutool。为新项目自动初始化 Claude Code 权限、配置和文档骨架，让 AI 助手开箱即用。

详细中文文档请参阅项目 README 英文部分，或提交 Issue 请求中文版。

### 术语表

关键术语的中英文对照见 [docs/glossary.md](docs/glossary.md)。新增翻译前请先查阅。
