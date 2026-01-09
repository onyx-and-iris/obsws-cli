"""module for settings management for obsws-cli."""

from collections import UserDict
from pathlib import Path

from dotenv import dotenv_values

ConfigValue = str | int


class Config(UserDict):
    """A class to manage config for obsws-cli.

    This class extends UserDict to provide a dictionary-like interface for config.
    It loads config from environment variables and .env files.
    The config values are expected to be in uppercase and should start with 'OBS_'.

    Example:
    -------
        config = Config()
        host = config['OBS_HOST']
        config['OBS_PORT'] = 4455

    """

    PREFIX = 'OBS_'

    def __init__(self, *args, **kwargs):
        """Initialize the Settings object."""
        kwargs.update(
            {
                **dotenv_values('.env'),
                **dotenv_values(Path.home() / '.config' / 'obsws-cli' / 'obsws.env'),
            }
        )
        super().__init__(*args, **kwargs)

    def __getitem__(self, key: str) -> ConfigValue:
        """Get a setting value by key."""
        key = key.upper()
        if not key.startswith(Config.PREFIX):
            key = f'{Config.PREFIX}{key}'
        return self.data[key]

    def __setitem__(self, key: str, value: ConfigValue):
        """Set a setting value by key."""
        key = key.upper()
        if not key.startswith(Config.PREFIX):
            key = f'{Config.PREFIX}{key}'
        self.data[key] = value


_config = Config(
    OBS_HOST='localhost',
    OBS_PORT=4455,
    OBS_PASSWORD='',
    OBS_TIMEOUT=5,
    OBS_DEBUG=False,
    OBS_STYLE='disabled',
    OBS_STYLE_NO_BORDER=False,
)


def get(key: str) -> ConfigValue:
    """Get a setting value by key.

    Args:
    ----
        key (str): The key of the config to retrieve.

    Returns:
    -------
        The value of the config.

    Raises:
    ------
        KeyError: If the key does not exist in the config.

    """
    return _config[key]
