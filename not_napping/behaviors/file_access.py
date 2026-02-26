"""Create, read, touch, and delete files in ~/.not_napping/scratch/."""

import os
import random
import time
from pathlib import Path
from datetime import datetime

from .base import BaseBehavior

SCRATCH_DIR = Path.home() / ".not_napping" / "scratch"
MAX_FILES = 20


def _ensure_scratch_dir():
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)


def _list_scratch_files():
    """Return scratch files sorted by modification time (oldest first)."""
    if not SCRATCH_DIR.exists():
        return []
    files = [f for f in SCRATCH_DIR.iterdir() if f.is_file()]
    files.sort(key=lambda f: f.stat().st_mtime)
    return files


def _timestamp_name():
    return f"scratch_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{random.randint(100, 999)}.txt"


class FileAccessBehavior(BaseBehavior):
    name = "file_access"

    def perform(self):
        _ensure_scratch_dir()
        existing = _list_scratch_files()

        # Enforce cap: delete oldest files if at limit
        while len(existing) >= MAX_FILES:
            oldest = existing.pop(0)
            oldest.unlink(missing_ok=True)

        roll = random.random()

        if roll < 0.40:
            # Touch an existing file or create an empty one
            if existing and random.random() < 0.6:
                target = random.choice(existing)
                target.touch()
                return f"file: touched {target.name}"
            else:
                name = _timestamp_name()
                path = SCRATCH_DIR / name
                path.touch()
                return f"file: touched (new) {name}"

        elif roll < 0.65:
            # Create a file with some content
            name = _timestamp_name()
            path = SCRATCH_DIR / name
            lines = [
                f"# Scratch file created at {datetime.now().isoformat()}",
                "",
                "Meeting notes:",
                f"- Action item {random.randint(1, 50)}: follow up on project status",
                f"- Review document version {random.randint(1, 20)}",
                f"- Schedule sync for next {'Monday Tuesday Wednesday Thursday Friday'.split()[random.randint(0, 4)]}",
                "",
            ]
            path.write_text("\n".join(lines))
            return f"file: created {name}"

        elif roll < 0.90:
            # Read an existing file
            if existing:
                target = random.choice(existing)
                try:
                    _ = target.read_text()
                except (OSError, UnicodeDecodeError):
                    pass
                return f"file: read {target.name}"
            else:
                # Nothing to read; create instead
                name = _timestamp_name()
                (SCRATCH_DIR / name).touch()
                return f"file: created (fallback) {name}"

        else:
            # Delete a file
            if existing:
                target = random.choice(existing)
                target.unlink(missing_ok=True)
                return f"file: deleted {target.name}"
            return "file: nothing to delete"
