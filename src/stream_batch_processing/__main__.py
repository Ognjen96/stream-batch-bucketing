import random
import time
 
from .interfaces import Message, Minibatch
from .source import PoissonMessageSource
from .batcher import MessageBatcher
from .processor import SimulatedProcessor
from .worker_pool import WorkerPool
 
DEFAULT_DURATION_S = 60.0
RATE_PER_MINUTE = 10
SEED = 42
WINDOW_DURATION = 10.0
SECONDS_PER_MESSAGE = 3.0 
MAX_WORKERS = 10

def handle_batch(batch: Minibatch) -> None:
    """Stand-in for the worker pool: prints what would be processed."""
    print(
        f"{batch.closed_at:7.1f}s  batch of {len(batch.messages)} messages"
        f"  (window {batch.opened_at:.1f} - {batch.closed_at:.1f})",
        flush=True,
    ) 

def now(started_at) -> float:
    return time.monotonic() - started_at

def main(duration_s: float = DEFAULT_DURATION_S) -> None:
    source = PoissonMessageSource(rate_per_minute=RATE_PER_MINUTE, rng=random.Random(SEED))
    batcher = MessageBatcher(WINDOW_DURATION)
    processor = SimulatedProcessor(SECONDS_PER_MESSAGE)
    worker_pool = WorkerPool(MAX_WORKERS)

    started_at = time.monotonic()

    delay, message = source.next_message()
    next_arrival = delay

    try:
        while now(started_at) < duration_s:
            if batcher._deadline is None:
                wake = next_arrival
            else:
                wake = min(next_arrival, batcher._deadline)
            wake = min(wake, duration_s)
            time.sleep(max(0.0, wake - now(started_at)))
            moment = now(started_at)
    
            if batcher._deadline is not None and moment >= batcher._deadline:
                minibatch = batcher.close(moment)
                worker_pool.submit(processor.process, minibatch)
            elif moment >= next_arrival:
                batcher.add(message, moment)
                delay, message = source.next_message()
                next_arrival += delay
    
        if batcher._deadline is not None:
            minibatch = batcher.close(now(started_at))
            worker_pool.submit(processor.process, minibatch)

    finally:
        worker_pool.shutdown()

if __name__ == "__main__":
    main()