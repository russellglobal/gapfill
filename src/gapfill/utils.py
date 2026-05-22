"""Utility functions."""

import os
import platform
import shutil
import subprocess
from pathlib import Path


def detect_git():
    """Check if git is available."""
    return shutil.which("git") is not None


def detect_ssh_key():
    """Check if an SSH key exists. Returns the key path or None."""
    ssh_dir = Path.home() / ".ssh"
    for key_name in ["id_ed25519", "id_rsa"]:
        key_path = ssh_dir / key_name
        if key_path.exists():
            return str(key_path)
    return None


def detect_tools():
    """Probe available development tools and their versions."""
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
                results[name] = "Detection failed"
    return results


def get_os_info():
    """Get operating system information."""
    return {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "python_version": platform.python_version(),
    }


def run_git(cwd, *args):
    """Run a git command in the specified directory."""
    result = subprocess.run(
        ["git"] + list(args),
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    return result


def has_git_repo(path):
    """Check if a directory has a git repository."""
    return (Path(path) / ".git").exists()
