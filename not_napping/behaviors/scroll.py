"""Incremental scrolling with direction bias."""

import random
import time

import pyautogui

from .base import BaseBehavior
from ..timing import jitter

pyautogui.PAUSE = 0


class ScrollBehavior(BaseBehavior):
    name = "scroll"

    def perform(self):
        # Direction bias: 65% down, 35% up
        direction = -1 if random.random() < 0.65 else 1  # negative = down in pyautogui
        num_clicks = random.randint(3, 12)

        desc_dir = "down" if direction == -1 else "up"

        # 15% chance of "read-and-return": scroll down, pause, scroll back partially
        read_and_return = random.random() < 0.15

        for _ in range(num_clicks):
            amount = random.randint(1, 3)
            pyautogui.scroll(direction * amount)
            time.sleep(jitter(random.uniform(0.05, 0.15)))

        if read_and_return:
            # Pause to "read"
            time.sleep(jitter(random.uniform(1.0, 3.0)))
            # Scroll back partially
            return_clicks = random.randint(1, max(1, num_clicks // 2))
            for _ in range(return_clicks):
                amount = random.randint(1, 2)
                pyautogui.scroll(-direction * amount)
                time.sleep(jitter(random.uniform(0.05, 0.15)))
            return f"scroll {desc_dir} {num_clicks} + read-return"

        return f"scroll {desc_dir} {num_clicks} clicks"
