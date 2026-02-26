"""Markov-chain typing with variable speed, typos, and corrections."""

import random
import time

import pyautogui

from .base import BaseBehavior
from ..timing import typing_delay, thinking_pause, jitter
from ..text.markov import get_generator

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


class TypingBehavior(BaseBehavior):
    name = "typing"

    def __init__(self):
        self.generator = get_generator()

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
