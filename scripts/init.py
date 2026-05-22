#!/usr/bin/env python
"""gapfill init - 项目初始化脚本（由 skill 调用，不对外发布）"""

import argparse
import sys
from pathlib import Path

# 添加 src 到 Python 路径（支持直接运行，无需 pip install）
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.init import init_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill init",
        description="溜缝儿 - 项目初始化",
    )
    parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    args = parser.parse_args()
    init_command(args)


if __name__ == "__main__":
    main()
