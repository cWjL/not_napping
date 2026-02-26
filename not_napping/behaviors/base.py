"""Abstract base class for all behaviors."""

from abc import ABC, abstractmethod


class BaseBehavior(ABC):
    """Base class that all behavior implementations must subclass."""

    name: str = "base"

    @abstractmethod
    def perform(self):
        """Execute one discrete action (a single mouse move, typing burst, etc.).

        Returns a short string describing what was done (for verbose logging).
        """

    def __repr__(self):
        return f"<{self.__class__.__name__}>"
