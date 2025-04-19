"""module for controlling OBS recording functionality."""

import obsws_python as obsws
import typer

from .errors import ObswsCliError

app = typer.Typer()


@app.callback()
def main():
    """Control OBS recording functionality."""


@app.command()
def start(ctx: typer.Context):
    """Start recording."""
    try:
        ctx.obj['obsws'].start_record()
        typer.echo('Recording started successfully.')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 500:
            raise ObswsCliError(
                'Recording is already in progress, cannot start.'
            ) from e
        raise


@app.command()
def stop(ctx: typer.Context):
    """Stop recording."""
    try:
        ctx.obj['obsws'].stop_record()
        typer.echo('Recording stopped successfully.')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 501:
            raise ObswsCliError('Recording is not in progress, cannot stop.') from e
        raise


def _get_recording_status(ctx: typer.Context) -> tuple:
    """Get recording status."""
    resp = ctx.obj['obsws'].get_record_status()
    return resp.output_active, resp.output_paused


@app.command()
def status(ctx: typer.Context):
    """Get recording status."""
    active, paused = _get_recording_status(ctx)
    if active:
        if paused:
            typer.echo('Recording is in progress and paused.')
        else:
            typer.echo('Recording is in progress.')
    else:
        typer.echo('Recording is not in progress.')


@app.command()
def toggle(ctx: typer.Context):
    """Toggle recording."""
    active, _ = _get_recording_status(ctx)
    if active:
        try:
            ctx.obj['obsws'].stop_record()
            typer.echo('Recording stopped successfully.')
        except obsws.error.OBSSDKRequestError as e:
            raise ObswsCliError(str(e)) from e
    else:
        try:
            ctx.obj['obsws'].start_record()
            typer.echo('Recording started successfully.')
        except obsws.error.OBSSDKRequestError as e:
            raise ObswsCliError(str(e)) from e


@app.command()
def resume(ctx: typer.Context):
    """Resume recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        raise ObswsCliError('Recording is not in progress, cannot resume.')
    if not paused:
        raise ObswsCliError('Recording is in progress but not paused, cannot resume.')

    try:
        ctx.obj['obsws'].resume_record()
        typer.echo('Recording resumed successfully.')
    except obsws.error.OBSSDKRequestError as e:
        raise ObswsCliError(str(e)) from e


@app.command()
def pause(ctx: typer.Context):
    """Pause recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        raise ObswsCliError('Recording is not in progress, cannot pause.')
    if paused:
        raise ObswsCliError(
            'Recording is in progress but already paused, cannot pause.'
        )

    try:
        ctx.obj['obsws'].pause_record()
        typer.echo('Recording paused successfully.')
    except obsws.error.OBSSDKRequestError as e:
        raise ObswsCliError(str(e)) from e
