#!/usr/bin/env python
"""gapfill stack-claude-md - Generate tech-stack-specific CLAUDE.md (called by skill)"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from skill directory without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SRC_DIR = SKILL_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.stack_claude_md import stack_claude_md_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill stack-claude-md",
        description="AI developer's universal toolkit - Generate tech-stack-specific CLAUDE.md",
    )
    parser.add_argument("--stack", "-s", default=None, help="Tech stack name (generic/spring-boot/react)")
    parser.add_argument("path", nargs="?", default=".", help="Project directory (default: current directory)")

    args = parser.parse_args()
    stack_claude_md_command(args)


if __name__ == "__main__":
    main()
