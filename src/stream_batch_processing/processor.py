import threading
import time
from .interfaces import Minibatch

class SimulatedProcessor:

    def __init__(self, seconds_per_message: float):
        self._seconds_per_message = seconds_per_message
        

    def process(self, batch: Minibatch) -> None:
        worker = threading.current_thread().name
        count = len(batch.messages)
        print(f"{worker}: start, {count} messages", flush=True)
        time.sleep(count * self._seconds_per_message)
        print(f"{worker}: done, {count} messages", flush=True)