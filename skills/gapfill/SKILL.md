---
name: gapfill
description: Gapfill - A universal toolkit for AI developers. Initialize new projects, manage Claude Code configs, sync permissions, and more.
---

## Installation

Copy the `skills/gapfill/` directory to your Claude Code skills directory:

```bash
cp -r skills/gapfill ~/.claude/skills/gapfill
```

Requires **Python 3.8+** and **git**. Zero external dependencies.

## Triggers

Invoke this skill when the user mentions gapfill:
- "gapfill init" / "initialize with gapfill"
- "gapfill stack-claude-md" / "generate CLAUDE.md with gapfill"
- "gapfill review" / "review project with gapfill"
- "gapfill scan" / "scan permissions with gapfill"
- "gapfill sync" / "sync permissions with gapfill"

**Note**: Do NOT trigger solely based on "initialize project" — this may invoke Claude Code's built-in behavior. The user must explicitly mention gapfill.

## init Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/init.py" [path]
```

### Arguments
- **path**: Project directory path (optional, defaults to current directory)

### Examples
```bash
# Initialize in current directory
python "{SKILL_DIR}/scripts/init.py" .

# Initialize in a specific directory
python "{SKILL_DIR}/scripts/init.py" ./my-project
```

### Execution Flow
1. Environment check (git / SSH key)
2. Git initialization (if no .git exists)
3. Scaffold files: .gitignore, README.md, settings.local.json, env-info.txt
4. Permission preset: basic + low-risk levels
5. Environment probe: record available tools and versions
6. Initial commit (chore: init project by gapfill)

### After Execution
After the script completes, confirm with the user:
1. List of created files
2. Environment probe results
3. Error messages with troubleshooting suggestions if any

**Important**: Only describe what gapfill has actually done. Do NOT suggest capabilities that do not yet exist (e.g., remote repo setup, backend framework initialization, etc.). After init completes, simply ask "接下来需要做什么？" without listing unimplemented features.
