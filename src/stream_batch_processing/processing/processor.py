import threading
import time
from ..interfaces import Minibatch, Bucket

class SimulatedProcessor:
    """Class used to simulate processing of a minibatch.

       Processing takes `seconds_per_message` seconds for every message in the batch."""

    def __init__(self, seconds_per_message: float):
        self._seconds_per_message = seconds_per_message
        

    def process(self, batch: Minibatch) -> None:
        worker = threading.current_thread().name
        count = len(batch.messages)
        print(f"{worker}: start, {count} messages\n",end="", flush=True)
        time.sleep(count * self._seconds_per_message)
        print(f"{worker}: done, {count} messages\n",end="", flush=True)


class SimulatedFilesProcessor:
    """Class used to simulate a transformation of buckets which arrive as a nigthly job. 
    
       Processing takes `seconds_per_mb` seconds for every MB in the bucket,
       so larger buckets keep a worker busy longer."""

    def __init__(self, seconds_per_mb: float):
        self._seconds_per_mb = seconds_per_mb

    def process(self, bucket: Bucket):
        worker = threading.current_thread().name
        count = bucket.size_mb
        print(f"{worker}: start, {count:.1f} Megabytes\n", end="", flush=True)
        time.sleep(count * self._seconds_per_mb)
        print(f"{worker}: done, {count:.1f} Megabytes\n", end="", flush=True)