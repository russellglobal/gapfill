"""init subcommand tests."""

import io
import json
import subprocess
from pathlib import Path

import pytest


def run_gapfill_init(tmp_path, extra_args=None):
    """Run gapfill init and return result."""
    script_path = Path(__file__).resolve().parent.parent / "scripts" / "init.py"
    args = ["python", str(script_path), str(tmp_path)]
    if extra_args:
        args.extend(extra_args)
    proc = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    stdout = io.TextIOWrapper(io.BytesIO(out), encoding="utf-8", errors="replace").read()
    stderr = io.TextIOWrapper(io.BytesIO(err), encoding="utf-8", errors="replace").read()
    proc.stdout_data = stdout
    proc.stderr_data = stderr
    return proc


def test_init_creates_files(tmp_path):
    """init should create all necessary files."""
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0

    assert (tmp_path / ".git").exists()
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "README.md").exists()
    assert (tmp_path / ".claude" / "settings.local.json").exists()
    assert (tmp_path / "env-info.txt").exists()


def test_init_idempotent(tmp_path):
    """Running init twice should not error (idempotent)."""
    run_gapfill_init(tmp_path)
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0


def test_init_settings_has_permissions(tmp_path):
    """settings.local.json should contain preset permissions."""
    run_gapfill_init(tmp_path)
    settings = json.loads(
        (tmp_path / ".claude" / "settings.local.json").read_text()
    )
    assert "permissions" in settings
    assert "allow" in settings["permissions"]
    allow_list = settings["permissions"]["allow"]
    assert any("git" in p for p in allow_list)
    assert any("WebSearch" in p for p in allow_list)


def test_init_env_info_has_tools(tmp_path):
    """env-info.txt should contain tool information."""
    run_gapfill_init(tmp_path)
    content = (tmp_path / "env-info.txt").read_text(encoding="utf-8")
    assert "git" in content.lower()


def test_init_existing_git_repo(tmp_path):
    """Directory with existing git repo, init should only create files."""
    subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True)
    result = run_gapfill_init(tmp_path)
    assert result.returncode == 0
    assert (tmp_path / ".gitignore").exists()
    assert (tmp_path / "README.md").exists()
