"""module for controlling OBS stream functionality."""

import typer
from rich.console import Console

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control OBS stream functionality."""


def _get_streaming_status(ctx: typer.Context) -> tuple:
    """Get streaming status."""
    resp = ctx.obj.get_stream_status()
    return resp.output_active, resp.output_duration


@app.command('start | s')
def start(ctx: typer.Context):
    """Start streaming."""
    active, _ = _get_streaming_status(ctx)
    if active:
        err_console.print('Streaming is already in progress, cannot start.')
        raise typer.Exit(1)

    ctx.obj.start_stream()
    out_console.print('Streaming started successfully.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop streaming."""
    active, _ = _get_streaming_status(ctx)
    if not active:
        err_console.print('Streaming is not in progress, cannot stop.')
        raise typer.Exit(1)

    ctx.obj.stop_stream()
    out_console.print('Streaming stopped successfully.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle streaming."""
    resp = ctx.obj.toggle_stream()
    if resp.output_active:
        out_console.print('Streaming started successfully.')
    else:
        out_console.print('Streaming stopped successfully.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get streaming status."""
    active, duration = _get_streaming_status(ctx)
    if active:
        if duration > 0:
            seconds = duration / 1000
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            if minutes > 0:
                out_console.print(
                    f'Streaming is in progress for {minutes} minutes and {seconds} seconds.'
                )
            else:
                if seconds > 0:
                    out_console.print(
                        f'Streaming is in progress for {seconds} seconds.'
                    )
                else:
                    out_console.print(
                        'Streaming is in progress for less than a second.'
                    )
        else:
            out_console.print('Streaming is in progress.')
    else:
        out_console.print('Streaming is not in progress.')
