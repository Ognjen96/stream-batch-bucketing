from concurrent.futures import ThreadPoolExecutor, Future

def report_error(future: Future) -> None:
    error = future.exception()
    if error is not None:
        print(f"Task failed: {error!r}", flush=True)

class WorkerPool:
    def __init__(self, max_workers: int):
        self._max_workers = max_workers
        self._pool = ThreadPoolExecutor(self._max_workers, thread_name_prefix="worker")

    def submit(self, process, item):       
        future = self._pool.submit(process, item)
        future.add_done_callback(report_error)

        return future
    
    def shutdown(self):
        self._pool.shutdown(wait=True)