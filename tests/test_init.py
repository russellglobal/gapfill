"""init 子命令测试"""

import json
import subprocess
from pathlib import Path

import pytest


def run_gapfill_init(tmp_path, extra_args=None):
    """运行 gapfill init 并返回结果"""
    # 通过 scripts/init.py 运行（与 skill 调用方式一致）
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "init.py"
    args = ["python", str(script_path), str(tmp_path)]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(args, capture_output=True, text=True)
    return result


def test_init_creates_files(tmp_path):
    """init 应该创建所有必要文件"""
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0

    assert (tmp_path / ".git").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "settings.local.json").exists()
    assert (tmp_path / "env-info.txt").exists()


def test_init_idempotent(tmp_path):
    """重复运行 init 不应报错（幂等）"""
    run_gapfill_init(tmp_path)
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0


def test_init_settings_has_permissions(tmp_path):
    """settings.local.json 应该包含预置权限"""
    run_gapfill_init(tmp_path)
    settings = json.loads(
        (tmp_path / ".claude" / "settings.local.json").read_text()
    )
    assert "permissions" in settings
    assert "allow" in settings["permissions"]
    allow_list = settings["permissions"]["allow"]
    assert any("git" in p for p in allow_list)
    assert any("WebSearch" in p for p in allow_list)


def test_init_claude_md_has_chinese_rules(tmp_path):
    """CLAUDE.md 应该包含中文语言规则"""
    run_gapfill_init(tmp_path)
    content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "中文" in content
    assert "不强制翻译" in content


def test_init_claude_md_has_single_command_rule(tmp_path):
    """CLAUDE.md 应该包含单命令执行规则"""
    run_gapfill_init(tmp_path)
    content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
    assert "一个命令" in content


def test_init_env_info_has_tools(tmp_path):
    """env-info.txt 应该包含工具信息"""
    run_gapfill_init(tmp_path)
    content = (tmp_path / "env-info.txt").read_text(encoding="utf-8")
    assert "git" in content.lower()


def test_init_existing_git_repo(tmp_path):
    """已有 git 仓库的目录，init 应该只创建文件"""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".gitignore").exists()
