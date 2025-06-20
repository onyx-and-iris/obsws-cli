"""module for console output handling in obsws_cli."""

from rich.console import Console

out = Console()
err = Console(stderr=True, style='bold red')
