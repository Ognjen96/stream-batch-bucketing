from ..interfaces import Message, Minibatch
 
 
class MessageBatcher:
    """Collects messages into minibatches.
 
    The first message opens a window; the window closes `window_seconds` later.
    The batcher itself never waits: every decision about time comes in as `now`,
    and whoever drives the system decides when to call close().
    """
 
    def __init__(self, window_seconds: float) -> None:
        self._window_seconds = window_seconds
        self._messages: list[Message] = []
        self._opened_at: float | None = None
        self._deadline: float | None = None
 
    def add(self, message: Message, now: float) -> None:
        """Add a message, opening a new window if none is open."""
        if self._deadline is None:
            self._opened_at = now
            self._deadline = now + self._window_seconds

        if self._deadline is not None and now >= self._deadline:
            raise RuntimeError("message arrived after the window deadline")
        
        self._messages.append(message)

 
    def close(self, now: float) -> Minibatch:
        """Close the open window and return it as a minibatch."""
        if self._opened_at is None:
            raise RuntimeError("Window was never opened.")
        self._closed_at = now
        batch = Minibatch(tuple(self._messages), self._opened_at, now)
        self._messages = []
        self._opened_at = None
        self._deadline = None

        return batch