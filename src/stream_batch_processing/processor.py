import threading
import time
from .interfaces import Minibatch, Bucket

class SimulatedProcessor:

    def __init__(self, seconds_per_message: float):
        self._seconds_per_message = seconds_per_message
        

    def process(self, batch: Minibatch) -> None:
        worker = threading.current_thread().name
        count = len(batch.messages)
        print(f"{worker}: start, {count} messages\n",end="", flush=True)
        time.sleep(count * self._seconds_per_message)
        print(f"{worker}: done, {count} messages\n",end="", flush=True)


class SimulatedFilesProcessor:
    def __init__(self, seconds_per_mb: float):
        self._seconds_per_mb = seconds_per_mb

    def process(self, bucket: Bucket):
        worker = threading.current_thread().name
        count = bucket.size_mb
        print(f"{worker}: start, {count:.1f} Megabytes\n", end="", flush=True)
        time.sleep(count * self._seconds_per_mb)
        print(f"{worker}: done, {count:.1f} Megabytes\n", end="", flush=True)