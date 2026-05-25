"""Utility functions."""

import json
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


def scan_projects(root_dir):
    """Scan a directory tree for projects with .claude/settings.local.json.

    Returns a list of (project_path, settings_dict) tuples.
    """
    root = Path(root_dir).resolve()
    projects = []
    if not root.exists():
        return projects

    for settings_file in root.rglob(".claude/settings.local.json"):
        project_path = settings_file.parent.parent
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                settings = json.load(f)
            projects.append((project_path, settings))
        except (json.JSONDecodeError, OSError):
            # Skip projects with invalid or unreadable settings files
            continue

    return projects


def merge_permissions(projects):
    """Merge permissions.allow rules from multiple projects.

    Args:
        projects: List of (project_path, settings_dict) tuples

    Returns:
        dict with keys:
            'all_rules': set of all unique rules
            'by_project': dict mapping project name to its rules set
            'merged': sorted list of all unique rules
    """
    by_project = {}
    all_rules = set()

    for project_path, settings in projects:
        name = project_path.name
        rules = set(settings.get("permissions", {}).get("allow", []))
        by_project[name] = rules
        all_rules |= rules

    return {
        "all_rules": all_rules,
        "by_project": by_project,
        "merged": sorted(all_rules),
    }


def compute_diff(base_name, merge_result):
    """Compute permission differences between base project and others.

    Args:
        base_name: Name of the base project to compare against
        merge_result: Result from merge_permissions()

    Returns:
        dict with keys:
            'additions': list of (rule, source_projects) for rules not in base
            'removals': list of rules only in base but not in any other project
    """
    by_project = merge_result["by_project"]
    if base_name not in by_project:
        return {"additions": [], "removals": []}

    base_rules = by_project[base_name]
    other_rules = set()
    for name, rules in by_project.items():
        if name != base_name:
            other_rules |= rules

    additions = []
    for rule in sorted(other_rules - base_rules):
        sources = [
            name for name, rules in by_project.items()
            if name != base_name and rule in rules
        ]
        additions.append((rule, sources))

    # Removals: rules only in base, not in any other project
    removals = sorted(base_rules - other_rules)

    return {"additions": additions, "removals": removals}
