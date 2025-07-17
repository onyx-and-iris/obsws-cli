"""module for exit codes used in the application."""

from enum import IntEnum, auto


class ExitCode(IntEnum):
    """Exit codes for the application."""

    SUCCESS = 0
    ERROR = auto()
