"""通用工具函数"""

import os
import platform
import shutil
import subprocess
from pathlib import Path


def detect_git():
    """检测 git 是否可用"""
    return shutil.which("git") is not None


def detect_ssh_key():
    """检测 SSH key 是否存在，返回 key 路径或 None"""
    ssh_dir = Path.home() / ".ssh"
    for key_name in ["id_ed25519", "id_rsa"]:
        key_path = ssh_dir / key_name
        if key_path.exists():
            return str(key_path)
    return None


def detect_gh_cli():
    """检测 gh CLI 是否可用"""
    return shutil.which("gh") is not None


def detect_tools():
    """探测环境中可用的开发工具及其版本"""
    tools = {
        "python": ["python", "--version"],
        "python3": ["python3", "--version"],
        "node": ["node", "--version"],
        "npm": ["npm", "--version"],
        "git": ["git", "--version"],
        "java": ["java", "-version"],
        "mvn": ["mvn", "--version"],
        "docker": ["docker", "--version"],
        "pip": ["pip", "--version"],
        "pip3": ["pip3", "--version"],
        "gh": ["gh", "--version"],
    }
    results = {}
    for name, cmd in tools.items():
        if shutil.which(cmd[0]):
            try:
                output = subprocess.run(
                    cmd, capture_output=True, text=True, timeout=5
                )
                version = (output.stdout or output.stderr).strip().split("\n")[0]
                results[name] = version
            except Exception:
                results[name] = "检测失败"
    return results


def get_os_info():
    """获取操作系统信息"""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }


def run_git(cwd, *args):
    """在指定目录运行 git 命令"""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def has_git_repo(path):
    """检查目录是否已有 git 仓库"""
    return (Path(path) / ".git").exists()


def get_platform_remote_url(platform_name, username, repo_name):
    """生成 remote URL"""
    if platform_name == "gitee":
        return f"git@gitee.com:{username}/{repo_name}.git"
    elif platform_name == "gitlab":
        return f"git@gitlab.com:{username}/{repo_name}.git"
    return f"git@github.com:{username}/{repo_name}.git"
