"""module for settings management for obsws-cli."""

from collections import UserDict
from pathlib import Path
from typing import Any, Union

from dotenv import dotenv_values

ConfigValue = Union[str, int, bool]


class EnvConfig(UserDict):
    """A class to manage .env config for obsws-cli.

    This class extends UserDict to provide a dictionary-like interface for config.
    It loads config from .env files in the following priority:
    1. Local .env file
    2. User config file (~/.config/obsws-cli/obsws.env)
    3. Default values

    Note, typer handles reading from environment variables automatically. They take precedence
    over values set in this class.

    The config values are expected to be in uppercase and should start with 'OBSWS_CLI_'.

    Example:
    -------
        config = EnvConfig()
        host = config['OBSWS_CLI_HOST']
        config['OBSWS_CLI_PORT'] = 4455
        # Or with defaults
        timeout = config.get('OBSWS_CLI_TIMEOUT', 30)
        # Keys will be normalised to uppercase with prefix
        debug = config.get('debug', False)  # Equivalent to 'OBSWS_CLI_DEBUG'

    """

    PREFIX = 'OBSWS_CLI_'

    def __init__(self, *args, **kwargs):
        """Initialize the Config object with hierarchical loading."""
        kwargs.update(
            {
                **dotenv_values(Path.home() / '.config' / 'obsws-cli' / 'obsws.env'),
                **dotenv_values('.env'),
            }
        )

        super().__init__(*args, **self._convert_types(kwargs))

    def _convert_types(self, config_data: dict[str, Any]) -> dict[str, ConfigValue]:
        """Convert string values to appropriate types."""
        converted = {}
        for key, value in config_data.items():
            if isinstance(value, str):
                if value.lower() in ('true', 'false'):
                    converted[key] = value.lower() == 'true'
                elif value.isdigit():
                    converted[key] = int(value)
                else:
                    converted[key] = value
            else:
                converted[key] = value
        return converted

    def __getitem__(self, key: str) -> ConfigValue:
        """Get a setting value by key."""
        normalised_key = self._normalise_key(key)
        try:
            return self.data[normalised_key]
        except KeyError as e:
            raise KeyError(
                f"Config key '{key}' not found. Available keys: {list(self.data.keys())}"
            ) from e

    def __setitem__(self, key: str, value: ConfigValue):
        """Set a setting value by key."""
        normalised_key = self._normalise_key(key)
        self.data[normalised_key] = value

    def _normalise_key(self, key: str) -> str:
        """Normalise a key to uppercase with OBS_ prefix."""
        key = key.upper()
        if not key.startswith(self.PREFIX):
            key = f'{self.PREFIX}{key}'
        return key

    def get(self, key: str, default=None) -> ConfigValue:
        """Get a config value with optional default.

        Args:
        ----
            key (str): The key to retrieve
            default: Default value if key is not found

        Returns:
        -------
            The config value or default

        """
        normalised_key = self._normalise_key(key)
        if not self.has_key(normalised_key):
            return default
        return self[normalised_key]

    def has_key(self, key: str) -> bool:
        """Check if a config key exists.

        Args:
        ----
            key (str): The key to check

        Returns:
        -------
            bool: True if key exists, False otherwise

        """
        normalised_key = self._normalise_key(key)
        return normalised_key in self.data


_envconfig = EnvConfig(
    OBSWS_CLI_HOST='localhost',
    OBSWS_CLI_PORT=4455,
    OBSWS_CLI_PASSWORD='',
    OBSWS_CLI_TIMEOUT=5,
    OBSWS_CLI_DEBUG=False,
    OBSWS_CLI_STYLE='disabled',
    OBSWS_CLI_STYLE_NO_BORDER=False,
)


def get(key: str) -> ConfigValue:
    """Get a setting value by key from the global config instance.

    Args:
    ----
        key (str): The key of the config to retrieve.
        default: Default value if key is not found.

    Returns:
    -------
        The value of the config or default value.

    """
    return _envconfig.get(key)
