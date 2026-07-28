"""
app.py
------
Defines the root Kivy App class for Ugoh Notepad.

This class is responsible for:
- Building the widget tree (via a ScreenManager)
- Wiring up global keyboard shortcuts
- Wiring up the "are you sure you want to exit" warning
- Holding shared managers (theme, recent files) that other
  widgets can reach through App.get_running_app()
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

from ui.screens.editor_screen import EditorScreen
from ui.themes.theme_manager import ThemeManager
from utils.recent_files import RecentFilesManager


class UgohNotepadApp(App):
    """Main application class for Ugoh Notepad."""

    title = "Ugoh Notepad"

    def build(self):
        # Shared managers, reachable anywhere via App.get_running_app()
        self.theme_manager = ThemeManager()
        self.recent_files_manager = RecentFilesManager()

        self.sm = ScreenManager()
        self.editor_screen = EditorScreen(name="editor")
        self.sm.add_widget(self.editor_screen)

        # Desktop window close button -> ask about unsaved changes first
        Window.bind(on_request_close=self.on_request_close)

        # Global keyboard shortcuts (Ctrl+N, Ctrl+S, etc.)
        Window.bind(on_key_down=self._on_keyboard_down)

        # Apply the default (light) theme on startup
        self.theme_manager.apply_theme(self.editor_screen, dark=False)

        return self.sm

    def on_request_close(self, *args, **kwargs):
        """
        Called when the user clicks the window's [X] button (desktop only).
        Returning True blocks the close so we can show a confirmation popup.
        """
        editor = self.editor_screen
        if editor.file_manager.has_unsaved_changes(editor.text_editor.text):
            editor.show_exit_confirmation()
            return True  # Block the close; the popup decides what happens next
        return False  # No unsaved changes, allow the app to close normally

    def _on_keyboard_down(self, window, key, scancode, codepoint, modifier, *args):
        """Forward every key press to the active screen's shortcut handler."""
        return self.editor_screen.handle_shortcut(key, modifier)

    def on_stop(self):
        """Called right before the app process exits. Stop background timers."""
        if hasattr(self, "editor_screen"):
            self.editor_screen.stop_autosave()
