#!/usr/bin/env python
"""gapfill stack-claude-md - Generate tech-stack-specific CLAUDE.md (for development)"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from project root without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.stack_claude_md import stack_claude_md_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill stack-claude-md",
        description="溜缝儿 - 生成技术栈专属 CLAUDE.md",
    )
    parser.add_argument("--stack", "-s", default=None, help="技术栈名称 (generic/spring-boot/react)")
    parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    args = parser.parse_args()
    stack_claude_md_command(args)


if __name__ == "__main__":
    main()
