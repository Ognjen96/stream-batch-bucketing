from concurrent.futures import ThreadPoolExecutor, Future


def report_error(future: Future) -> None:
    """Callback which is executed after the task finished.
    
       If .exeption returns None, task failed, return None, othervise continue with execution"""
    error = future.exception()
    if error is not None:
        print(f"Task failed: {error!r}", flush=True)

class WorkerPool:
    """Runs submitted work on a fixed set of threads without making the caller wait."""
    def __init__(self, max_workers: int):
        self._max_workers = max_workers
        self._pool = ThreadPoolExecutor(self._max_workers, thread_name_prefix="worker")

    def submit(self, process, item):       
        future = self._pool.submit(process, item)
        future.add_done_callback(report_error)

        return future
    
    def shutdown(self):
        self._pool.shutdown(wait=True)