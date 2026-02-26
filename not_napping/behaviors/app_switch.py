"""Cmd-Tab / Alt-Tab window switching."""

import random
import time

import pyautogui

from .base import BaseBehavior
from ..timing import jitter
from ..platform_check import get_modifier_key, IS_MACOS

pyautogui.PAUSE = 0


class AppSwitchBehavior(BaseBehavior):
    name = "app_switch"

    def __init__(self):
        self.modifier = get_modifier_key()

    def perform(self):
        roll = random.random()

        if roll < 0.70:
            # Single Cmd/Alt-Tab
            pyautogui.hotkey(self.modifier, "tab")
            time.sleep(jitter(0.3))
            return "app-switch: single tab"

        elif roll < 0.90:
            # Hold modifier, tab 2-4 times (browsing windows)
            num_tabs = random.randint(2, 4)
            pyautogui.keyDown(self.modifier)
            time.sleep(jitter(0.1))
            for i in range(num_tabs):
                pyautogui.press("tab")
                time.sleep(jitter(random.uniform(0.3, 0.8)))
            pyautogui.keyUp(self.modifier)
            time.sleep(jitter(0.2))
            return f"app-switch: browsed {num_tabs} windows"

        else:
            # Mission control / show desktop then click back
            if IS_MACOS:
                # Mission Control: Ctrl+Up
                pyautogui.hotkey("ctrl", "up")
                time.sleep(jitter(random.uniform(1.0, 2.0)))
                # Click roughly center to dismiss
                screen = pyautogui.size()
                cx = screen[0] // 2 + random.randint(-100, 100)
                cy = screen[1] // 2 + random.randint(-50, 50)
                pyautogui.click(cx, cy)
            else:
                # Windows: Win+D (show desktop), then Win+D again
                pyautogui.hotkey("win", "d")
                time.sleep(jitter(random.uniform(1.0, 2.0)))
                pyautogui.hotkey("win", "d")
            time.sleep(jitter(0.3))
            return "app-switch: mission control"
