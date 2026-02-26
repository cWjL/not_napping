"""Bezier-curve mouse movement with jitter and overshoot."""

import random
import time

import pyautogui

from .base import BaseBehavior
from ..timing import jitter

# We handle all timing ourselves
pyautogui.PAUSE = 0


def _bezier_point(t, p0, p1, p2, p3):
    """Evaluate a cubic bezier curve at parameter t."""
    u = 1 - t
    return (
        u ** 3 * p0[0] + 3 * u ** 2 * t * p1[0] + 3 * u * t ** 2 * p2[0] + t ** 3 * p3[0],
        u ** 3 * p0[1] + 3 * u ** 2 * t * p1[1] + 3 * u * t ** 2 * p2[1] + t ** 3 * p3[1],
    )


def _ease_in_out(t):
    """Smooth ease-in/ease-out for speed along the curve."""
    return t * t * (3 - 2 * t)


class MouseBehavior(BaseBehavior):
    name = "mouse"

    def __init__(self):
        screen = pyautogui.size()
        self.screen_w = screen[0]
        self.screen_h = screen[1]

    def _random_target(self):
        """Pick a target biased toward screen center (gaussian)."""
        cx, cy = self.screen_w / 2, self.screen_h / 2
        x = int(random.gauss(cx, self.screen_w * 0.2))
        y = int(random.gauss(cy, self.screen_h * 0.2))
        # Clamp to screen bounds with margin
        x = max(10, min(self.screen_w - 10, x))
        y = max(10, min(self.screen_h - 10, y))
        return x, y

    def _random_control_point(self, start, end):
        """Generate a random control point between start and end."""
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        spread_x = abs(end[0] - start[0]) * 0.5 + 50
        spread_y = abs(end[1] - start[1]) * 0.5 + 50
        return (
            mid_x + random.gauss(0, spread_x),
            mid_y + random.gauss(0, spread_y),
        )

    def perform(self):
        current = pyautogui.position()
        start = (current[0], current[1])
        target = self._random_target()

        # Generate cubic bezier control points
        cp1 = self._random_control_point(start, target)
        cp2 = self._random_control_point(start, target)

        # Number of steps based on distance
        dist = ((target[0] - start[0]) ** 2 + (target[1] - start[1]) ** 2) ** 0.5
        steps = max(20, int(dist / 8))

        # Move along the bezier curve
        for i in range(steps + 1):
            t = _ease_in_out(i / steps)
            bx, by = _bezier_point(t, start, cp1, cp2, target)
            # Add per-point jitter (1-3px gaussian noise)
            jx = bx + random.gauss(0, 1.5)
            jy = by + random.gauss(0, 1.5)
            pyautogui.moveTo(int(jx), int(jy))
            time.sleep(jitter(0.008, 0.3))

        # ~30% chance: overshoot then correct
        if random.random() < 0.30:
            dx = target[0] - start[0]
            dy = target[1] - start[1]
            overshoot_dist = random.uniform(5, 25)
            if dist > 0:
                ox = target[0] + dx / dist * overshoot_dist
                oy = target[1] + dy / dist * overshoot_dist
            else:
                ox = target[0] + random.gauss(0, 10)
                oy = target[1] + random.gauss(0, 10)
            ox = max(5, min(self.screen_w - 5, int(ox)))
            oy = max(5, min(self.screen_h - 5, int(oy)))
            pyautogui.moveTo(ox, oy)
            time.sleep(jitter(0.05))
            # Correct back to target
            for i in range(8):
                t = _ease_in_out(i / 7)
                cx = ox + (target[0] - ox) * t
                cy = oy + (target[1] - oy) * t
                pyautogui.moveTo(int(cx), int(cy))
                time.sleep(jitter(0.01))

        return f"mouse -> ({target[0]}, {target[1]})"
