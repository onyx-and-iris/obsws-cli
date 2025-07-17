"""module containing error handling for OBS WebSocket CLI."""


class OBSWSCLIError(Exception):
    """Base class for OBS WebSocket CLI errors."""

    def __init__(self, message: str, code: int = 1):
        """Initialize the error with a message and an optional code."""
        super().__init__(message)
        self.message = message
        self.code = code
