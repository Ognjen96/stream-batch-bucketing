import random
from collections.abc import Iterator
 
from .interfaces import Message

SECONDS_PER_MINUTE = 60.0 
 
class PoissonMessageSource:
    """Produces messages as a Poisson process averaging `rate_per_minute` messages per minute."""
    def __init__(self, rate_per_minute: float, rng: random.Random) -> None:
        self._rate_per_minute = rate_per_minute
        self._rng = rng
        self._next_id = 1
 
    def next_message(self) -> tuple[float, Message]:
        """Return (delay in seconds until the next message, the message)."""
        delay = self._rng.expovariate(self._rate_per_minute / SECONDS_PER_MINUTE)
        message = Message(id=self._next_id)
        self._next_id += 1
        return delay, message