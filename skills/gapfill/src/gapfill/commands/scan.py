"""scan subcommand - Scan projects for dangerous permissions in settings."""

import json
import sys
from pathlib import Path

from gapfill.utils import fix_windows_encoding, scan_projects

fix_windows_encoding()

from gapfill.commands.review import HIGH_RISK_PERMISSIONS, LOW_RISK_PERMISSIONS


def scan_command(args):
    """Execute the scan subcommand."""
    root = Path(args.path).resolve()

    if not root.exists():
        print(f"错误: 目录不存在: {root}")
        sys.exit(1)

    projects = scan_projects(root)
    if not projects:
        print(f"未在 {root} 下找到包含 settings.local.json 的项目")
        return

    results = []
    for project_path, settings in projects:
        rules = settings.get("permissions", {}).get("allow", [])
        high = [r for r in rules if r in HIGH_RISK_PERMISSIONS]
        low = [r for r in rules if r in LOW_RISK_PERMISSIONS]
        results.append((project_path, rules, high, low))

    _print_report(results)

    # Exit 1 if any project has high-risk permissions
    if any(high for _, _, high, _ in results):
        sys.exit(1)


def _print_report(results):
    total = len(results)
    clean = 0
    error = 0
    warning = 0
    other = 0

    for project_path, rules, high, low in results:
        name = project_path.name
        rule_count = len(rules)

        if high and low:
            status = "error"
            error += 1
            icon = "❌"
            print(f"{icon} {name}: {len(high)} 个高危权限, {len(low)} 个低风险权限 ({rule_count} 条规则)")
            for r in high:
                print(f"   - {r}")
            for r in low:
                print(f"   - {r}")
        elif high:
            status = "error"
            error += 1
            icon = "❌"
            print(f"{icon} {name}: {len(high)} 个高危权限 ({rule_count} 条规则)")
            for r in high:
                print(f"   - {r}")
        elif low:
            status = "warning"
            warning += 1
            icon = "⚠️"
            print(f"{icon} {name}: {len(low)} 个低风险权限 ({rule_count} 条规则)")
            for r in low:
                print(f"   - {r}")
        else:
            clean += 1
            icon = "✅"
            print(f"{icon} {name}: 通过 ({rule_count} 条规则)")

    # Summary
    other = total - clean - error - warning
    print(f"\n共 {total} 个项目: {clean} 个通过", end="")
    if error:
        print(f", {error} 个不合规", end="")
    if warning:
        print(f", {warning} 个低风险", end="")
    if other:
        print(f", {other} 个其他", end="")
    print()
