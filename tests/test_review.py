"""Tests for review subcommand."""

import io
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve().parent.parent / "scripts" / "review.py"


def run_review(tmp_path, args=None):
    """Run review command with UTF-8 encoding fix for Windows."""
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


class TestReviewCommand:
    def test_clean_project_passes(self, tmp_path):
        """Test that a clean project passes review."""
        # Set up a minimal project structure
        src = tmp_path / "src" / "gapfill"
        src.mkdir(parents=True)
        (src / "__init__.py").write_text('"""gapfill"""\n', encoding="utf-8")
        (src / "commands" / "__init__.py").parent.mkdir(parents=True, exist_ok=True)
        (src / "commands" / "__init__.py").write_text('"""gapfill commands"""\n', encoding="utf-8")

        result = run_review(tmp_path)
        assert result.returncode == 0
        assert "审查通过" in result.stdout_data

    def test_detects_dangerous_permissions(self, tmp_path):
        """Test that dangerous permissions are detected."""
        templates = tmp_path / "src" / "gapfill" / "templates"
        templates.mkdir(parents=True)
        (templates / "settings.json").write_text(
            '{"permissions": {"allow": ["Write(/**)", "Edit(/**)", "Bash(curl:*)"]}}',
            encoding="utf-8"
        )

        result = run_review(tmp_path)
        assert result.returncode == 1
        assert "危险权限" in result.stdout_data
        assert "Write(/**)" in result.stdout_data

    def test_detects_stale_content(self, tmp_path):
        """Test that old project names are detected."""
        src = tmp_path / "src" / "gapfill" / "commands"
        src.mkdir(parents=True)
        (src / "__init__.py").write_text('"""aidev 子命令包"""\n', encoding="utf-8")

        result = run_review(tmp_path)
        assert result.returncode == 0  # warning doesn't fail
        assert "过期内容" in result.stdout_data
        assert "aidev" in result.stdout_data

    def test_detects_copy_inconsistency(self, tmp_path):
        """Test that src/ vs skills/src/ inconsistencies are detected."""
        # Create src with one content
        src = tmp_path / "src" / "gapfill"
        src.mkdir(parents=True)
        (src / "__init__.py").write_text('"""gapfill v1"""\n', encoding="utf-8")

        # Create skills/src with different content
        skills = tmp_path / "skills" / "gapfill" / "src" / "gapfill"
        skills.mkdir(parents=True)
        (skills / "__init__.py").write_text('"""gapfill v2"""\n', encoding="utf-8")

        result = run_review(tmp_path)
        assert result.returncode == 1
        assert "副本不一致" in result.stdout_data

    def test_detects_missing_copy(self, tmp_path):
        """Test that files missing from skills/ are detected."""
        src = tmp_path / "src" / "gapfill"
        src.mkdir(parents=True)
        (src / "__init__.py").write_text('"""gapfill"""\n', encoding="utf-8")
        (src / "new_module.py").write_text('# new\n', encoding="utf-8")

        skills = tmp_path / "skills" / "gapfill" / "src" / "gapfill"
        skills.mkdir(parents=True)
        (skills / "__init__.py").write_text('"""gapfill"""\n', encoding="utf-8")

        result = run_review(tmp_path)
        assert result.returncode == 1
        assert "副本缺失" in result.stdout_data

    def test_invalid_path_returns_error(self, tmp_path):
        """Test that non-existent path returns error."""
        result = run_review(tmp_path / "nonexistent")
        assert result.returncode == 1
        assert "错误" in result.stdout_data

    def test_no_false_positives_on_clean_project(self):
        """Test review on the actual gapfill project - should pass."""
        project_root = SCRIPT_PATH.parent.parent
        result = run_review(project_root)
        assert result.returncode == 0
        assert "审查通过" in result.stdout_data
