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

Invoke this skill when the user mentions any of the following:
- "initialize project" / "new project" / "create project"
- "git init" / "create repository"
- "set up Claude config" / "permission config"
- "sync permissions" / "update permissions"
- "project skeleton"

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

## sync Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/sync.py" [root] [--base project_name]
```

### Arguments
- **root**: Directory to scan for projects (optional, defaults to parent of current directory)
- **--base, -b**: Base project name to compare against (optional, auto-detects from cwd)

### Examples
```bash
# Auto-detect base project from current directory
python "{SKILL_DIR}/scripts/sync.py" /path/to/projects

# Specify base project explicitly
python "{SKILL_DIR}/scripts/sync.py" /path/to/projects --base my-project
```

### Execution Flow
1. Scan directory tree for projects with `.claude/settings.local.json`
2. Collect `permissions.allow` rules from each project
3. Merge all unique rules and compute diff against base project
4. Print project summary and rule differences
5. Output JSON for Claude to process and present to user

### After Execution
After the script completes:
1. Present the diff report to the user
2. Ask which rules they want to sync
3. Output the updated `settings.local.json` content (do NOT write to files automatically)

**Important**: Always ask for user confirmation before generating any file changes. Never auto-modify `settings.local.json`.
