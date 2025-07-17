"""module for exit codes used in the application."""

from enum import IntEnum, auto


class ExitCode(IntEnum):
    """Exit codes for the application."""

    SUCCESS = 0
    ERROR = auto()
    INVALID_ARGUMENT = auto()
    INVALID_PARAMETER = auto()
    NOT_FOUND = auto()
    ALREADY_EXISTS = auto()
    TIMEOUT = auto()
    UNKNOWN_ERROR = auto()
