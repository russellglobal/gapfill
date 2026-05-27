"""review subcommand - Pre-commit project health check."""

import ast
import json
import sys
from dataclasses import dataclass
from pathlib import Path

from gapfill.utils import fix_windows_encoding

fix_windows_encoding()

HIGH_RISK_PERMISSIONS = [
    "Write(/**)",
    "Edit(/**)",
    "Bash(curl:*)",
    "Bash(wget:*)",
    "WebFetch(domain:*)",
]

LOW_RISK_PERMISSIONS = [
    "Bash(find:*)",
    "Bash(npx:*)",
    "Bash(node:*)",
    "Bash(python:*)",
    "Bash(python3:*)",
    "Bash(pip install:*)",
    "Bash(npm install:*)",
]

STALE_PATTERNS = [
    "aidev",  # old project name
]

SENSITIVE_FILE_PATTERNS = [
    ".env",
    "*.key", "*.pem", "*.crt",
    "credentials.json", "secrets.json",
    "*.id_rsa", "*.id_ed25519",
]

ALL_CHECKS = [
    "副本一致性", "死引用", "危险权限",
    "过期内容", "JSON 语法", "脚本语法",
    "敏感文件忽略",
]


@dataclass
class Issue:
    severity: str  # "error" or "warning"
    category: str
    message: str


def review_command(args):
    """Execute the review subcommand."""
    project_path = Path(args.path).resolve()

    if not project_path.exists():
        print(f"错误: 目录不存在: {project_path}")
        sys.exit(1)

    issues = []
    checks_run = []
    files_scanned = 0

    # Run all 7 checks
    result = check_copy_consistency(project_path)
    checks_run.append("副本一致性")
    issues.extend(result)

    result, count = check_imports(project_path)
    checks_run.append("死引用")
    issues.extend(result)
    files_scanned += count

    result = check_permissions(project_path)
    checks_run.append("危险权限")
    issues.extend(result)

    result = check_stale_content(project_path)
    checks_run.append("过期内容")
    issues.extend(result)

    result, count = check_json_syntax(project_path)
    checks_run.append("JSON 语法")
    issues.extend(result)
    files_scanned += count

    result, count = check_scripts_syntax(project_path)
    checks_run.append("脚本语法")
    issues.extend(result)
    files_scanned += count

    result = check_sensitive_files(project_path)
    checks_run.append("敏感文件忽略")
    issues.extend(result)

    _print_report(issues, checks_run, files_scanned)

    if any(i.severity == "error" for i in issues):
        sys.exit(1)


def check_copy_consistency(project_path):
    """Check that src/ and skills/src/ are consistent."""
    issues = []
    src_dir = project_path / "src" / "gapfill"
    skills_dir = project_path / "skills" / "gapfill" / "src" / "gapfill"

    if not src_dir.exists() or not skills_dir.exists():
        return issues

    src_files = set()
    for f in src_dir.rglob("*"):
        if f.is_file() and not f.name.endswith(".pyc") and f.parent.name != "__pycache__":
            src_files.add(f.relative_to(src_dir))

    skills_files = set()
    for f in skills_dir.rglob("*"):
        if f.is_file() and not f.name.endswith(".pyc") and f.parent.name != "__pycache__":
            skills_files.add(f.relative_to(skills_dir))

    for rel_path in sorted(src_files - skills_files):
        issues.append(Issue(
            "error",
            "副本缺失",
            f"{rel_path} 存在于 src/ 但不存在于 skills/src/"
        ))

    for rel_path in sorted(skills_files - src_files):
        issues.append(Issue(
            "warning",
            "副本多余",
            f"{rel_path} 存在于 skills/src/ 但不存在于 src/"
        ))

    for rel_path in sorted(src_files & skills_files):
        src_file = src_dir / rel_path
        skills_file = skills_dir / rel_path
        if src_file.read_bytes() != skills_file.read_bytes():
            issues.append(Issue(
                "error",
                "副本不一致",
                f"{rel_path} 在 src/ 和 skills/src/ 内容不同"
            ))

    return issues


def check_imports(project_path):
    """Check that all local imports in gapfill resolve to existing files."""
    issues = []
    src_dir = project_path / "src" / "gapfill"

    if not src_dir.exists():
        return issues, 0

    available = set()
    for f in src_dir.rglob("*.py"):
        if f.name == "__init__.py":
            mod_path = f.relative_to(src_dir.parent).parent
            available.add(str(mod_path).replace("/", "."))
        else:
            mod_path = f.relative_to(src_dir.parent).with_suffix("")
            available.add(str(mod_path).replace("/", "."))

    file_count = 0
    for py_file in src_dir.rglob("*.py"):
        if py_file.parent.name == "__pycache__":
            continue
        file_count += 1
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.level and node.module and node.module.startswith("gapfill"):
                    found = False
                    for candidate in [
                        src_dir / f"{node.module.replace('.', '/')}.py",
                        src_dir / f"{node.module.replace('.', '/')}" / "__init__.py",
                    ]:
                        if candidate.exists():
                            found = True
                            break
                    if not found:
                        rel_file = py_file.relative_to(src_dir)
                        issues.append(Issue(
                            "warning",
                            "死引用",
                            f"{rel_file}: 从 '{node.module}' 导入，但模块不存在"
                        ))

    return issues, file_count


def check_permissions(project_path):
    """Check settings templates for dangerous permissions."""
    issues = []
    templates_dir = project_path / "src" / "gapfill" / "templates"

    if not templates_dir.exists():
        return issues

    settings_file = templates_dir / "settings.json"
    if not settings_file.exists():
        return issues

    content = settings_file.read_text(encoding="utf-8")
    for perm in HIGH_RISK_PERMISSIONS:
        if perm in content:
            issues.append(Issue(
                "error",
                "危险权限",
                f"settings.json 包含危险权限: {perm}"
            ))

    return issues


def check_stale_content(project_path):
    """Check for stale project names and deprecated references."""
    issues = []
    src_dir = project_path / "src" / "gapfill"

    if not src_dir.exists():
        return issues

    for py_file in sorted(src_dir.rglob("*.py")):
        if py_file.parent.name == "__pycache__":
            continue
        if py_file.name == "review.py":
            continue
        try:
            content = py_file.read_text(encoding="utf-8")
        except Exception:
            continue
        for pattern in STALE_PATTERNS:
            if pattern.lower() in content.lower():
                rel_file = py_file.relative_to(src_dir.parent)
                issues.append(Issue(
                    "warning",
                    "过期内容",
                    f"{rel_file}: 包含旧项目名 '{pattern}'"
                ))

    return issues


def check_json_syntax(project_path):
    """Validate all *.json files parse correctly."""
    issues = []
    count = 0
    src_dir = project_path / "src"

    if not src_dir.exists():
        return issues, count

    for json_file in sorted(src_dir.rglob("*.json")):
        if json_file.parent.name == "__pycache__":
            continue
        count += 1
        try:
            json.loads(json_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            rel_file = json_file.relative_to(src_dir.parent)
            issues.append(Issue(
                "error",
                "JSON 语法",
                f"{rel_file}: {e.msg} (第 {e.lineno} 行)"
            ))

    return issues, count


def check_scripts_syntax(project_path):
    """Validate scripts/*.py parse without syntax errors."""
    issues = []
    count = 0
    scripts_dir = project_path / "scripts"

    if not scripts_dir.exists():
        return issues, count

    for py_file in sorted(scripts_dir.glob("*.py")):
        count += 1
        try:
            ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError as e:
            rel_file = py_file.relative_to(project_path)
            issues.append(Issue(
                "error",
                "脚本语法",
                f"{rel_file}: 语法错误 (第 {e.lineno} 行)"
            ))

    return issues, count


def check_sensitive_files(project_path):
    """Check that sensitive files are covered by .gitignore."""
    issues = []
    gitignore = project_path / ".gitignore"

    if not gitignore.exists():
        return issues

    ignored = _parse_gitignore(gitignore)

    for pattern in SENSITIVE_FILE_PATTERNS:
        if pattern not in ignored:
            issues.append(Issue(
                "warning",
                "敏感文件忽略",
                f".gitignore 未忽略常见敏感文件名: {pattern}"
            ))

    return issues


def _parse_gitignore(path):
    """Parse .gitignore and return set of ignored patterns."""
    patterns = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            patterns.add(line)
            # Also add basename
            if "/" in line:
                patterns.add(line.lstrip("/"))
    return patterns


def _print_report(issues, checks_run, files_scanned):
    if not issues:
        print(f"审查通过，扫描 {files_scanned} 个文件，{len(checks_run)} 项检查 ✓")
        return

    for issue in issues:
        icon = "❌" if issue.severity == "error" else "⚠️"
        print(f"{icon} {issue.category}: {issue.message}")

    error_count = sum(1 for i in issues if i.severity == "error")
    warn_count = sum(1 for i in issues if i.severity == "warning")
    parts = []
    if error_count:
        parts.append(f"{error_count} 个错误")
    if warn_count:
        parts.append(f"{warn_count} 个警告")
    print(f"\n共发现 {len(issues)} 个问题 ({', '.join(parts)})")
    print(f"已执行 {len(checks_run)} 项检查，扫描 {files_scanned} 个文件")
