"""module for controlling OBS recording functionality."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


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

        typer.echo(err_msg, err=True)
        raise typer.Exit(1)

    ctx.obj.start_record()
    typer.echo('Recording started successfully.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop recording."""
    active, _ = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot stop.', err=True)
        raise typer.Exit(1)

    ctx.obj.stop_record()
    typer.echo('Recording stopped successfully.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle recording."""
    resp = ctx.obj.toggle_record()
    if resp.output_active:
        typer.echo('Recording started successfully.')
    else:
        typer.echo('Recording stopped successfully.')


@app.command('status | ss')
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


@app.command('resume | r')
def resume(ctx: typer.Context):
    """Resume recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot resume.', err=True)
        raise typer.Exit(1)
    if not paused:
        typer.echo('Recording is in progress but not paused, cannot resume.', err=True)
        raise typer.Exit(1)

    ctx.obj.resume_record()
    typer.echo('Recording resumed successfully.')


@app.command('pause | p')
def pause(ctx: typer.Context):
    """Pause recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot pause.', err=True)
        raise typer.Exit(1)
    if paused:
        typer.echo(
            'Recording is in progress but already paused, cannot pause.', err=True
        )
        raise typer.Exit(1)

    ctx.obj.pause_record()
    typer.echo('Recording paused successfully.')
