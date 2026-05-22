"""init 子命令"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

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
    platform_name = args.platform
    is_public = args.public

    # 1. 环境检查 + 缺失组件安装
    print("检查环境...")
    _check_and_install(platform_name)

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

    # 5. 远程仓库创建 + 推送
    _create_remote_repo(project_path, platform_name, is_public)


def _check_and_install(platform_name):
    """环境检查 + 缺失组件安装提示"""
    from gapfill.utils import detect_git, detect_ssh_key, detect_gh_cli

    # git 是必须的
    if not detect_git():
        print("未检测到 git，请先安装 git")
        sys.exit(1)
    print("  git: 已安装")

    # SSH key 是必须的（用于认证）
    ssh_key = detect_ssh_key()
    if not ssh_key:
        print("  未检测到 SSH key")
        print("  正在自动创建 SSH key (ed25519)...")
        _generate_ssh_key()
        ssh_key = detect_ssh_key()
        if ssh_key:
            print(f"  SSH key 已创建: {ssh_key}")
            _print_ssh_setup_guide()
        else:
            print("  SSH key 创建失败，请手动运行: ssh-keygen -t ed25519")
            sys.exit(1)
    else:
        print(f"  SSH key: {ssh_key}")

    # gh CLI 非必须，但影响远程仓库创建
    if platform_name == "github":
        if detect_gh_cli():
            print("  gh CLI: 已安装")
        else:
            print("  gh CLI: 未安装（可选，用于自动创建远程仓库）")
            print("  建议安装。安装命令（任选其一）：")
            print("    Windows: winget install --id GitHub.cli")
            print("    Mac:     brew install gh")
            print("    Linux:   sudo snap install gh")
            print("  安装后运行: gh auth login")
            print("  跳过此步不影响本地初始化。")


def _generate_ssh_key():
    """自动生成 SSH key"""
    import subprocess
    result = subprocess.run(
        ["ssh-keygen", "-t", "ed25519", "-C", "gapfill-generated-key",
         "-f", str(Path.home() / ".ssh" / "id_ed25519"), "-N", "", "-q"],
        capture_output=True, text=True, timeout=30
    )
    return result.returncode == 0


def _print_ssh_setup_guide():
    """打印 SSH key 配置指南"""
    pub_key_path = Path.home() / ".ssh" / "id_ed25519.pub"
    try:
        pub_key = pub_key_path.read_text().strip()
    except Exception:
        pub_key = "（请读取 ~/.ssh/id_ed25519.pub 内容）"

    print("\n  ⚠️  首次使用需要将公钥添加到 Git 平台：")
    print("    GitHub:  https://github.com/settings/ssh/new")
    print("    Gitee:   https://gitee.com/profile/ssh_keys")
    print("    GitLab:  https://gitlab.com/-/profile/keys")
    print(f"  公钥: {pub_key}\n")


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


def _create_remote_repo(project_path, platform_name, is_public):
    """创建远程仓库并推送"""
    if platform_name != "github":
        print(f"  平台 {platform_name} 暂不支持自动创建")
        return

    from gapfill.utils import (
        detect_gh_cli, detect_git_username,
        create_github_repo, bind_remote_and_push,
    )

    if not detect_gh_cli():
        print("  gh CLI 未安装，无法创建远程仓库")
        return

    print("创建远程仓库...")
    result = create_github_repo(project_path.name, is_public)
    if result.returncode == 0:
        print(f"  远程仓库已创建")
    else:
        print(f"  仓库可能已存在，尝试推送...")
        username = detect_git_username(platform_name) or "unknown"
        push_result = bind_remote_and_push(project_path, platform_name, username, project_path.name)
        if push_result.returncode == 0:
            print(f"  推送成功")
        else:
            print(f"  推送失败: {push_result.stderr}")
