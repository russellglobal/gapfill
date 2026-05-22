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


def detect_git_username(platform_name="github"):
    """从 git config 获取用户名，或从 SSH URL 推断"""
    result = subprocess.run(
        ["git", "config", "--global", "user.name"],
        capture_output=True, text=True,
    )
    if result.returncode == 0 and result.stdout.strip():
        return result.stdout.strip()
    return None


def create_github_repo(repo_name, is_public=False):
    """使用 gh CLI 创建 GitHub 仓库"""
    cmd = ["gh", "repo", "create", repo_name]
    if is_public:
        cmd.append("--public")
    else:
        cmd.append("--private")
    cmd.extend(["--source", ".", "--remote", "origin", "--push"])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result


def create_repo_via_api(platform_name, repo_name, is_public, token=None):
    """通过 REST API 创建仓库（当 gh 不可用时）"""
    import urllib.request
    import json as _json

    if platform_name == "github":
        url = "https://api.github.com/user/repos"
        if not token:
            return None, "需要 GitHub Personal Access Token"
    elif platform_name == "gitee":
        url = "https://gitee.com/api/v5/user/repos"
        if not token:
            return None, "需要 Gitee API Token"
    elif platform_name == "gitlab":
        url = "https://gitlab.com/api/v4/projects"
        if not token:
            return None, "需要 GitLab Personal Access Token"
    else:
        return None, f"不支持的平台: {platform_name}"

    data = {"name": repo_name, "private": not is_public}
    if platform_name == "gitlab":
        data = {"name": repo_name, "visibility": "private" if not is_public else "public"}

    body = _json.dumps(data).encode()
    req = urllib.request.Request(
        url, data=body, method="POST",
        headers={"Content-Type": "application/json"}
    )
    if token:
        if platform_name == "gitee":
            req.add_header("Authorization", f"Bearer {token}")
        elif platform_name == "gitlab":
            req.add_header("PRIVATE-TOKEN", token)
        else:
            req.add_header("Authorization", f"Bearer {token}")

    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, None
    except Exception as e:
        return None, str(e)


def bind_remote_and_push(project_path, platform_name, username, repo_name):
    """绑定 remote 并 push"""
    remote_url = get_platform_remote_url(platform_name, username, repo_name)
    result = run_git(project_path, "remote", "add", "origin", remote_url)
    if result.returncode != 0:
        result = run_git(project_path, "remote", "set-url", "origin", remote_url)

    result = run_git(project_path, "push", "-u", "origin", "main")
    if result.returncode != 0:
        result = run_git(project_path, "push", "-u", "origin", "master")

    return result
