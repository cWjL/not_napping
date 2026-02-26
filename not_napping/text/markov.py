"""Order-2 Markov chain text generator."""

import random
from .corpus import CORPUS


class MarkovChain:
    """Generates text from an order-2 Markov chain trained on the corpus."""

    def __init__(self, order=2):
        self.order = order
        self.chain = {}
        self._train(CORPUS)

    def _train(self, text):
        words = text.split()
        for i in range(len(words) - self.order):
            key = tuple(words[i : i + self.order])
            next_word = words[i + self.order]
            self.chain.setdefault(key, []).append(next_word)

    def generate(self, num_words=30):
        """Generate a string of approximately num_words words."""
        if not self.chain:
            return "the quick brown fox jumps over the lazy dog"

        key = random.choice(list(self.chain.keys()))
        result = list(key)

        for _ in range(num_words - self.order):
            next_words = self.chain.get(key)
            if next_words is None:
                key = random.choice(list(self.chain.keys()))
                next_words = self.chain[key]
            word = random.choice(next_words)
            result.append(word)
            key = tuple(result[-self.order :])

        return " ".join(result)


# Module-level singleton for reuse
_generator = None


def get_generator():
    global _generator
    if _generator is None:
        _generator = MarkovChain()
    return _generator
