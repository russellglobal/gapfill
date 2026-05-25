"""review subcommand - Pre-commit project health check."""

import ast
import sys
from dataclasses import dataclass
from pathlib import Path

from gapfill.utils import fix_windows_encoding

fix_windows_encoding()

DANGEROUS_PERMISSIONS = [
    "Write(/**)",
    "Edit(/**)",
    "Bash(curl:*)",
    "Bash(wget:*)",
    "WebFetch(domain:*)",
    "Bash(find:*)",
    "Bash(npx:*)",
    "Bash(node:*)",
    "Bash(python:*)",
    "Bash(python3:*)",
]

STALE_PATTERNS = [
    "aidev",  # old project name
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
    issues.extend(check_copy_consistency(project_path))
    issues.extend(check_imports(project_path))
    issues.extend(check_permissions(project_path))
    issues.extend(check_stale_content(project_path))

    _print_report(issues)

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

    # Files only in src/
    for rel_path in sorted(src_files - skills_files):
        issues.append(Issue(
            "error",
            "副本缺失",
            f"{rel_path} 存在于 src/ 但不存在于 skills/src/"
        ))

    # Files only in skills/
    for rel_path in sorted(skills_files - src_files):
        issues.append(Issue(
            "warning",
            "副本多余",
            f"{rel_path} 存在于 skills/src/ 但不存在于 src/"
        ))

    # Content differences
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
        return issues

    # Build a map of available modules
    available = set()
    for f in src_dir.rglob("*.py"):
        if f.name == "__init__.py":
            mod_path = f.relative_to(src_dir.parent).parent
            available.add(str(mod_path).replace("/", "."))
        else:
            mod_path = f.relative_to(src_dir.parent).with_suffix("")
            available.add(str(mod_path).replace("/", "."))

    # Check each Python file
    for py_file in src_dir.rglob("*.py"):
        if py_file.parent.name == "__pycache__":
            continue
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"))
        except SyntaxError:
            continue

        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                if node.level and node.module and node.module.startswith("gapfill"):
                    # Convert gapfill.xxx to path
                    mod_name = node.module.replace(".", "/")
                    # Check if it exists as a package (dir with __init__.py) or module (.py)
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

    return issues


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
    for perm in DANGEROUS_PERMISSIONS:
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
        # Skip review.py itself - it legitimately contains stale patterns as data
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


def _print_report(issues):
    if not issues:
        print("审查通过，未发现问题 ✓")
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
