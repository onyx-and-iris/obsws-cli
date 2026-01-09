"""module contains utility functions for the obsws_cli package."""

import os


def snakecase_to_titlecase(snake_str: str) -> str:
    """Convert a snake_case string to a title case string."""
    return snake_str.replace('_', ' ').title()


def check_mark(value: bool, empty_if_false: bool = False) -> str:
    """Return a check mark or cross mark based on the boolean value."""
    if empty_if_false and not value:
        return ''

    # rich gracefully handles the absence of colour throughout the rest of the application,
    # but here we must handle it manually.
    # If NO_COLOR is set, we return plain text symbols.
    # Otherwise, we return coloured symbols.
    if os.getenv('NO_COLOR', '') != '':
        return '✓' if value else '✗'
    return '✅' if value else '❌'


def timecode_to_milliseconds(timecode: str) -> int:
    """Convert a timecode string (HH:MM:SS) to total milliseconds."""
    match timecode.split(':'):
        case [mm, ss]:
            hours = 0
            minutes = int(mm)
            seconds = int(ss)
        case [hh, mm, ss]:
            hours = int(hh)
            minutes = int(mm)
            seconds = int(ss)
    return (hours * 3600 + minutes * 60 + seconds) * 1000


def milliseconds_to_timecode(milliseconds: int) -> str:
    """Convert total milliseconds to a timecode string (HH:MM:SS)."""
    total_seconds = milliseconds // 1000
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    if hours == 0:
        return f'{minutes:02}:{seconds:02}'
    return f'{hours:02}:{minutes:02}:{seconds:02}'
