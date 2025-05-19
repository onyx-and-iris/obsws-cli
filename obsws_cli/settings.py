"""module for settings management."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the OBS WebSocket client."""

    model_config = SettingsConfigDict(
        env_file=(
            '.env',
            Path.home() / '.config' / 'obsws-cli' / 'obsws.env',
        ),
        env_file_encoding='utf-8',
        env_prefix='OBS_',
    )

    HOST: str = 'localhost'
    PORT: int = 4455
    PASSWORD: str = ''  # No password by default
    TIMEOUT: int = 5  # Timeout for requests in seconds


_settings = Settings().model_dump()


def get(key: str) -> str:
    """Get a setting by key."""
    return _settings.get(key)
