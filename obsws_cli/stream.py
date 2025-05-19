"""module for controlling OBS stream functionality."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


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
        typer.echo('Streaming is already in progress, cannot start.', err=True)
        raise typer.Exit(1)

    ctx.obj.start_stream()
    typer.echo('Streaming started successfully.')


@app.command('stop | st')
def stop(ctx: typer.Context):
    """Stop streaming."""
    active, _ = _get_streaming_status(ctx)
    if not active:
        typer.echo('Streaming is not in progress, cannot stop.', err=True)
        raise typer.Exit(1)

    ctx.obj.stop_stream()
    typer.echo('Streaming stopped successfully.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle streaming."""
    resp = ctx.obj.toggle_stream()
    if resp.output_active:
        typer.echo('Streaming started successfully.')
    else:
        typer.echo('Streaming stopped successfully.')


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
                typer.echo(
                    f'Streaming is in progress for {minutes} minutes and {seconds} seconds.'
                )
            else:
                if seconds > 0:
                    typer.echo(f'Streaming is in progress for {seconds} seconds.')
                else:
                    typer.echo('Streaming is in progress for less than a second.')
        else:
            typer.echo('Streaming is in progress.')
    else:
        typer.echo('Streaming is not in progress.')
