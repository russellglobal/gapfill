#!/usr/bin/env python
"""gapfill review - 提交前全局审查（开发用）"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from project root without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.review import review_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill review",
        description="溜缝儿 - 提交前全局审查",
    )
    parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    args = parser.parse_args()
    review_command(args)


if __name__ == "__main__":
    main()
