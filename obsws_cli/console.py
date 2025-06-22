"""module for console output handling in obsws_cli."""

import typer
from rich.console import Console

out = Console()
err = Console(stderr=True, style='bold red')


def highlight(ctx: typer.Context, text: str) -> str:
    """Highlight text using the current context's style."""
    return f'[{ctx.obj["style"].highlight}]{text}[/{ctx.obj["style"].highlight}]'
