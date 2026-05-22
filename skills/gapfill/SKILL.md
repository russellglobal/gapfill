---
name: gapfill
description: Gapfill - A universal toolkit for AI developers. Initialize new projects, manage Claude Code configs, sync permissions, and more.
---

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
3. Scaffold files: .gitignore, README.md, CLAUDE.md, settings.local.json, env-info.txt
4. Permission preset: basic + low-risk levels
5. Environment probe: record available tools and versions
6. Initial commit (chore: init project by gapfill)

### After Execution
After the script completes, confirm with the user:
1. List of created files
2. Environment probe results
3. Error messages with troubleshooting suggestions if any
