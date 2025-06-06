"""module for settings management for obsws-cli."""

from collections import UserDict
from pathlib import Path

from dotenv import dotenv_values

SettingsValue = str | int


class Settings(UserDict):
    """A class to manage settings for obsws-cli.

    This class extends UserDict to provide a dictionary-like interface for settings.
    It loads settings from environment variables and .env files.
    The settings are expected to be in uppercase and should start with 'OBS_'.

    Example:
        settings = Settings()
        host = settings['OBS_HOST']
        settings['OBS_PORT'] = 4455

    """

    def __init__(self, *args, **kwargs):
        """Initialize the Settings object."""
        kwargs.update(
            {
                **dotenv_values('.env'),
                **dotenv_values(Path.home() / '.config' / 'obsws-cli' / 'obsws.env'),
            }
        )
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> SettingsValue:
        """Get a setting value by key."""
        if not key.startswith('OBS_'):
            key = f'OBS_{key}'
        return self.data[key.upper()]

    def __setitem__(self, key: str, value: SettingsValue):
        """Set a setting value by key."""
        if not key.startswith('OBS_'):
            key = f'OBS_{key}'
        self.data[key.upper()] = value


_settings = Settings(
    OBS_HOST='localhost', OBS_PORT=4455, OBS_PASSWORD='', OBS_TIMEOUT=5
)


def get(key: str) -> SettingsValue:
    """Get a setting value by key.

    Args:
        key (str): The key of the setting to retrieve.

    Returns:
        The value of the setting.

    Raises:
        KeyError: If the key does not exist in the settings.

    """
    return _settings[key]
