"""module for controlling OBS stream functionality."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS stream functionality."""


def _get_streaming_status(ctx: typer.Context) -> tuple:
    """Get streaming status."""
    resp = ctx.obj['obsws'].get_stream_status()
    return resp.output_active, resp.output_duration


@app.command()
def start(ctx: typer.Context):
    """Start streaming."""
    active, _ = _get_streaming_status(ctx)
    if active:
        typer.echo('Streaming is already in progress, cannot start.')
        raise typer.Exit(code=1)

    ctx.obj['obsws'].start_stream()
    typer.echo('Streaming started successfully.')


@app.command()
def stop(ctx: typer.Context):
    """Stop streaming."""
    active, _ = _get_streaming_status(ctx)
    if not active:
        typer.echo('Streaming is not in progress, cannot stop.')
        raise typer.Exit(code=1)

    ctx.obj['obsws'].stop_stream()
    typer.echo('Streaming stopped successfully.')


@app.command()
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


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle streaming."""
    active, _ = _get_streaming_status(ctx)
    if active:
        ctx.invoke(stop, ctx=ctx)
    else:
        ctx.invoke(start, ctx=ctx)
