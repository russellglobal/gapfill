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

## stack-md Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/stack_md.py" [path] [--stack name]
```

### Arguments
- **path**: Project directory (optional, defaults to current directory)
- **--stack, -s**: Tech stack name: `generic` (default), `spring-boot`, `react`

### Examples
```bash
# Create generic CLAUDE.md in current directory
python "{SKILL_DIR}/scripts/stack_md.py" .

# Create Spring Boot CLAUDE.md for a specific project
python "{SKILL_DIR}/scripts/stack_md.py" ./my-spring-project --stack spring-boot

# Create React CLAUDE.md
python "{SKILL_DIR}/scripts/stack_md.py" ./my-react-app -s react
```

### Execution Flow
1. Validate tech stack name
2. Load pre-defined template
3. Replace `{{project_name}}` placeholder
4. If `CLAUDE.md` does not exist: create it with template content
5. If `CLAUDE.md` already exists: write suggestions to `.claude/gapfill-suggestions.md` (never overwrite)

### After Execution
After the script completes, tell the user:
1. Whether CLAUDE.md was created or if suggestions were generated
2. The line count of the created file
3. If suggestions were generated, briefly summarize the key points

**Important**: Never overwrite an existing CLAUDE.md. Always generate `.claude/gapfill-suggestions.md` instead.

## review Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/review.py" [path]
```

### Arguments
- **path**: Project directory (optional, defaults to current directory)

### Examples
```bash
# Review current project before commit
python "{SKILL_DIR}/scripts/review.py" .

# Review a specific project
python "{SKILL_DIR}/scripts/review.py" ./my-project
```

### Execution Flow
1. Check src/ vs skills/src/ copy consistency
2. Verify all Python imports resolve to existing modules
3. Scan settings templates for dangerous permissions
4. Check for stale project names and deprecated references
5. Print report with errors and warnings
6. Exit with code 1 if any errors found

### After Execution
After the script completes:
1. If no issues: "审查通过，未发现问题 ✓"
2. If issues found: show categorized report with error/warning counts
3. Fix any errors before committing
