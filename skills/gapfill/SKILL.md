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
python "{SKILL_DIR}/scripts/init.py" [path] [--lang zh] [--stack name]
```

### Arguments
- **path**: Project directory path (optional, defaults to current directory)
- **--lang**: Language for generated files: `en` (default), `zh`
- **--stack**: Tech stack for CLAUDE.md: `generic`, `spring-boot`, `react`

### Examples
```bash
# Initialize in current directory (English README)
python "{SKILL_DIR}/scripts/init.py" .

# Initialize with Chinese README
python "{SKILL_DIR}/scripts/init.py" . --lang zh

# Initialize with Spring Boot CLAUDE.md and Chinese README
python "{SKILL_DIR}/scripts/init.py" ./my-project --stack spring-boot --lang zh
```

### Execution Flow
1. Environment check (git / SSH key)
2. Git initialization (if no .git exists)
3. Scaffold files: .gitignore, README.md, settings.local.json, env-info.txt
4. Permission preset: basic + low-risk levels
5. Environment probe: record available tools and versions
6. Initial commit (chore: init project by gapfill)

### settings.local.json Handling
The script always performs a **union merge** — it never overwrites existing permissions. If `settings.local.json` already exists, it merges the template rules with the existing ones (deduplicating via set union). The output will show `+N 条规则` if new rules were added, or `已是最新` if no changes were needed. This is safe and idempotent.

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

## stack-claude-md Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/stack_claude_md.py" [path] [--stack name] [--lang zh]
```

### Arguments
- **path**: Project directory (optional, defaults to current directory)
- **--stack, -s**: Tech stack name: `generic` (default), `spring-boot`, `react`
- **--lang**: Language: `en` (default), `zh`

### Examples
```bash
# Create generic CLAUDE.md in current directory
python "{SKILL_DIR}/scripts/stack_claude_md.py" .

# Create Spring Boot CLAUDE.md for a specific project
python "{SKILL_DIR}/scripts/stack_claude_md.py" ./my-spring-project --stack spring-boot

# Create React CLAUDE.md with Chinese README
python "{SKILL_DIR}/scripts/stack_claude_md.py" ./my-react-app -s react --lang zh
```

### Execution Flow
1. Validate tech stack name
2. Load pre-defined template
3. Replace `{{project_name}}` placeholder
4. If `CLAUDE.md` does not exist: create it with template content
5. If `CLAUDE.md` already exists: write suggestions to `.claude/claude-suggestions.md` (never overwrite)

### After Execution
After the script completes, tell the user:
1. Whether CLAUDE.md was created or if suggestions were generated
2. The line count of the created file
3. If suggestions were generated, briefly summarize the key points

**Important**: Never overwrite an existing CLAUDE.md. Always generate `.claude/claude-suggestions.md` instead.

## scan Subcommand

### Usage
```bash
python "{SKILL_DIR}/scripts/scan.py" [path]
```

### Arguments
- **path**: Directory to scan for projects (optional, defaults to current directory)

### Examples
```bash
# Scan current directory for projects
python "{SKILL_DIR}/scripts/scan.py" .

# Scan a specific directory
python "{SKILL_DIR}/scripts/scan.py" /path/to/projects
```

### Execution Flow
1. Scan directory tree for projects with `.claude/settings.local.json`
2. Classify each project as clean, low-risk, or high-risk based on permissions
3. Print summary with icons for each project

### After Execution
After the script completes:
1. Show the project summary with pass/warning/fail icons
2. If any project has high-risk permissions, highlight them
3. No file modifications — scan is read-only

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
