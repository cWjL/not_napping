"""Single-threaded orchestrator with weighted random behavior selection."""

import random
import threading
import time

from .timing import burst_pattern
from . import output


# Default weights: mouse 35%, typing 25%, scroll 20%, app-switch 12%, file-access 8%
DEFAULT_WEIGHTS = {
    "mouse": 35,
    "typing": 25,
    "scroll": 20,
    "app_switch": 12,
    "file_access": 8,
}

# Brief grace period after perform() before arming the watchdog,
# so residual synthetic events don't trigger a false stop.
_ARM_GRACE = 0.2


class Scheduler:
    def __init__(self, behaviors, max_delay, verbose=False, auto_cancel=True):
        """
        behaviors: list of BaseBehavior instances (only enabled ones)
        max_delay: maximum delay in seconds
        verbose: print each action
        auto_cancel: stop when real user input is detected
        """
        self.behaviors = behaviors
        self.max_delay = max_delay
        self.verbose = verbose
        self._stop_event = threading.Event()

        # Build weighted list from available behaviors
        self._weighted_behaviors = []
        self._weights = []
        for b in behaviors:
            weight = DEFAULT_WEIGHTS.get(b.name, 10)
            self._weighted_behaviors.append(b)
            self._weights.append(weight)

        # Watchdog setup (graceful degradation if pynput missing)
        self._watchdog = None
        if auto_cancel:
            try:
                from .watchdog import InputWatchdog
                self._watchdog = InputWatchdog(self._on_user_input)
            except ImportError:
                output.warn(
                    "pynput not installed — auto-cancel disabled. "
                    "Install with: pip install pynput"
                )

    def _on_user_input(self):
        """Called by the watchdog when real input is detected."""
        output.warn("Real user input detected — stopping automatically.")
        self._stop_event.set()

    def run(self):
        """Main loop: pick behavior, perform, delay, repeat."""
        delay_gen = burst_pattern(self.max_delay)

        if self._watchdog:
            self._watchdog.start()
            output.ok("Auto-cancel enabled (will stop on real input).")

        output.ok("Activity simulation started.")
        output.ok("Press Ctrl+C to stop.")

        while not self._stop_event.is_set():
            # Pick a random behavior with weights
            behavior = random.choices(
                self._weighted_behaviors, weights=self._weights, k=1
            )[0]

            # Disarm watchdog while behavior runs (synthetic input)
            if self._watchdog:
                self._watchdog.disarm()

            try:
                result = behavior.perform()
                output.verbose(result, self.verbose)
            except Exception as e:
                output.warn(f"{behavior.name} error: {e}")

            # Grace period, then arm watchdog for the delay window
            if self._watchdog and not self._stop_event.is_set():
                import pyautogui
                time.sleep(_ARM_GRACE)
                self._watchdog.arm(pyautogui.position())

            # Wait using Event.wait() for interruptible sleep
            delay = next(delay_gen)
            self._stop_event.wait(delay)

    def stop(self):
        """Signal the scheduler to stop."""
        self._stop_event.set()
        if self._watchdog:
            self._watchdog.stop()
