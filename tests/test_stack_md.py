"""Tests for stack-md subcommand."""

import io
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "stack_md.py"


def run_stack_md(tmp_path, args=None):
    """Run stack-md command with UTF-8 encoding fix for Windows."""
    cmd = [sys.executable, str(SCRIPT_PATH), str(tmp_path)]
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


class TestStackMdCommand:
    def test_creates_claude_md_with_generic(self, tmp_path):
        """Test that stack-md creates CLAUDE.md with generic template."""
        result = run_stack_md(tmp_path, ["--stack", "generic"])
        assert result.returncode == 0
        assert (tmp_path / "CLAUDE.md").exists()
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "Development Principles" in content

    def test_creates_spring_boot_template(self, tmp_path):
        """Test that stack-md creates Spring Boot CLAUDE.md."""
        result = run_stack_md(tmp_path, ["--stack", "spring-boot"])
        assert result.returncode == 0
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "Spring Boot" in content
        assert "Anti-Patterns" in content

    def test_creates_react_template(self, tmp_path):
        """Test that stack-md creates React CLAUDE.md."""
        result = run_stack_md(tmp_path, ["--stack", "react"])
        assert result.returncode == 0
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "React" in content
        assert "Anti-Patterns" in content

    def test_existing_claude_md_generates_suggestion(self, tmp_path):
        """Test that existing CLAUDE.md generates gapfill-suggestions.md."""
        # Create existing CLAUDE.md
        (tmp_path / "CLAUDE.md").write_text("# Existing\n", encoding="utf-8")
        result = run_stack_md(tmp_path, ["--stack", "spring-boot"])
        assert result.returncode == 0
        assert (tmp_path / "CLAUDE.md").read_text(encoding="utf-8") == "# Existing\n"
        assert (tmp_path / ".claude" / "gapfill-suggestions.md").exists()
        suggestion = (tmp_path / ".claude" / "gapfill-suggestions.md").read_text(encoding="utf-8")
        assert "Spring Boot" in suggestion

    def test_invalid_stack_returns_error(self, tmp_path):
        """Test that invalid stack name returns error."""
        result = run_stack_md(tmp_path, ["--stack", "invalid"])
        assert result.returncode == 1
        assert "错误" in result.stdout_data

    def test_default_stack_is_generic(self, tmp_path):
        """Test that no --stack flag defaults to generic."""
        result = run_stack_md(tmp_path)
        assert result.returncode == 0
        content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
        assert "Development Principles" in content

    def test_template_has_no_sensitive_info(self, tmp_path):
        """Test that templates do not contain sensitive information."""
        import re
        for stack in ["generic", "spring-boot", "react"]:
            result = run_stack_md(tmp_path, ["--stack", stack])
            assert result.returncode == 0
            content = (tmp_path / "CLAUDE.md").read_text(encoding="utf-8")
            # Check for actual sensitive patterns, not just the word "secrets"
            # which legitimately appears in security rule instructions.
            # Patterns: key=value assignments, hardcoded passwords/tokens,
            # or placeholder values like "sk-xxx", "AKIA...", "ghp_..."
            assert not re.search(r'(?:password|token|api_key|secret)\s*[:=]\s*["\'][^"\']', content, re.IGNORECASE)
            assert not re.search(r'(?:sk-[a-zA-Z0-9]|AKIA|ghp_|xox[bposr]-)', content)
