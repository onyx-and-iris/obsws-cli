"""module for console output handling in obsws_cli."""

from rich.console import Console

from .context import Context

out = Console()
err = Console(stderr=True, style='bold red')


def highlight(ctx: Context, text: str) -> str:
    """Highlight text using the current context's style."""
    return f'[{ctx.style.highlight}]{text}[/{ctx.style.highlight}]'
