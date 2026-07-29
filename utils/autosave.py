"""
autosave.py
-----------
A tiny wrapper around Kivy's Clock that calls a save callback every
`interval` seconds. Kept separate from EditorScreen so the timer's
start/stop logic is easy to reason about and reuse.
"""

from kivy.clock import Clock


class AutoSaveManager:
    """Periodically invokes a save callback while the app is running."""

    def __init__(self, save_callback, interval=30):
        self.save_callback = save_callback
        self.interval = interval
        self._event = None

    def start(self):
        """Start (or restart) the autosave timer."""
        self.stop()
        self._event = Clock.schedule_interval(self._tick, self.interval)

    def _tick(self, dt):
        self.save_callback()

    def stop(self):
        """Cancel the autosave timer if it is running."""
        if self._event:
            self._event.cancel()
            self._event = None
