"""stack-claude-md subcommand - Generate tech-stack-specific CLAUDE.md."""

import sys
from pathlib import Path

from gapfill.utils import fix_windows_encoding

fix_windows_encoding()

from gapfill.templates import TEMPLATES_DIR
from gapfill.constants import VALID_STACKS, VALID_LANGS


def stack_claude_md_command(args):
    """Execute the stack-claude-md subcommand."""
    project_path = Path(args.path).resolve()
    stack = args.stack or "generic"
    lang = getattr(args, "lang", "en")

    if stack not in VALID_STACKS:
        available = ", ".join(sorted(VALID_STACKS))
        print(f"错误: 不支持的技术栈 '{stack}'")
        print(f"可用技术栈: {available}")
        sys.exit(1)

    if lang not in VALID_LANGS:
        print(f"错误: 不支持的语言 '{lang}'")
        print(f"可用语言: en, zh")
        sys.exit(1)

    # Read template
    template_name = f"claude-{stack}" if lang == "en" else f"claude-{stack}-{lang}"
    template_file = TEMPLATES_DIR / f"{template_name}.md"
    if not template_file.exists():
        print(f"错误: 模板文件不存在: {template_name}.md")
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
