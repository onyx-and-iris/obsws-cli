"""module contains utility functions for the obsws_cli package."""


def snakecase_to_titlecase(snake_str):
    """Convert a snake_case string to a title case string."""
    return snake_str.replace('_', ' ').title()
