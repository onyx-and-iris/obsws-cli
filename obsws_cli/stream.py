"""module for controlling OBS stream functionality."""

import obsws_python as obsws
import typer

from .errors import ObswsCliError

app = typer.Typer()


@app.callback()
def main():
    """Control OBS stream functionality."""


@app.command()
def start(ctx: typer.Context):
    """Start streaming."""
    try:
        ctx.obj['obsws'].start_stream()
        typer.echo('Streaming started successfully.')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 500:
            raise ObswsCliError(
                'Streaming is already in progress, cannot start.'
            ) from e
        raise


@app.command()
def stop(ctx: typer.Context):
    """Stop streaming."""
    try:
        ctx.obj['obsws'].stop_stream()
        typer.echo('Streaming stopped successfully.')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 501:
            raise ObswsCliError('Streaming is not in progress, cannot stop.') from e
        raise


def _get_streaming_status(ctx: typer.Context) -> tuple:
    """Get streaming status."""
    resp = ctx.obj['obsws'].get_stream_status()
    return resp.output_active, resp.output_duration


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
        try:
            ctx.obj['obsws'].stop_stream()
            typer.echo('Streaming stopped successfully.')
        except obsws.error.OBSSDKRequestError as e:
            raise ObswsCliError(str(e)) from e
    else:
        try:
            ctx.obj['obsws'].start_stream()
            typer.echo('Streaming started successfully.')
        except obsws.error.OBSSDKRequestError as e:
            raise ObswsCliError(str(e)) from e
