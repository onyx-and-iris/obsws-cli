"""module for controlling OBS recording functionality."""

from pathlib import Path
from typing import Annotated, Optional

import typer
from rich.console import Console

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control OBS recording functionality."""


def _get_recording_status(ctx: typer.Context) -> tuple:
    """Get recording status."""
    resp = ctx.obj.get_record_status()
    return resp.output_active, resp.output_paused


@app.command('start | s')
def start(ctx: typer.Context):
    """Start recording."""
    active, paused = _get_recording_status(ctx)
    if active:
        err_msg = 'Recording is already in progress, cannot start.'
        if paused:
            err_msg += ' Try resuming it.'

        err_console.print(err_msg)
        raise typer.Exit(1)

    ctx.obj.start_record()
    out_console.print('Recording started successfully.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop recording."""
    active, _ = _get_recording_status(ctx)
    if not active:
        err_console.print('Recording is not in progress, cannot stop.')
        raise typer.Exit(1)

    resp = ctx.obj.stop_record()
    out_console.print(f'Recording stopped successfully. Saved to: {resp.output_path}')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle recording."""
    resp = ctx.obj.toggle_record()
    if resp.output_active:
        out_console.print('Recording started successfully.')
    else:
        out_console.print('Recording stopped successfully.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get recording status."""
    active, paused = _get_recording_status(ctx)
    if active:
        if paused:
            out_console.print('Recording is in progress and paused.')
        else:
            out_console.print('Recording is in progress.')
    else:
        out_console.print('Recording is not in progress.')


@app.command('resume | r')
def resume(ctx: typer.Context):
    """Resume recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        err_console.print('Recording is not in progress, cannot resume.')
        raise typer.Exit(1)
    if not paused:
        err_console.print('Recording is in progress but not paused, cannot resume.')
        raise typer.Exit(1)

    ctx.obj.resume_record()
    out_console.print('Recording resumed successfully.')


@app.command('pause | p')
def pause(ctx: typer.Context):
    """Pause recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        err_console.print('Recording is not in progress, cannot pause.')
        raise typer.Exit(1)
    if paused:
        err_console.print('Recording is in progress but already paused, cannot pause.')
        raise typer.Exit(1)

    ctx.obj.pause_record()
    out_console.print('Recording paused successfully.')


@app.command('directory | d')
def directory(
    ctx: typer.Context,
    record_directory: Annotated[
        Optional[Path],
        # Since the CLI and OBS may be running on different platforms,
        # we won't validate the path here.
        typer.Argument(
            file_okay=False,
            dir_okay=True,
            help='Directory to set for recording.',
        ),
    ] = None,
):
    """Get or set the recording directory."""
    if record_directory is not None:
        ctx.obj.set_record_directory(str(record_directory))
        out_console.print(f'Recording directory updated to: {record_directory}')
    else:
        out_console.print(
            f'Recording directory: {ctx.obj.get_record_directory().record_directory}'
        )
