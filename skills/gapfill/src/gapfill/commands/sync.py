"""sync subcommand - Cross-project permission comparison."""

import json
import sys
from pathlib import Path

from gapfill.utils import fix_windows_encoding

fix_windows_encoding()

from gapfill.utils import scan_projects, merge_permissions, compute_diff


def sync_command(args):
    """Execute the sync subcommand."""
    root_dir = Path(args.root).resolve() if args.root else Path.cwd().parent
    base_name = args.base

    if not root_dir.exists():
        print(f"错误: 目录不存在: {root_dir}")
        sys.exit(1)

    # 1. Scan projects
    projects = scan_projects(root_dir)
    if not projects:
        print(f"未在 {root_dir} 下找到任何 Claude Code 项目")
        print("项目需要包含 .claude/settings.local.json 文件")
        sys.exit(0)

    # 2. Merge permissions
    merge_result = merge_permissions(projects)
    by_project = merge_result["by_project"]

    # 3. Determine base project
    if not base_name:
        # Auto-detect: use the project closest to cwd
        cwd = Path.cwd().resolve()
        for project_path, _ in projects:
            if cwd == project_path or str(cwd).startswith(str(project_path)):
                base_name = project_path.name
                break
        if not base_name:
            # Fallback: use first project
            base_name = list(by_project.keys())[0]

    if base_name not in by_project:
        available = ", ".join(by_project.keys())
        print(f"错误: 项目 '{base_name}' 不在扫描范围内")
        print(f"可用项目: {available}")
        sys.exit(1)

    # 4. Print project summary
    print(f"扫描到 {len(projects)} 个项目:")
    for project_path, settings in projects:
        name = project_path.name
        count = len(settings.get("permissions", {}).get("allow", []))
        marker = " <-- 基准" if name == base_name else ""
        print(f"  {name}: {count} 条规则{marker}")

    # 5. Compute and display diff
    diff = compute_diff(base_name, merge_result)

    if not diff["additions"] and not diff["removals"]:
        print(f"\n{base_name} 的权限规则与其他项目完全一致")
        return

    print(f"\n对比基准: {base_name}")

    if diff["additions"]:
        print(f"\n新增规则 ({len(diff['additions'])}):")
        for rule, sources in diff["additions"]:
            source_str = ", ".join(sources)
            print(f"  + {rule}     [来源: {source_str}]")

    if diff["removals"]:
        print(f"\n多余规则 ({len(diff['removals'])}):")
        for rule in diff["removals"]:
            print(f"  - {rule}")

    # 6. Interactive selection (output JSON for Claude to process)
    print(f"\n=== JSON 输出 (供 Claude 处理) ===")
    output = {
        "base_project": base_name,
        "additions": [{"rule": r, "sources": s} for r, s in diff["additions"]],
        "removals": diff["removals"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    print("=== 结束 ===")
    print(f"\n请告诉我哪些规则要同步，我会输出更新后的 settings.local.json 内容。")
