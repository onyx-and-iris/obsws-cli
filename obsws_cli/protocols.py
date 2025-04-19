"""module defining protocols for type hinting."""

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
@dataclass
class DataclassProtocol(Protocol):
    """A protocol for dataclass-like structures."""
