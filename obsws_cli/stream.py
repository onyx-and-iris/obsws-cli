"""module for controlling OBS stream functionality."""

from typing import Annotated

from cyclopts import App, Parameter

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='stream', help='Commands for controlling OBS stream functionality.')


def _get_streaming_status(ctx: Context) -> tuple:
    """Get streaming status."""
    resp = ctx.client.get_stream_status()
    return resp.output_active, resp.output_duration


@app.command(name=['start', 's'])
def start(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Start streaming.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    active, _ = _get_streaming_status(ctx)
    if active:
        raise OBSWSCLIError(
            'Streaming is already in progress, cannot start.',
            code=ExitCode.ERROR,
        )

    ctx.client.start_stream()
    console.out.print('Streaming started successfully.')


@app.command(name=['stop', 'st'])
def stop(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Stop streaming.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    active, _ = _get_streaming_status(ctx)
    if not active:
        raise OBSWSCLIError(
            'Streaming is not in progress, cannot stop.',
            code=ExitCode.ERROR,
        )

    ctx.client.stop_stream()
    console.out.print('Streaming stopped successfully.')


@app.command(name=['toggle', 'tg'])
def toggle(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle streaming.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    resp = ctx.client.toggle_stream()
    if resp.output_active:
        console.out.print('Streaming started successfully.')
    else:
        console.out.print('Streaming stopped successfully.')


@app.command(name=['status', 'ss'])
def status(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get streaming status.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
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
