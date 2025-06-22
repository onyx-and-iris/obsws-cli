"""module contains utility functions for the obsws_cli package."""

import typer


def snakecase_to_titlecase(snake_str: str) -> str:
    """Convert a snake_case string to a title case string."""
    return snake_str.replace('_', ' ').title()


def check_mark(ctx: typer.Context, value: bool, empty_if_false: bool = False) -> str:
    """Return a check mark or cross mark based on the boolean value."""
    if empty_if_false and not value:
        return ''

    if ctx.obj['style'].name == 'no_colour':
        return '✓' if value else '✗'
    return '✅' if value else '❌'
