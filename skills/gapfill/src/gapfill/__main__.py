"""gapfill CLI 入口"""

import argparse
import sys

from gapfill import __version__
from gapfill.commands.init import init_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill",
        description="溜缝儿 - AI 开发者的通用工具箱",
    )
    parser.add_argument("--version", action="version", version=f"gapfill {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # init 子命令
    init_parser = subparsers.add_parser("init", help="初始化新项目")
    init_parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        init_command(args)


if __name__ == "__main__":
    main()
