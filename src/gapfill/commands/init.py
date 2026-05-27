"""init subcommand"""

import sys
from datetime import datetime, timezone
from pathlib import Path

from gapfill.utils import fix_windows_encoding

fix_windows_encoding()

from gapfill.templates import TEMPLATES_DIR
from gapfill.utils import (
    detect_git,
    detect_ssh_key,
    get_os_info,
    detect_tools,
    has_git_repo,
    run_git,
)
from gapfill.constants import VALID_STACKS, VALID_LANGS


def init_command(args):
    """Execute the init subcommand."""
    project_path = Path(args.path).resolve()

    # 1. Environment check
    print("检查环境...")
    _check_env()

    # 2. Directory setup
    if not project_path.exists():
        print(f"创建目录: {project_path}")
        project_path.mkdir(parents=True, exist_ok=True)

    if not has_git_repo(project_path):
        print("初始化 git 仓库...")
        result = run_git(project_path, "init")
        if result.returncode != 0:
            print(f"git init 失败: {result.stderr}")
            sys.exit(1)

    # 3. Scaffold files
    print("创建项目文件...")
    _create_gitignore(project_path)
    _create_readme(project_path, project_path.name)
    _create_settings(project_path)

    # 4. Generate CLAUDE.md if --stack specified
    if getattr(args, "stack", None):
        lang = getattr(args, "lang", "en")
        _create_claude_md(project_path, args.stack, lang)

    # 5. Generate env-info.txt
    lang = getattr(args, "lang", "en")
    _create_env_info(project_path, lang)

    # 6. Initial commit (only for empty repos)
    _do_commit(project_path)

    print(f"\n本地初始化完成: {project_path}")


def _do_commit(project_path):
    """Commit scaffolded files. Auto-commit only for empty repos (no existing commits)."""
    has_commits = _has_existing_commits(project_path)

    if has_commits:
        print("已有 git 提交历史，跳过自动 commit")
        print("请手动执行: git add -A && git commit -m 'chore: init project by gapfill'")
        return

    print("首次 git commit...")
    add_result = run_git(project_path, "add", "-A")
    if add_result.returncode != 0:
        print(f"git add 失败: {add_result.stderr}")
        sys.exit(1)
    commit_result = run_git(project_path, "commit", "-m", "chore: init project by gapfill")
    if commit_result.returncode != 0:
        print(f"git commit 失败: {commit_result.stderr}")
        print("如果文件都已存在，可能无需提交")


def _has_existing_commits(project_path):
    """Check if the git repo has any existing commits."""
    result = run_git(project_path, "rev-list", "--count", "HEAD")
    if result.returncode != 0:
        return False  # fresh repo, no commits yet
    try:
        count = int(result.stdout.strip())
        return count > 0
    except (ValueError, IndexError):
        return False


def _do_commit(project_path):
    """Commit scaffolded files. Auto-commit only for empty repos (no existing commits)."""
    has_commits = _has_existing_commits(project_path)

    if has_commits:
        print("已有 git 提交历史，跳过自动 commit")
        print("请手动执行: git add -A && git commit -m 'chore: init project by gapfill'")
        return

    print("首次 git commit...")
    add_result = run_git(project_path, "add", "-A")
    if add_result.returncode != 0:
        print(f"git add 失败: {add_result.stderr}")
        sys.exit(1)
    commit_result = run_git(project_path, "commit", "-m", "chore: init project by gapfill")
    if commit_result.returncode != 0:
        print(f"git commit 失败: {commit_result.stderr}")
        print("如果文件都已存在，可能无需提交")


def _has_existing_commits(project_path):
    """Check if the git repo has any existing commits."""
    result = run_git(project_path, "rev-list", "--count", "HEAD")
    if result.returncode != 0:
        return False  # fresh repo, no commits yet
    try:
        count = int(result.stdout.strip())
        return count > 0
    except (ValueError, IndexError):
        return False


def _do_commit(project_path):
    """Commit scaffolded files. Auto-commit only for empty repos (no existing commits)."""
    has_commits = _has_existing_commits(project_path)

    if has_commits:
        print("已有 git 提交历史，跳过自动 commit")
        print("请手动执行: git add -A && git commit -m 'chore: init project by gapfill'")
        return

    print("首次 git commit...")
    add_result = run_git(project_path, "add", "-A")
    if add_result.returncode != 0:
        print(f"git add 失败: {add_result.stderr}")
        sys.exit(1)
    commit_result = run_git(project_path, "commit", "-m", "chore: init project by gapfill")
    if commit_result.returncode != 0:
        print(f"git commit 失败: {commit_result.stderr}")
        print("如果文件都已存在，可能无需提交")


def _has_existing_commits(project_path):
    """Check if the git repo has any existing commits."""
    result = run_git(project_path, "rev-list", "--count", "HEAD")
    if result.returncode != 0:
        return False  # fresh repo, no commits yet
    try:
        count = int(result.stdout.strip())
        return count > 0
    except (ValueError, IndexError):
        return False


def _check_env():
    """Check environment prerequisites."""
    if not detect_git():
        print("未检测到 git，请先安装 git")
        sys.exit(1)
    print("  git: 已安装")

    ssh_key = detect_ssh_key()
    if ssh_key:
        print(f"  SSH key: {ssh_key}")
    else:
        print("  SSH key: 未检测到（如需推送远程仓库请先配置）")


def _read_template(filename):
    """Read a template file."""
    template_path = TEMPLATES_DIR / filename
    return template_path.read_text(encoding="utf-8")


def _write_file(path, content):
    """Write file content, skip if already exists."""
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


def _create_settings(project_path):
    content = _read_template("settings.json")
    claude_dir = project_path / ".claude"
    claude_dir.mkdir(exist_ok=True)
    settings_path = claude_dir / "settings.local.json"

    if not settings_path.exists():
        settings_path.write_text(content, encoding="utf-8")
        print("  settings.local.json")
        return

    # File exists — ask for confirmation
    print("[CONFIRM] settings.local.json 已存在，是否用 gapfill 预设模板替换？(yes/no)")
    if sys.stdin.isatty():
        try:
            answer = input().strip().lower()
            if answer in ("yes", "y"):
                settings_path.write_text(content, encoding="utf-8")
                print("  settings.local.json (已替换)")
            else:
                print("  已保留现有 settings.local.json")
        except EOFError:
            print("  已保留现有 settings.local.json")
    else:
        # Non-interactive: default to skip
        print("  非交互模式，已保留现有 settings.local.json")


def _create_env_info(project_path, lang="en"):
    if lang == "zh":
        template = _read_template("env_info_zh.txt")
    else:
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


def _create_claude_md(project_path, stack, lang="en"):
    """Generate CLAUDE.md from a tech stack template during init."""
    if stack not in VALID_STACKS:
        print(f"警告: 不支持的技术栈 '{stack}'，跳过 CLAUDE.md 生成")
        return
    if lang not in VALID_LANGS:
        print(f"警告: 不支持的语言 '{lang}'，使用默认英文")
        lang = "en"
    template_name = f"claude-{stack}" if lang == "en" else f"claude-{stack}-{lang}"
    template = _read_template(f"{template_name}.md")
    content = template.replace("{{project_name}}", project_path.name)
    _write_file(project_path / "CLAUDE.md", content)
