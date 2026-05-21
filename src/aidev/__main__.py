"""aidev CLI 入口"""

import argparse
import sys

from aidev import __version__
from aidev.commands.init import init_command


def main():
    parser = argparse.ArgumentParser(
        prog="aidev",
        description="AI 开发者的通用工具箱",
    )
    parser.add_argument("--version", action="version", version=f"aidev {__version__}")

    subparsers = parser.add_subparsers(dest="command", help="可用子命令")

    # init 子命令
    init_parser = subparsers.add_parser("init", help="初始化新项目")
    init_parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")
    init_parser.add_argument("--public", action="store_true", help="创建公开仓库（默认私有）")
    init_parser.add_argument(
        "--platform",
        choices=["github", "gitee", "gitlab"],
        default="github",
        help="Git 平台（默认 github）",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        init_command(args)


if __name__ == "__main__":
    main()
