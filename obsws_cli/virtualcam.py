"""module containing commands for manipulating virtual camera in OBS."""

import typer
from rich.console import Console

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control virtual camera in OBS."""


@app.command('start | s')
def start(ctx: typer.Context):
    """Start the virtual camera."""
    ctx.obj.start_virtual_cam()
    out_console.print('Virtual camera started.')


@app.command('stop | p')
def stop(ctx: typer.Context):
    """Stop the virtual camera."""
    ctx.obj.stop_virtual_cam()
    out_console.print('Virtual camera stopped.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle the virtual camera."""
    resp = ctx.obj.toggle_virtual_cam()
    if resp.output_active:
        out_console.print('Virtual camera is enabled.')
    else:
        out_console.print('Virtual camera is disabled.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of the virtual camera."""
    resp = ctx.obj.get_virtual_cam_status()
    if resp.output_active:
        out_console.print('Virtual camera is enabled.')
    else:
        out_console.print('Virtual camera is disabled.')
