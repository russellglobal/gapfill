#!/usr/bin/env python
"""gapfill sync - Cross-project permission sync (for development)"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from project root without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.sync import sync_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill sync",
        description="溜缝儿 - 跨项目权限规则同步",
    )
    parser.add_argument("root", nargs="?", default=None, help="扫描根目录（默认父目录）")
    parser.add_argument("--base", "-b", default=None, help="基准项目名称（默认自动检测）")

    args = parser.parse_args()
    sync_command(args)


if __name__ == "__main__":
    main()
