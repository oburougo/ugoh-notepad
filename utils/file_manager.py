"""
file_manager.py
----------------
Handles all disk I/O: opening files, saving files, and tracking
whether the current buffer has unsaved changes. Keeping this
separate from the UI means it can be unit tested with no Kivy
widgets involved at all.
"""

import os


class FileManager:
    """Handles reading/writing text files and tracking save state."""

    def __init__(self):
        self.current_path = None
        self.saved_text = ""

    @property
    def filename(self):
        """Return just the file name (no folder path) for display."""
        if self.current_path:
            return os.path.basename(self.current_path)
        return "Untitled"

    def new_file(self):
        """Reset state for a brand new, empty document."""
        self.current_path = None
        self.saved_text = ""

    def open_file(self, path):
        """Read a text file from disk and remember it as the active file."""
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        self.current_path = path
        self.saved_text = content
        return content

    def save_file(self, text, path=None):
        """Write `text` to `path` (or the current file if path is None)."""
        target = path or self.current_path
        if not target:
            raise ValueError("No file path specified for saving.")
        with open(target, "w", encoding="utf-8") as f:
            f.write(text)
        self.current_path = target
        self.saved_text = text
        return target

    def has_unsaved_changes(self, current_text):
        """True if the editor's text differs from what's on disk."""
        return current_text != self.saved_text
