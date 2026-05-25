#!/usr/bin/env python
"""gapfill sync - Cross-project permission sync (called by skill)"""

import argparse
import sys
from pathlib import Path

# Add src/ to Python path (supports running from skill directory without pip install)
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
SRC_DIR = SKILL_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gapfill.commands.sync import sync_command


def main():
    parser = argparse.ArgumentParser(
        prog="gapfill sync",
        description="AI developer's universal toolkit - Cross-project permission sync",
    )
    parser.add_argument("root", nargs="?", default=None, help="Scan root directory (default: parent directory)")
    parser.add_argument("--base", "-b", default=None, help="Base project name (default: auto-detect)")

    args = parser.parse_args()
    sync_command(args)


if __name__ == "__main__":
    main()
