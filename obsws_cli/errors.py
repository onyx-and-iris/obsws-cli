"""Exceptions for obsws_cli."""


class ObswsCliError(Exception):
    """Base class for all exceptions raised by obsws_cli."""

    def __init__(self, message: str):
        """Initialize the exception with a message."""
        message = (
            message.split('With message: ')[1]
            if 'With message: ' in message
            else message
        )
        super().__init__(message)


class ObswsCliBadParameter(ObswsCliError):
    """Exception raised when a bad parameter is passed to a command."""
