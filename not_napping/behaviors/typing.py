"""Markov-chain typing with variable speed, typos, and corrections."""

import random
import subprocess
import time
from pathlib import Path

import pyautogui

from .base import BaseBehavior
from ..timing import typing_delay, thinking_pause, jitter
from ..text.markov import get_generator
from ..platform_check import IS_MACOS, IS_WINDOWS, IS_LINUX

pyautogui.PAUSE = 0

# Adjacent keys on QWERTY for typo simulation
ADJACENT_KEYS = {
    "a": "sqwz", "b": "vghn", "c": "xdfv", "d": "sfecx", "e": "wrds",
    "f": "dgrtcv", "g": "fhtyb", "h": "gjyubn", "i": "uojk", "j": "hkunm",
    "k": "jloi", "l": "kop", "m": "njk", "n": "bhjm", "o": "iplk",
    "p": "ol", "q": "wa", "r": "etdf", "s": "awedxz", "t": "rfgy",
    "u": "yhji", "v": "cfgb", "w": "qase", "x": "zsdc", "y": "tghu",
    "z": "asx",
}


SCRATCH_DIR = Path.home() / ".not_napping" / "scratch"
TYPING_PAD = SCRATCH_DIR / "typing_pad.txt"


class TypingBehavior(BaseBehavior):
    name = "typing"

    def __init__(self):
        self.generator = get_generator()
        self._editor_proc = None
        self._open_editor()

    def _open_editor(self):
        """Create the typing pad file and open it in the platform's text editor."""
        SCRATCH_DIR.mkdir(parents=True, exist_ok=True)
        TYPING_PAD.write_text("")

        if IS_MACOS:
            subprocess.Popen(["open", "-a", "TextEdit", str(TYPING_PAD)])
        elif IS_WINDOWS:
            self._editor_proc = subprocess.Popen(["notepad", str(TYPING_PAD)])
        elif IS_LINUX:
            subprocess.Popen(["xdg-open", str(TYPING_PAD)])

    def _focus_editor(self):
        """Bring the editor window to the front before typing."""
        if IS_MACOS:
            subprocess.Popen(["open", "-a", "TextEdit", str(TYPING_PAD)])
        elif IS_WINDOWS:
            subprocess.Popen([
                "powershell", "-command",
                '(New-Object -ComObject WScript.Shell).AppActivate("typing_pad")',
            ])
        elif IS_LINUX:
            subprocess.Popen(["xdg-open", str(TYPING_PAD)])
        # Give the OS a moment to bring the window forward
        time.sleep(0.5)

    def _type_char(self, char):
        """Type a single character with realistic delay."""
        pyautogui.press(char) if len(char) == 1 and char.isalnum() else pyautogui.typewrite(char, interval=0)
        time.sleep(typing_delay())

    def _make_typo(self, char):
        """Type wrong adjacent key, pause, backspace, retype correct key."""
        lower = char.lower()
        if lower in ADJACENT_KEYS:
            wrong = random.choice(ADJACENT_KEYS[lower])
            pyautogui.press(wrong)
            time.sleep(jitter(0.15))
            pyautogui.press("backspace")
            time.sleep(jitter(0.1))
            pyautogui.press(char)
            time.sleep(typing_delay())
            return True
        return False

    def _select_back_and_retype(self, text_so_far):
        """Select back a few words and retype them (~8% chance per perform)."""
        words = text_so_far.split()
        if len(words) < 3:
            return
        num_words = random.randint(1, min(3, len(words) - 1))
        chars_to_select = len(" ".join(words[-num_words:]))

        # Select backwards
        for _ in range(chars_to_select):
            pyautogui.hotkey("shift", "left")
            time.sleep(jitter(0.01))

        time.sleep(jitter(0.2))
        # Delete selection
        pyautogui.press("backspace")
        time.sleep(jitter(0.15))

        # Retype the words
        retype = " ".join(words[-num_words:])
        for ch in retype:
            pyautogui.press(ch) if ch != " " else pyautogui.press("space")
            time.sleep(typing_delay())

    def perform(self):
        self._focus_editor()

        # Generate a short burst of text (5-20 words)
        num_words = random.randint(5, 20)
        text = self.generator.generate(num_words)
        words = text.split()[:num_words]

        typed_so_far = []
        for i, word in enumerate(words):
            # Thinking pause at word boundaries (~5% chance)
            if i > 0 and random.random() < 0.05:
                time.sleep(thinking_pause())

            for char in word:
                # ~3% chance of typo per character
                if random.random() < 0.03:
                    if not self._make_typo(char):
                        pyautogui.press(char)
                        time.sleep(typing_delay())
                else:
                    pyautogui.press(char)
                    time.sleep(typing_delay())

            # Space after word (except last)
            if i < len(words) - 1:
                pyautogui.press("space")
                time.sleep(typing_delay())

            typed_so_far.append(word)

        # ~8% chance: select back and retype
        if random.random() < 0.08:
            full_text = " ".join(typed_so_far)
            self._select_back_and_retype(full_text)

        word_count = len(words)
        return f"typed {word_count} words"
