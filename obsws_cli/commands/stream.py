"""module for controlling OBS stream functionality."""

import typer

from obsws_cli import console

app = typer.Typer()


@app.callback()
def main():
    """Control OBS stream functionality."""


def _get_streaming_status(ctx: typer.Context) -> tuple:
    """Get streaming status."""
    resp = ctx.obj['obsws'].get_stream_status()
    return resp.output_active, resp.output_duration


@app.command('start')
@app.command('s', hidden=True)
def start(ctx: typer.Context):
    """Start streaming."""
    active, _ = _get_streaming_status(ctx)
    if active:
        console.err.print('Streaming is already in progress, cannot start.')
        raise typer.Exit(1)

    ctx.obj['obsws'].start_stream()
    console.out.print('Streaming started successfully.')


@app.command('stop')
@app.command('st', hidden=True)
def stop(ctx: typer.Context):
    """Stop streaming."""
    active, _ = _get_streaming_status(ctx)
    if not active:
        console.err.print('Streaming is not in progress, cannot stop.')
        raise typer.Exit(1)

    ctx.obj['obsws'].stop_stream()
    console.out.print('Streaming stopped successfully.')


@app.command('toggle')
@app.command('tg', hidden=True)
def toggle(ctx: typer.Context):
    """Toggle streaming."""
    resp = ctx.obj['obsws'].toggle_stream()
    if resp.output_active:
        console.out.print('Streaming started successfully.')
    else:
        console.out.print('Streaming stopped successfully.')


@app.command('status')
@app.command('ss', hidden=True)
def status(ctx: typer.Context):
    """Get streaming status."""
    active, duration = _get_streaming_status(ctx)
    if active:
        if duration > 0:
            seconds = duration / 1000
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            if minutes > 0:
                console.out.print(
                    f'Streaming is in progress for {minutes} minutes and {seconds} seconds.'
                )
            else:
                if seconds > 0:
                    console.out.print(
                        f'Streaming is in progress for {seconds} seconds.'
                    )
                else:
                    console.out.print(
                        'Streaming is in progress for less than a second.'
                    )
        else:
            console.out.print('Streaming is in progress.')
    else:
        console.out.print('Streaming is not in progress.')
