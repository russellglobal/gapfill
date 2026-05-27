"""Tests for sync subcommand."""

import io
import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "sync.py"


def run_sync(tmp_path, args=None):
    """Run sync command with UTF-8 encoding fix for Windows."""
    cmd = [sys.executable, str(SCRIPT_PATH), str(tmp_path)]
    if args:
        cmd.extend(args)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Wrap stdout/stderr in UTF-8 decoder for Windows
    out, err = proc.communicate()
    stdout = io.TextIOWrapper(io.BytesIO(out), encoding="utf-8", errors="replace").read()
    stderr = io.TextIOWrapper(io.BytesIO(err), encoding="utf-8", errors="replace").read()
    return proc.returncode, stdout, stderr


def _create_mock_project(tmp_path, name, rules):
    """Create a mock project with given permission rules."""
    project = tmp_path / name
    claude_dir = project / ".claude"
    claude_dir.mkdir(parents=True)
    settings = {"permissions": {"allow": rules}}
    (claude_dir / "settings.local.json").write_text(
        json.dumps(settings), encoding="utf-8"
    )
    return project


class TestSyncCommand:
    def test_sync_discovers_projects(self, tmp_path):
        """Test that sync finds all projects with settings.local.json."""
        _create_mock_project(tmp_path, "proj_a", ["Bash(git:*)", "Read(/**)"])
        _create_mock_project(tmp_path, "proj_b", ["Bash(git:*)", "Write(/**)"])

        rc, stdout, _ = run_sync(tmp_path)
        assert rc == 0
        assert "2 个项目" in stdout
        assert "proj_a" in stdout
        assert "proj_b" in stdout

    def test_sync_shows_diff(self, tmp_path):
        """Test that sync shows permission differences."""
        _create_mock_project(tmp_path, "base", ["Bash(git:*)", "Read(/**)"])
        _create_mock_project(tmp_path, "other", ["Bash(git:*)", "Read(/**)", "Write(/**)"])

        rc, stdout, _ = run_sync(tmp_path, ["--base", "base"])
        assert rc == 0
        assert "Write(/**)" in stdout
        assert "+" in stdout

    def test_sync_no_diff_when_identical(self, tmp_path):
        """Test that sync reports no diff when all projects are identical."""
        rules = ["Bash(git:*)", "Read(/**)", "Write(/**)"]
        _create_mock_project(tmp_path, "proj_a", rules)
        _create_mock_project(tmp_path, "proj_b", rules)

        rc, stdout, _ = run_sync(tmp_path)
        assert rc == 0
        assert "完全一致" in stdout

    def test_sync_empty_directory(self, tmp_path):
        """Test sync with no projects found."""
        rc, stdout, _ = run_sync(tmp_path)
        assert rc == 0
        assert "Claude Code" in stdout

    def test_sync_invalid_directory(self, tmp_path):
        """Test sync with non-existent directory."""
        rc, stdout, _ = run_sync(tmp_path / "nonexistent")
        assert rc == 1
        assert "错误" in stdout

    def test_sync_outputs_json(self, tmp_path):
        """Test that sync outputs valid JSON for Claude processing."""
        _create_mock_project(tmp_path, "base", ["Bash(git:*)"])
        _create_mock_project(tmp_path, "other", ["Bash(git:*)", "Bash(docker:*)"])

        rc, stdout, _ = run_sync(tmp_path, ["--base", "base"])
        # Extract JSON from output
        start = stdout.index("=== JSON")
        end = stdout.index("=== 结束 ===")
        json_str = stdout[start:end].split("\n", 1)[1].strip()
        data = json.loads(json_str)
        assert "additions" in data
        assert "removals" in data
        assert "base_project" in data
