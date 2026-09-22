import random
from collections.abc import Iterator
 
from .interfaces import Message
 
 
class PoissonMessageSource:
    """Produces messages as a Poisson process averaging `rate_per_minute` messages per minute."""
    def __init__(self, rate_per_minute: float, rng: random.Random) -> None:
        self._rate_per_minute = rate_per_minute
        self._rng = rng
 
    def messages(self) -> Iterator[tuple[float, Message]]:
        next_id = 1
        while True:
            delay = self._rng.expovariate(self._rate_per_minute / 60)
            yield delay, Message(id=next_id)
            next_id += 1