"""module containing commands for manipulating studio mode in OBS."""

import typer
from rich.console import Console

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control studio mode in OBS."""


@app.command('enable | on')
def enable(ctx: typer.Context):
    """Enable studio mode."""
    ctx.obj.set_studio_mode_enabled(True)
    out_console.print('Studio mode has been enabled.')


@app.command('disable | off')
def disable(ctx: typer.Context):
    """Disable studio mode."""
    ctx.obj.set_studio_mode_enabled(False)
    out_console.print('Studio mode has been disabled.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle studio mode."""
    resp = ctx.obj.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        ctx.obj.set_studio_mode_enabled(False)
        out_console.print('Studio mode is now disabled.')
    else:
        ctx.obj.set_studio_mode_enabled(True)
        out_console.print('Studio mode is now enabled.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of studio mode."""
    resp = ctx.obj.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        out_console.print('Studio mode is enabled.')
    else:
        out_console.print('Studio mode is disabled.')
