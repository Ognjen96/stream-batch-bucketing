from dataclasses import dataclass
from typing import Protocol
 
 
@dataclass(frozen=True)
class Message:
    """A single message from the source."""
    id: int
    payload: str = ""


@dataclass(frozen = True)
class File:
    """Interface for one file"""
    name: str
    size_mb: float

@dataclass(frozen = True)
class Bucket:
    """Interface for one Bucket"""
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
    """Decides how the night's files are grouped into buckets."""
    def pack(self, files: list[File]) -> list[Bucket]: ...