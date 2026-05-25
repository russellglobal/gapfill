#!/usr/bin/env python
"""gapfill scan - settings 合规扫描（开发用）"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.scan import scan_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill scan",
        description="溜缝儿 - settings 合规扫描",
    )
    parser.add_argument("path", nargs="?", default=".", help="扫描目录（默认当前目录）")

    args = parser.parse_args()
    scan_command(args)


if __name__ == "__main__":
    main()
