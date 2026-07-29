"""
text_utils.py
-------------
Pure text-processing helpers: word/char/line counting, reading time
estimation, and find/replace logic. None of this touches Kivy, so it
can be tested with plain `python -m unittest` (see tests/ folder
described in the README).
"""

import re


class TextStats:
    """Static helpers for computing statistics and searching text."""

    @staticmethod
    def word_count(text):
        words = re.findall(r"\S+", text)
        return len(words)

    @staticmethod
    def char_count(text):
        return len(text)

    @staticmethod
    def line_count(text):
        if text == "":
            return 1
        return text.count("\n") + 1

    @staticmethod
    def reading_time_minutes(text, wpm=200):
        """Estimate reading time assuming `wpm` words per minute."""
        words = TextStats.word_count(text)
        return max(words / wpm, 0.0)

    @staticmethod
    def find_all_occurrences(text, query, case_sensitive=False):
        """Return a list of (start, end) index tuples for every match."""
        if not query:
            return []
        haystack = text if case_sensitive else text.lower()
        needle = query if case_sensitive else query.lower()
        positions = []
        start = 0
        while True:
            idx = haystack.find(needle, start)
            if idx == -1:
                break
            positions.append((idx, idx + len(needle)))
            start = idx + 1
        return positions

    @staticmethod
    def replace_all(text, query, replacement, case_sensitive=False):
        """Replace every occurrence of `query` with `replacement`.

        Returns a tuple of (new_text, number_of_replacements_made).
        """
        if not query:
            return text, 0
        if case_sensitive:
            count = text.count(query)
            return text.replace(query, replacement), count
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        count = len(pattern.findall(text))
        return pattern.sub(replacement, text), count
