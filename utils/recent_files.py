"""
recent_files.py
----------------
Persists the last 10 opened/saved files to a small JSON file inside
the data/ folder, so the list survives restarting the app.
"""

import json
import os

# data/ lives one level above utils/, i.e. UgohNotepad/data/
DATA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
)
RECENT_FILE_PATH = os.path.join(DATA_DIR, "recent_files.json")
MAX_RECENT = 10


class RecentFilesManager:
    """Tracks the most recently opened/saved file paths."""

    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self.files = self._load()

    def _load(self):
        if os.path.exists(RECENT_FILE_PATH):
            try:
                with open(RECENT_FILE_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save(self):
        try:
            with open(RECENT_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.files, f, indent=2)
        except IOError:
            pass  # Non-fatal: recent files list is a convenience, not critical

    def add(self, path):
        """Push `path` to the front of the list, capped at MAX_RECENT."""
        if path in self.files:
            self.files.remove(path)
        self.files.insert(0, path)
        self.files = self.files[:MAX_RECENT]
        self._save()

    def get_all(self):
        """Return recent files that still exist on disk."""
        return [p for p in self.files if os.path.exists(p)]
