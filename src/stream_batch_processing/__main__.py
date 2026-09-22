import random
import time
 
from .interfaces import Message, MessageSink
from .source import PoissonMessageSource
 
DEFAULT_DURATION_S = 60.0
RATE_PER_MINUTE = 10
SEED = 42


class PrintSink:
    """Demo sink: prints elapsed time and message id."""
 
    def __init__(self) -> None:
        self._start = time.monotonic()
 
    def on_message(self, message: Message) -> None:
        elapsed = time.monotonic() - self._start
        print(f"{elapsed:7.1f}s  message {message.id}", flush=True)
 
 
def main(duration_s: float = DEFAULT_DURATION_S) -> None:
    source = PoissonMessageSource(rate_per_minute=RATE_PER_MINUTE, rng=random.Random(SEED))
    sink: MessageSink = PrintSink()
 
    deadline = time.monotonic() + duration_s
    for delay, message in source.messages():
        if time.monotonic() + delay > deadline:
            break
        time.sleep(delay)
        sink.on_message(message)
 
 
if __name__ == "__main__":
    main()