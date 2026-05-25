# -*- coding: utf-8 -*-
"""Tests for scan subcommand."""

import io
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "scan.py"


def run_scan(path, args=None):
    """Run scan command with UTF-8 encoding fix for Windows."""
    cmd = [sys.executable, str(SCRIPT_PATH), str(path)]
    if args:
        cmd.extend(args)
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    stdout = io.TextIOWrapper(io.BytesIO(out), encoding="utf-8", errors="replace").read()
    stderr = io.TextIOWrapper(io.BytesIO(err), encoding="utf-8", errors="replace").read()
    proc.stdout_data = stdout
    proc.stderr_data = stderr
    return proc


class TestScanCommand:
    def test_clean_project_passes(self, tmp_path):
        """Test that clean settings passes scan."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": ["Bash(git status)", "Read(/**)"]}}),
            encoding="utf-8"
        )

        result = run_scan(tmp_path)
        assert result.returncode == 0
        assert "through" in result.stdout_data.lower() or "pass" in result.stdout_data.lower() or "\u901a\u8fc7" in result.stdout_data  # "通过"

    def test_detects_high_risk_permissions(self, tmp_path):
        """Test that high-risk permissions are detected."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": [
                "Bash(git status)",
                "Write(/**)",
                "Bash(curl:*)",
            ]}}),
            encoding="utf-8"
        )

        result = run_scan(tmp_path)
        assert result.returncode == 1
        assert "Write(/**)" in result.stdout_data

    def test_detects_low_risk_permissions(self, tmp_path):
        """Test that low-risk permissions trigger warning."""
        claude_dir = tmp_path / ".claude"
        claude_dir.mkdir()
        (claude_dir / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": [
                "Bash(git status)",
                "Bash(pip install:*)",
                "Bash(find:*)",
            ]}}),
            encoding="utf-8"
        )

        result = run_scan(tmp_path)
        assert result.returncode == 0  # warning doesn't fail
        assert "Bash(find:*)" in result.stdout_data

    def test_no_projects_found(self, tmp_path):
        """Test that empty directory shows helpful message."""
        result = run_scan(tmp_path)
        assert result.returncode == 0
        assert "settings.local.json" in result.stdout_data

    def test_invalid_path_returns_error(self, tmp_path):
        """Test that non-existent path returns error."""
        result = run_scan(tmp_path / "nonexistent")
        assert result.returncode == 1
        assert "error" in result.stdout_data.lower() or "\u9519\u8bef" in result.stdout_data  # "错误"

    def test_multiple_projects(self, tmp_path):
        """Test scanning multiple projects in one directory."""
        # Project A - clean
        a = tmp_path / "project-a"
        (a / ".claude").mkdir(parents=True)
        (a / ".claude" / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": ["Bash(git status)"]}}),
            encoding="utf-8"
        )

        # Project B - has high risk
        b = tmp_path / "project-b"
        (b / ".claude").mkdir(parents=True)
        (b / ".claude" / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": ["Write(/**)"]}}),
            encoding="utf-8"
        )

        # Project C - has low risk
        c = tmp_path / "project-c"
        (c / ".claude").mkdir(parents=True)
        (c / ".claude" / "settings.local.json").write_text(
            json.dumps({"permissions": {"allow": ["Bash(find:*)"]}}),
            encoding="utf-8"
        )

        result = run_scan(tmp_path)
        assert result.returncode == 1
        assert "project-a" in result.stdout_data
        assert "project-b" in result.stdout_data
        assert "project-c" in result.stdout_data
        assert "Write(/**)" in result.stdout_data
