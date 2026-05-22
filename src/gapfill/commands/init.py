"""init 子命令"""

import io
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Windows 中文控制台编码修复
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

from gapfill.templates import TEMPLATES_DIR
from gapfill.utils import (
    detect_git,
    detect_ssh_key,
    get_os_info,
    detect_tools,
    has_git_repo,
    run_git,
)


def init_command(args):
    """执行 init 子命令"""
    project_path = Path(args.path).resolve()

    # 1. 环境检查
    print("检查环境...")
    _check_env()

    # 2. 本地目录处理
    if not project_path.exists():
        print(f"创建目录: {project_path}")
        project_path.mkdir(parents=True, exist_ok=True)

    if not has_git_repo(project_path):
        print("初始化 git 仓库...")
        result = run_git(project_path, "init")
        if result.returncode != 0:
            print(f"git init 失败: {result.stderr}")
            sys.exit(1)

    # 3. 创建项目文件
    print("创建项目文件...")
    _create_gitignore(project_path)
    _create_readme(project_path, project_path.name)
    _create_claude_md(project_path, project_path.name)
    _create_settings(project_path)
    _create_env_info(project_path)

    # 4. 首次提交
    print("首次 git commit...")
    run_git(project_path, "add", "-A")
    run_git(project_path, "commit", "-m", "chore: init project by gapfill")

    print(f"\n本地初始化完成: {project_path}")


def _check_env():
    """环境检查"""
    # git 是必须的
    if not detect_git():
        print("未检测到 git，请先安装 git")
        sys.exit(1)
    print("  git: 已安装")

    # 检查 SSH key
    ssh_key = detect_ssh_key()
    if ssh_key:
        print(f"  SSH key: {ssh_key}")
    else:
        print("  SSH key: 未检测到（如需推送远程仓库请先配置）")


def _read_template(filename):
    """读取模板文件"""
    template_path = TEMPLATES_DIR / filename
    return template_path.read_text(encoding="utf-8")


def _write_file(path, content):
    """写入文件，如果已存在则跳过"""
    if path.exists():
        print(f"  {path.name} 已存在，跳过")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  {path.name}")


def _create_gitignore(project_path):
    content = _read_template("gitignore")
    _write_file(project_path / ".gitignore", content)


def _create_readme(project_path, project_name):
    content = _read_template("readme.md").replace("{{project_name}}", project_name)
    _write_file(project_path / "README.md", content)


def _create_claude_md(project_path, project_name):
    content = _read_template("claude.md").replace("{{project_name}}", project_name)
    _write_file(project_path / "CLAUDE.md", content)


def _create_settings(project_path):
    content = _read_template("settings.json")
    claude_dir = project_path / ".claude"
    claude_dir.mkdir(exist_ok=True)
    _write_file(claude_dir / "settings.local.json", content)


def _create_env_info(project_path):
    template = _read_template("env_info.txt")
    os_info = get_os_info()
    tools_info = detect_tools()

    os_text = "\n".join(f"- {k}: {v}" for k, v in os_info.items())
    tools_text = "\n".join(f"- {k}: {v}" for k, v in tools_info.items())

    content = (
        template.replace("{{timestamp}}", datetime.now(timezone.utc).isoformat())
        .replace("{{os_info}}", os_text)
        .replace("{{tools_info}}", tools_text)
    )
    _write_file(project_path / "env-info.txt", content)
