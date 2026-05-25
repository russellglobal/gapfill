"""stack-md subcommand - Generate tech-stack-specific CLAUDE.md."""

import io
import sys
from pathlib import Path

# Fix Chinese encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from gapfill.templates import TEMPLATES_DIR

VALID_STACKS = {"generic", "spring-boot", "react"}


def stack_md_command(args):
    """Execute the stack-md subcommand."""
    project_path = Path(args.path).resolve()
    stack = args.stack or "generic"

    if stack not in VALID_STACKS:
        available = ", ".join(sorted(VALID_STACKS))
        print(f"错误: 不支持的技术栈 '{stack}'")
        print(f"可用技术栈: {available}")
        sys.exit(1)

    # Read template
    template_file = TEMPLATES_DIR / f"claude-{stack}.md"
    if not template_file.exists():
        print(f"错误: 模板文件不存在: claude-{stack}.md")
        sys.exit(1)

    content = template_file.read_text(encoding="utf-8")
    content = content.replace("{{project_name}}", project_path.name)

    # Check if CLAUDE.md already exists
    claude_md = project_path / "CLAUDE.md"
    if claude_md.exists():
        # Generate suggestion file instead
        claude_dir = project_path / ".claude"
        claude_dir.mkdir(exist_ok=True)
        suggestion_file = claude_dir / "gapfill-suggestions.md"
        suggestion_file.write_text(content, encoding="utf-8")
        print(f"CLAUDE.md 已存在，建议内容已写入 {suggestion_file}")
    else:
        claude_md.write_text(content, encoding="utf-8")
        line_count = len(content.splitlines())
        print(f"CLAUDE.md 已创建 ({line_count} 行)")
