import random
 
import pytest
 
from stream_batch_processing.interfaces import Message
from stream_batch_processing.source import PoissonMessageSource
 
 
def make_source(seed: int = 42, rate_per_minute: float = 10) -> PoissonMessageSource:
    return PoissonMessageSource(rate_per_minute=rate_per_minute, rng=random.Random(seed))
 
 
def take(source: PoissonMessageSource, n: int) -> list[tuple[float, Message]]:
    return [source.next_message() for _ in range(n)]
 
 
def test_ids_are_sequential():
    pairs = take(make_source(), 100)
 
    ids = [message.id for _, message in pairs]
    assert ids == list(range(1, 101))
 
 
def test_same_seed_gives_same_delays():
    first = [delay for delay, _ in take(make_source(seed=7), 50)]
    again = [delay for delay, _ in take(make_source(seed=7), 50)]
    other = [delay for delay, _ in take(make_source(seed=8), 50)]
 
    assert first == again
    assert first != other
 
 
def test_average_delay_matches_configured_rate():
    delays = [delay for delay, _ in take(make_source(), 10_000)]
 
    average = sum(delays) / len(delays)
    assert average == pytest.approx(6.0, rel=0.05)