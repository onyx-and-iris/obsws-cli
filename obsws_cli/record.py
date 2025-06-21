"""module for controlling OBS recording functionality."""

from pathlib import Path
from typing import Annotated, Optional

import typer

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control OBS recording functionality."""


def _get_recording_status(ctx: typer.Context) -> tuple:
    """Get recording status."""
    resp = ctx.obj['obsws'].get_record_status()
    return resp.output_active, resp.output_paused


@app.command('start | s')
def start(ctx: typer.Context):
    """Start recording."""
    active, paused = _get_recording_status(ctx)
    if active:
        err_msg = 'Recording is already in progress, cannot start.'
        if paused:
            err_msg += ' Try resuming it.'

        console.err.print(err_msg)
        raise typer.Exit(1)

    ctx.obj['obsws'].start_record()
    console.out.print('Recording started successfully.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop recording."""
    active, _ = _get_recording_status(ctx)
    if not active:
        console.err.print('Recording is not in progress, cannot stop.')
        raise typer.Exit(1)

    resp = ctx.obj['obsws'].stop_record()
    console.out.print(
        f'Recording stopped successfully. Saved to: {console.highlight(ctx, resp.output_path)}'
    )


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle recording."""
    resp = ctx.obj['obsws'].toggle_record()
    if resp.output_active:
        console.out.print('Recording started successfully.')
    else:
        console.out.print('Recording stopped successfully.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get recording status."""
    active, paused = _get_recording_status(ctx)
    if active:
        if paused:
            console.out.print('Recording is in progress and paused.')
        else:
            console.out.print('Recording is in progress.')
    else:
        console.out.print('Recording is not in progress.')


@app.command('resume | r')
def resume(ctx: typer.Context):
    """Resume recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        console.err.print('Recording is not in progress, cannot resume.')
        raise typer.Exit(1)
    if not paused:
        console.err.print('Recording is in progress but not paused, cannot resume.')
        raise typer.Exit(1)

    ctx.obj['obsws'].resume_record()
    console.out.print('Recording resumed successfully.')


@app.command('pause | p')
def pause(ctx: typer.Context):
    """Pause recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        console.err.print('Recording is not in progress, cannot pause.')
        raise typer.Exit(1)
    if paused:
        console.err.print('Recording is in progress but already paused, cannot pause.')
        raise typer.Exit(1)

    ctx.obj['obsws'].pause_record()
    console.out.print('Recording paused successfully.')


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
        ctx.obj['obsws'].set_record_directory(str(record_directory))
        console.out.print(
            f'Recording directory updated to: {console.highlight(ctx, record_directory)}'
        )
    else:
        resp = ctx.obj['obsws'].get_record_directory()
        console.out.print(
            f'Recording directory: {console.highlight(ctx, resp.record_directory)}'
        )
