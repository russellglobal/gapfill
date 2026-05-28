#!/usr/bin/env python
"""gapfill init - Project initialization script (called by skill)"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from skill directory without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SRC_DIR = SKILL_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.init import init_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill init",
        description="AI developer's universal toolkit - Project initialization",
    )
    parser.add_argument("path", nargs="?", default=".", help="Project directory (default: current directory)")
    parser.add_argument("--lang", default="en", help="Language: en (default), zh")
    parser.add_argument("--stack", default=None, help="Tech stack: generic, spring-boot, react")

    args = parser.parse_args()
    init_command(args)


if __name__ == "__main__":
    main()
