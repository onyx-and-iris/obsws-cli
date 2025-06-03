"""module for settings management for obsws-cli."""

from collections import UserDict
from pathlib import Path

from dotenv import dotenv_values


class Settings(UserDict):
    """Settings for the OBS WebSocket client."""

    def __init__(self, *args, **kwargs):
        """Initialize the Settings object."""
        kwargs.update(
            {
                **dotenv_values('.env'),
                **dotenv_values(Path.home() / '.config' / 'obsws-cli' / 'obsws.env'),
            }
        )
        super().__init__(*args, **kwargs)

    def __getitem__(self, key):
        """Get a setting value by key."""
        if not key.startswith('OBS_'):
            key = f'OBS_{key.upper()}'
        return self.data[key]

    def __setitem__(self, key, value):
        """Set a setting value by key."""
        self.data[key] = value


_settings = Settings(
    OBS_HOST='localhost', OBS_PORT=4455, OBS_PASSWORD='', OBS_TIMEOUT=5
)


def get(key: str):
    """Get a setting value by key.

    Args:
        key (str): The key of the setting to retrieve.

    Returns:
        The value of the setting.

    Raises:
        KeyError: If the key does not exist in the settings.

    """
    return _settings[key]
