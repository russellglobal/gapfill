"""gapfill CLI 入口"""

import argparse
import sys

from gapfill import __version__
from gapfill.commands.init import init_command
from gapfill.commands.sync import sync_command
from gapfill.commands.stack_md import stack_md_command
from gapfill.commands.review import review_command
from gapfill.commands.scan import scan_command


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

    # sync 子命令
    sync_parser = subparsers.add_parser("sync", help="跨项目权限规则同步")
    sync_parser.add_argument("root", nargs="?", default=None, help="扫描根目录（默认父目录）")
    sync_parser.add_argument("--base", "-b", default=None, help="基准项目名称（默认自动检测）")

    # stack-md 子命令
    stack_parser = subparsers.add_parser("stack-md", help="生成技术栈专属 CLAUDE.md")
    stack_parser.add_argument("--stack", "-s", default=None, help="技术栈名称 (generic/spring-boot/react)")
    stack_parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    # review 子命令
    review_parser = subparsers.add_parser("review", help="提交前全局审查")
    review_parser.add_argument("path", nargs="?", default=".", help="项目路径（默认当前目录）")

    # scan 子命令
    scan_parser = subparsers.add_parser("scan", help="settings 合规扫描")
    scan_parser.add_argument("path", nargs="?", default=".", help="扫描目录（默认当前目录）")

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        init_command(args)
    elif args.command == "sync":
        sync_command(args)
    elif args.command == "stack-md":
        stack_md_command(args)
    elif args.command == "review":
        review_command(args)
    elif args.command == "scan":
        scan_command(args)


if __name__ == "__main__":
    main()
