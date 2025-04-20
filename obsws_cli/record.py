"""module for controlling OBS recording functionality."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS recording functionality."""


def _get_recording_status(ctx: typer.Context) -> tuple:
    """Get recording status."""
    resp = ctx.obj['obsws'].get_record_status()
    return resp.output_active, resp.output_paused


@app.command()
def start(ctx: typer.Context):
    """Start recording."""
    active, paused = _get_recording_status(ctx)
    if active:
        err_msg = 'Recording is already in progress, cannot start.'
        if paused:
            err_msg += ' Try resuming it.'

        typer.echo(err_msg)
        raise typer.Exit(1)

    ctx.obj['obsws'].start_record()
    typer.echo('Recording started successfully.')


@app.command()
def stop(ctx: typer.Context):
    """Stop recording."""
    active, _ = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot stop.')
        raise typer.Exit(1)

    ctx.obj['obsws'].stop_record()
    typer.echo('Recording stopped successfully.')


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


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle recording."""
    active, _ = _get_recording_status(ctx)
    if active:
        ctx.invoke(stop, ctx=ctx)
    else:
        ctx.invoke(start, ctx=ctx)


@app.command()
def resume(ctx: typer.Context):
    """Resume recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot resume.')
        raise typer.Exit(1)
    if not paused:
        typer.echo('Recording is in progress but not paused, cannot resume.')
        raise typer.Exit(1)

    ctx.obj['obsws'].resume_record()
    typer.echo('Recording resumed successfully.')


@app.command()
def pause(ctx: typer.Context):
    """Pause recording."""
    active, paused = _get_recording_status(ctx)
    if not active:
        typer.echo('Recording is not in progress, cannot pause.')
        raise typer.Exit(1)
    if paused:
        typer.echo('Recording is in progress but already paused, cannot pause.')
        raise typer.Exit(1)

    ctx.obj['obsws'].pause_record()
    typer.echo('Recording paused successfully.')
