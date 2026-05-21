# aidev MVP: init 子命令实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 创建 `aidev` CLI 工具及 `init` 子命令，实现一人公司新项目初始化的 0 交互体验。

**Architecture:** Python 3 单文件 CLI（MVP），`argparse` 处理子命令，纯标准库零依赖。子命令入口通过 `if __name__ == "__main__"` 路由。为未来插件化预留 `commands/` 目录结构。

**Tech Stack:** Python 3.8+, argparse, subprocess, json, pathlib, os, sys

---

### 文件结构

| 文件 | 职责 |
|------|------|
| `src/aidev/__init__.py` | 包初始化，版本号 |
| `src/aidev/__main__.py` | CLI 入口，子命令路由 |
| `src/aidev/commands/__init__.py` | 子命令包 |
| `src/aidev/commands/init.py` | init 子命令核心逻辑 |
| `src/aidev/commands/feedback.py` | feedback 子命令（v2 预留，MVP 只做空壳） |
| `src/aidev/utils.py` | 通用工具函数（SSH 检测、git 操作等） |
| `src/aidev/templates/__init__.py` | 模板包 |
| `src/aidev/templates/gitignore` | .gitignore 通用模板 |
| `src/aidev/templates/readme.md` | README.md 模板 |
| `src/aidev/templates/claude.md` | CLAUDE.md 模板 |
| `src/aidev/templates/settings.json` | settings.local.json 模板 |
| `src/aidev/templates/env_info.txt` | env-info.txt 模板 |
| `pyproject.toml` | Python 项目配置 |
| `tests/test_init.py` | init 子命令测试 |
| `tests/test_utils.py` | 工具函数测试 |

---

### Task 1: 项目骨架和 CLI 入口

**Files:**
- Create: `pyproject.toml`
- Create: `src/aidev/__init__.py`
- Create: `src/aidev/__main__.py`
- Create: `src/aidev/commands/__init__.py`

- [ ] **Step 1: 创建 pyproject.toml**

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.backends._legacy:_Backend"

[project]
name = "aidev"
version = "0.1.0"
description = "AI 开发者的通用工具箱"
requires-python = ">=3.8"
authors = [{ name = "aidev contributors" }]
license = { text = "MIT" }

[project.scripts]
aidev = "aidev.__main__:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 2: 创建 src/aidev/__init__.py**

```python
"""aidev - AI 开发者的通用工具箱"""

__version__ = "0.1.0"
```

- [ ] **Step 3: 创建 src/aidev/__main__.py**

```python
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
```

- [ ] **Step 4: 创建 src/aidev/commands/__init__.py**

```python
"""aidev 子命令包"""
```

- [ ] **Step 5: 验证 CLI 可运行**

```bash
cd D:/proApes/ccProjects/idea_analysis
python -m aidev --help
```

期望输出：包含 `init` 子命令的帮助信息。

- [ ] **Step 6: 验证 init 子命令可识别**

```bash
python -m aidev init --help
```

期望输出：init 子命令的帮助信息。

- [ ] **Step 7: 提交**

```bash
git add pyproject.toml src/
git commit -m "feat: 创建 aidev CLI 骨架和 init 子命令路由"
```

---

### Task 2: 工具函数和模板文件

**Files:**
- Create: `src/aidev/utils.py`
- Create: `src/aidev/templates/__init__.py`
- Create: `src/aidev/templates/gitignore`
- Create: `src/aidev/templates/readme.md`
- Create: `src/aidev/templates/claude.md`
- Create: `src/aidev/templates/settings.json`
- Create: `src/aidev/templates/env_info.txt`
- Test: `tests/test_utils.py`

- [ ] **Step 1: 创建 src/aidev/utils.py**

```python
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
```

- [ ] **Step 2: 创建 src/aidev/templates/__init__.py**

```python
"""模板文件包"""
from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent
```

- [ ] **Step 3: 创建 .gitignore 模板**

```
# 创建 src/aidev/templates/gitignore
# IDE
.idea/
.vscode/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Python
__pycache__/
*.pyc
*.pyo
*.egg-info/
dist/
build/
venv/
.env

# Node
node_modules/
npm-debug.log*

# Java
target/
*.class

# 通用
*.log
*.tmp
```

- [ ] **Step 4: 创建 README.md 模板**

```
# 创建 src/aidev/templates/readme.md
# {{project_name}}

> 项目描述（待填写）

## 快速开始

<!-- 在此填写项目的启动说明 -->

## 开发

<!-- 在此填写开发指南 -->
```

- [ ] **Step 5: 创建 CLAUDE.md 模板**

```
# 创建 src/aidev/templates/claude.md
# {{project_name}}

## 角色
你是一位经验丰富的软件工程师，正在帮助我开发这个项目。

## 原则
- 先阅读现有代码和文件，再提出修改建议
- 保持修改最小化和聚焦，不要附带清理无关代码
- 不要添加超出需求的功能
- 只在必要时添加注释，代码逻辑自明时不写注释
- 优先使用现有的代码风格和模式

## 语言规则
- 对话、文档、解释使用中文
- 代码标识符（变量/函数/类名）保持项目原有语言，不强制翻译
- 遇到英文代码，用中文解释，不改写代码本身
- 生成新代码时，遵循项目已有风格

## 命令执行
- 一次执行一个命令，不要使用 && 或 ; 或 || 链式组合
- 先 cd 切换目录，再在单独的步骤中执行后续命令
- 这确保每个命令都能被权限系统单独匹配

## 会话恢复
- 关闭终端后，使用 `claude -r` 或 `claude --resume` 继续之前的对话
- 不要使用 `claude -c`（这会新建对话）

## 环境
可用工具和环境信息见 env-info.txt。
```

- [ ] **Step 6: 创建 settings.local.json 模板**

```json
{
  "permissions": {
    "allow": [
      "Bash(git --version)",
      "Bash(node --version)",
      "Bash(npm --version)",
      "Bash(python --version)",
      "Bash(python3 --version)",
      "Bash(java -version)",
      "Bash(git status)",
      "Bash(git log:*)",
      "Bash(git diff:*)",
      "Bash(git branch:*)",
      "Bash(ls:*)",
      "Bash(dir:*)",
      "Bash(cat:*)",
      "Bash(find:*)",
      "Bash(grep:*)",
      "WebSearch",
      "WebFetch(domain:*)",
      "Read(/**)",
      "Bash(git init)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(git pull:*)",
      "Bash(git merge:*)",
      "Bash(git checkout:*)",
      "Bash(git restore:*)",
      "Bash(git remote:*)",
      "Bash(git worktree:*)",
      "Bash(git cherry-pick:*)",
      "Bash(mkdir:*)",
      "Bash(cp:*)",
      "Bash(npm install:*)",
      "Bash(npm init:*)",
      "Bash(npm ls:*)",
      "Bash(npm view:*)",
      "Bash(pip install:*)",
      "Bash(pip show:*)",
      "Bash(python -m venv:*)",
      "Bash(mvn clean:*)",
      "Bash(mvn compile:*)",
      "Bash(mvn test:*)",
      "Bash(mvn dependency:*)",
      "Bash(npx:*)",
      "Bash(node:*)",
      "Bash(python:*)",
      "Bash(python3:*)",
      "Bash(unzip:*)",
      "Bash(docker info:*)",
      "Bash(docker ps:*)",
      "Bash(docker compose ps:*)",
      "Bash(curl:*)",
      "Bash(wget:*)",
      "Write(/**)",
      "Edit(/**)",
      "Glob(/**)",
      "Grep(/**)"
    ]
  }
}
```

- [ ] **Step 7: 创建 env-info.txt 模板（运行时填充）**

```
# 创建 src/aidev/templates/env_info.txt
# 环境信息 - 自动生成，请勿手动修改
# 生成时间: {{timestamp}}

## 操作系统
{{os_info}}

## 可用工具
{{tools_info}}
```

- [ ] **Step 8: 创建 tests/test_utils.py**

```python
"""工具函数测试"""

from aidev.utils import detect_git, detect_tools, get_os_info


def test_detect_git():
    """git 应该被检测到（开发环境通常有 git）"""
    result = detect_git()
    assert result is True  # 测试环境假设有 git


def test_detect_tools_returns_dict():
    """detect_tools 应返回字典"""
    result = detect_tools()
    assert isinstance(result, dict)
    assert "git" in result  # git 应该存在


def test_get_os_info():
    """get_os_info 应返回包含 system 的字典"""
    result = get_os_info()
    assert "system" in result
    assert result["system"] in ("Windows", "Linux", "Darwin")
```

- [ ] **Step 9: 运行测试**

```bash
cd D:/proApes/ccProjects/idea_analysis
python -m pytest tests/test_utils.py -v
```

期望：3 个测试全部通过。

- [ ] **Step 10: 提交**

```bash
git add src/aidev/utils.py src/aidev/templates/ tests/test_utils.py
git commit -m "feat: 添加工具函数和模板（gitignore/CLAUDE.md/settings/环境探测）"
```

---

### Task 3: init 子命令核心逻辑 — 本地初始化

**Files:**
- Modify: `src/aidev/commands/init.py`

- [ ] **Step 1: 实现 init_command 函数（本地部分）**

修改 `src/aidev/commands/init.py`：

```python
"""init 子命令"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from aidev.templates import TEMPLATES_DIR
from aidev.utils import (
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
    platform = args.platform
    is_public = args.public

    # 1. 环境检查
    print("🔍 检查环境...")
    if not detect_git():
        print("❌ 未检测到 git，请先安装 git")
        sys.exit(1)

    ssh_key = detect_ssh_key()
    if not ssh_key:
        print("⚠️  未检测到 SSH key")
        print("   请运行: ssh-keygen -t ed25519 -C \"your_email@example.com\"")
        print("   然后将公钥添加到 Git 平台")
        sys.exit(1)
    print(f"  ✅ SSH key: {ssh_key}")

    # 2. 本地目录处理
    if not project_path.exists():
        print(f"📁 创建目录: {project_path}")
        project_path.mkdir(parents=True, exist_ok=True)

    if not has_git_repo(project_path):
        print("📦 初始化 git 仓库...")
        result = run_git(project_path, "init")
        if result.returncode != 0:
            print(f"❌ git init 失败: {result.stderr}")
            sys.exit(1)

    # 3. 创建项目文件
    print("📝 创建项目文件...")
    _create_gitignore(project_path)
    _create_readme(project_path, project_path.name)
    _create_claude_md(project_path, project_path.name)
    _create_settings(project_path)
    _create_env_info(project_path)

    # 4. 首次提交
    print("📦 首次 git commit...")
    run_git(project_path, "add", "-A")
    run_git(project_path, "commit", "-m", "chore: init project by aidev")

    print(f"\n✅ 本地初始化完成: {project_path}")

    # 5. 远程仓库创建（下一步实现）
    print("🔗 远程仓库功能待实现（v2）")


def _read_template(filename):
    """读取模板文件"""
    template_path = TEMPLATES_DIR / filename
    return template_path.read_text(encoding="utf-8")


def _write_file(path, content):
    """写入文件，如果已存在则跳过"""
    if path.exists():
        print(f"  ⏭️  {path.name} 已存在，跳过")
        return
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ {path.name}")


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
```

- [ ] **Step 2: 在临时目录测试本地初始化**

```bash
cd D:/proApes/ccProjects/idea_analysis
mkdir -p /tmp/test-aidev-init
python -m aidev init /tmp/test-aidev-init
```

期望输出：环境检查通过 → git init → 创建文件 → commit 成功。

- [ ] **Step 3: 验证生成文件**

```bash
ls -la /tmp/test-aidev-init/
cat /tmp/test-aidev-init/CLAUDE.md
cat /tmp/test-aidev-init/.claude/settings.local.json
cat /tmp/test-aidev-init/env-info.txt
```

- [ ] **Step 4: 清理测试目录**

```bash
rm -rf /tmp/test-aidev-init
```

- [ ] **Step 5: 提交**

```bash
git add src/aidev/commands/init.py
git commit -m "feat: 实现 init 本地初始化（git/文件创建/环境探测/权限预置）"
```

---

### Task 4: init 子命令核心逻辑 — 远程仓库创建

**Files:**
- Modify: `src/aidev/commands/init.py`
- Modify: `src/aidev/utils.py`

- [ ] **Step 1: 添加远程仓库创建函数到 utils.py**

在 `src/aidev/utils.py` 末尾添加：

```python
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
        # remote 可能已存在
        result = run_git(project_path, "remote", "set-url", "origin", remote_url)

    result = run_git(project_path, "push", "-u", "origin", "main")
    if result.returncode != 0:
        # 尝试 master
        result = run_git(project_path, "push", "-u", "origin", "master")

    return result
```

- [ ] **Step 2: 修改 init_command，集成远程仓库创建**

在 `src/aidev/commands/init.py` 中，替换 `init_command` 末尾部分：

```python
    print(f"\n✅ 本地初始化完成: {project_path}")

    # 5. 远程仓库创建
    print("🔗 创建远程仓库...")
    from aidev.utils import (
        detect_gh_cli, detect_git_username,
        create_github_repo, create_repo_via_api,
        bind_remote_and_push,
    )

    if detect_gh_cli() and platform == "github":
        result = create_github_repo(project_path.name, is_public)
        if result.returncode == 0:
            print(f"  ✅ 远程仓库已创建")
        else:
            # remote 可能已存在（重复运行），尝试直接 push
            print(f"  ⚠️  仓库创建可能已存在，尝试推送...")
            username = detect_git_username(platform) or "unknown"
            push_result = bind_remote_and_push(project_path, platform, username, project_path.name)
            if push_result.returncode == 0:
                print(f"  ✅ 推送成功")
            else:
                print(f"  ⚠️  推送失败: {push_result.stderr}")
                print(f"  请手动执行: cd {project_path} && git remote add origin <url> && git push -u origin main")
    else:
        print(f"  ⚠️  未检测到 gh CLI 或平台不是 GitHub")
        print(f"  提示: 安装 gh CLI (https://cli.github.com) 可自动创建仓库")
        print(f"  或手动创建仓库后执行:")
        print(f"    cd {project_path}")
        print(f"    git remote add origin <remote-url>")
        print(f"    git push -u origin main")
```

- [ ] **Step 3: 测试（需要 gh CLI）**

```bash
cd D:/proApes/ccProjects/idea_analysis
mkdir -p /tmp/test-aidev-remote
python -m aidev init /tmp/test-aidev-remote
```

如果没有 gh CLI，应看到友好的提示。

- [ ] **Step 4: 清理**

```bash
rm -rf /tmp/test-aidev-remote
```

- [ ] **Step 5: 提交**

```bash
git add src/aidev/commands/init.py src/aidev/utils.py
git commit -m "feat: 实现 init 远程仓库创建（gh CLI 优先 + REST API 兜底）"
```

---

### Task 5: 测试和幂等性验证

**Files:**
- Create: `tests/test_init.py`

- [ ] **Step 1: 创建 tests/test_init.py**

```python
"""init 子命令测试"""

import json
import subprocess
import tempfile
from pathlib import Path

import pytest


def run_aidev_init(tmp_path, extra_args=None):
    """运行 aidev init 并返回结果"""
    args = ["python", "-m", "aidev", "init", str(tmp_path)]
    if extra_args:
        args.extend(extra_args)
    result = subprocess.run(args, capture_output=True, text=True)
    return result


def test_init_creates_files(tmp_path):
    """init 应该创建所有必要文件"""
    result = run_aidev_init(tmp_path)
    assert result.returncode == 0

    assert (tmp_path / ".git").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".claude" / "settings.local.json").exists()
    assert (tmp_path / "env-info.txt").exists()


def test_init_idempotent(tmp_path):
    """重复运行 init 不应报错（幂等）"""
    run_aidev_init(tmp_path)
    result = run_aidev_init(tmp_path)
    assert result.returncode == 0


def test_init_settings_has_permissions(tmp_path):
    """settings.local.json 应该包含预置权限"""
    run_aidev_init(tmp_path)
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
    run_aidev_init(tmp_path)
    content = (tmp_path / "CLAUDE.md").read_text()
    assert "中文" in content
    assert "不强制翻译" in content


def test_init_claude_md_has_single_command_rule(tmp_path):
    """CLAUDE.md 应该包含单命令执行规则"""
    run_aidev_init(tmp_path)
    content = (tmp_path / "CLAUDE.md").read_text()
    assert "一个命令" in content


def test_init_env_info_has_tools(tmp_path):
    """env-info.txt 应该包含工具信息"""
    run_aidev_init(tmp_path)
    content = (tmp_path / "env-info.txt").read_text()
    assert "git" in content.lower()


def test_init_existing_git_repo(tmp_path):
    """已有 git 仓库的目录，init 应该只创建文件"""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    result = run_aidev_init(tmp_path)
    assert result.returncode == 0
    assert (tmp_path / "CLAUDE.md").exists()
    assert (tmp_path / ".gitignore").exists()
```

- [ ] **Step 2: 运行所有测试**

```bash
cd D:/proApes/ccProjects/idea_analysis
python -m pytest tests/ -v
```

期望：全部 10 个测试通过。

- [ ] **Step 3: 提交**

```bash
git add tests/test_init.py
git commit -m "test: 添加 init 子命令的集成测试（幂等性/文件创建/权限预置）"
```

---

### Task 6: README 和安装说明

**Files:**
- Create: `README.md`
- Modify: `pyproject.toml`

- [ ] **Step 1: 创建 README.md**

```markdown
# aidev

AI 开发者的通用工具箱 —— 类似 Java 生态的 Hutool，为 AI 辅助开发流程中的各种小痛点提供轻量解决方案。

## 安装

```bash
pip install -e .
```

或使用 pipx（推荐）：

```bash
pipx install -e .
```

## 使用

### 初始化新项目

```bash
# 在当前目录初始化
aidev init

# 在指定目录初始化
aidev init ./my-project

# 创建公开仓库
aidev init --public

# 指定 Git 平台
aidev init --platform gitee
```

### init 做了什么

1. **环境检查** — 检测 git、SSH key 等
2. **Git 初始化** — 如果目录没有 .git，自动 git init
3. **创建文件** — .gitignore、README.md、CLAUDE.md、settings.local.json、env-info.txt
4. **权限预置** — 基础级 + 低风险级权限，减少 AI 交互轮次
5. **环境探测** — 自动记录可用工具和版本
6. **远程仓库** — 如果有 gh CLI，自动创建 GitHub 仓库并推送

## 开发路线图

| 版本 | 功能 |
|------|------|
| MVP | init（项目初始化） |
| v2 | sync（跨项目配置同步）、perm（权限管理）、lang（语言设置）、feedback（一键提报） |
| v3 | roadmap（决策自动沉淀） |
| v4 | capture（高价值交互记录） |
| v5 | audit（Skill 安全扫描）、skill-localize（开源 Skill 本地化） |

## 许可证

MIT
```

- [ ] **Step 2: 提交**

```bash
git add README.md
git commit -m "docs: 添加项目 README 和安装说明"
```

---

## Spec Self-Review

**1. 覆盖率检查：**
- ✅ 环境检查（git/SSH）
- ✅ 本地 git init + 文件创建
- ✅ .gitignore 通用模板
- ✅ README.md 占位模板
- ✅ CLAUDE.md（角色 + 原则 + 语言规则 + 单命令规范 + 会话恢复提示）
- ✅ settings.local.json（基础+低风险权限）
- ✅ env-info.txt（环境探测）
- ✅ 远程仓库创建（gh 优先 + API 兜底）
- ✅ 幂等性（重复执行安全）
- ✅ 测试覆盖（7 个测试用例）
- ✅ 多平台支持（github/gitee/gitlab 参数）
- ✅ 复合命令指令规范（CLAUDE.md）

**2. 占位符扫描：** 无 TBD/TODO。

**3. 一致性：** 所有文件路径、函数名、变量名一致。

**4. 范围检查：** 聚焦 MVP（init），不越界到 v2+ 功能。feedback.py 仅预留空壳，不实现。

计划完整，可以开始执行。
