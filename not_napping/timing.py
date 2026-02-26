"""Human-like delay generation with burst/lull patterns."""

import random


def jitter(value, pct=0.15):
    """Add +/- pct noise to a timing value."""
    noise = value * random.uniform(-pct, pct)
    return max(0.01, value + noise)


def human_delay(low=0.5, high=3.0):
    """Beta-distributed delay skewed toward shorter values."""
    # alpha=2, beta=5 skews toward low end
    sample = random.betavariate(2, 5)
    return low + sample * (high - low)


def burst_pattern(max_delay):
    """Yield an infinite sequence of delays: clusters of short delays
    followed by one longer pause (30-100% of max_delay).

    Produces 3-15 short delays, then one long pause, repeating.
    """
    while True:
        burst_length = random.randint(3, 15)
        for _ in range(burst_length):
            yield jitter(human_delay(0.5, 3.0))
        # Longer lull between bursts
        lull = random.uniform(0.3, 1.0) * max_delay
        yield jitter(lull)


def typing_delay():
    """Inter-key delay for typing simulation."""
    return max(0.02, random.gauss(0.08, 0.03))


def thinking_pause():
    """Pause at word boundaries to simulate thinking."""
    return random.uniform(0.5, 2.0)
