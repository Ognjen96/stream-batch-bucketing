from dataclasses import dataclass
from typing import Protocol
 
 
@dataclass(frozen=True)
class Message:
    """A single message from the source.
 
    Arrival time is not carried here: the receiver records it when it arrives.
    """
    id: int
    payload: str = ""


@dataclass(frozen = True)
class File:
    name: str
    size_mb: float

@dataclass(frozen = True)
class Bucket:
    files: tuple[File, ...]
    size_mb: float


@dataclass(frozen=True)
class Minibatch:
    """One closed window: the messages it collected and when it was open.
 
    Frozen, so it can be handed to a worker without anyone changing it later.
    """
    messages: tuple[Message, ...]
    opened_at: float
    closed_at: float 

class BucketingStrategy(Protocol):
    def pack(self, files: list[File]) -> list[Bucket]: ...