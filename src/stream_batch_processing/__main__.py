import time
import os

from .interfaces import Message, Minibatch
from .sources.message_source import PoissonMessageSource
from .batching.batcher import MessageBatcher
from .processing.processor import SimulatedProcessor, SimulatedFilesProcessor
from .sources.file_source import FileGenerator
from .processing.worker_pool import WorkerPool
from .batching.bucketing_strategy import FirstFitDecreasing

def env_var(name: str, default: float) -> float:
    return float(os.environ.get(name, default))

DEFAULT_DURATION_S =  env_var("DEMO_DURATION", 900.0)
RATE_PER_MINUTE = env_var("RATE_PER_MINUTE", 10)
SEED = int(env_var("SEED", 42))
WINDOW_DURATION = env_var("WINDOW_DURATION", 300.0)
SECONDS_PER_MESSAGE = env_var("SECONDS_PER_MESSAGE", 3.0)
MAX_WORKERS = int(env_var("MAX_WORKERS", 10))
AVG_FILE_SIZE_MB = env_var("AVG_FILE_SIZE_MB", 2.0)
BUCKET_CAPACITY_MB = env_var("BUCKET_CAPACITY_MB", 10.0)
NUM_OF_FILES = int(env_var("NUM_OF_FILES", 100))
SECONDS_PER_MB = env_var("SECONDS_PER_MB",1.0)


def now(started_at) -> float:
    return time.monotonic() - started_at

def run_nightly_job(file_source: FileGenerator, strategy: FirstFitDecreasing, worker_pool: WorkerPool, files_processor: SimulatedFilesProcessor) -> None:
    files = file_source.generate_files()
    buckets = strategy.pack(files)
    print(f"nightly job: {len(files)} files packed into {len(buckets)} buckets", flush=True)
    for bucket in buckets:
        worker_pool.submit(files_processor.process, bucket)

def main(duration_s: float = DEFAULT_DURATION_S) -> None:

    message_source = PoissonMessageSource(rate_per_minute=RATE_PER_MINUTE, seed=SEED)
    file_source = FileGenerator(count = NUM_OF_FILES, avg_size_mb = AVG_FILE_SIZE_MB, seed = SEED)
    strategy = FirstFitDecreasing(capacity_mb = BUCKET_CAPACITY_MB)

    batcher = MessageBatcher(window_seconds = WINDOW_DURATION)
    message_processor = SimulatedProcessor(seconds_per_message = SECONDS_PER_MESSAGE)
    files_processor = SimulatedFilesProcessor(seconds_per_mb = SECONDS_PER_MB)

    worker_pool = WorkerPool(max_workers = MAX_WORKERS)

    started_at = time.monotonic()

    delay, message = message_source.next_message()
    next_arrival = delay

    try:

        run_nightly_job(file_source, strategy, worker_pool, files_processor)

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
                worker_pool.submit(message_processor.process, minibatch)
            elif moment >= next_arrival:
                batcher.add(message, moment)
                delay, message = message_source.next_message()
                next_arrival += delay
    
        if batcher._deadline is not None:
            minibatch = batcher.close(now(started_at))
            worker_pool.submit(message_processor.process, minibatch)

    finally:
        worker_pool.shutdown()

if __name__ == "__main__":
    main()