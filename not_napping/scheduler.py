"""Single-threaded orchestrator with weighted random behavior selection."""

import random
import threading

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


class Scheduler:
    def __init__(self, behaviors, max_delay, verbose=False):
        """
        behaviors: list of BaseBehavior instances (only enabled ones)
        max_delay: maximum delay in seconds
        verbose: print each action
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

    def run(self):
        """Main loop: pick behavior, perform, delay, repeat."""
        delay_gen = burst_pattern(self.max_delay)

        output.ok("Activity simulation started.")
        output.ok("Press Ctrl+C to stop.")

        while not self._stop_event.is_set():
            # Pick a random behavior with weights
            behavior = random.choices(
                self._weighted_behaviors, weights=self._weights, k=1
            )[0]

            try:
                result = behavior.perform()
                output.verbose(result, self.verbose)
            except Exception as e:
                output.verbose(f"{behavior.name} error: {e}", self.verbose)

            # Wait using Event.wait() for interruptible sleep
            delay = next(delay_gen)
            self._stop_event.wait(delay)

    def stop(self):
        """Signal the scheduler to stop."""
        self._stop_event.set()
