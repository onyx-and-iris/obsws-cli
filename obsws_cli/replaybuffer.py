"""module containing commands for manipulating the replay buffer in OBS."""

from typing import Annotated

from cyclopts import App, Parameter

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(
    name='replaybuffer', help='Commands for controlling the replay buffer in OBS.'
)


@app.command(name=['start', 's'])
def start(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Start the replay buffer.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    resp = ctx.client.get_replay_buffer_status()
    if resp.output_active:
        raise OBSWSCLIError('Replay buffer is already active.', ExitCode.ERROR)

    ctx.client.start_replay_buffer()
    console.out.print('Replay buffer started.')


@app.command(name=['stop', 'st'])
def stop(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Stop the replay buffer.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    resp = ctx.client.get_replay_buffer_status()
    if not resp.output_active:
        raise OBSWSCLIError('Replay buffer is not active.', ExitCode.ERROR)

    ctx.client.stop_replay_buffer()
    console.out.print('Replay buffer stopped.')


@app.command(name=['toggle', 'tg'])
def toggle(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle the replay buffer.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    resp = ctx.client.toggle_replay_buffer()
    if resp.output_active:
        console.out.print('Replay buffer is active.')
    else:
        console.out.print('Replay buffer is not active.')


@app.command(name=['status', 'ss'])
def status(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the status of the replay buffer.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    resp = ctx.client.get_replay_buffer_status()
    if resp.output_active:
        console.out.print('Replay buffer is active.')
    else:
        console.out.print('Replay buffer is not active.')


@app.command(name=['save', 'sv'])
def save(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Save the replay buffer.

    Parameters
    ----------
    ctx: Context
        The context containing the OBS client and other settings.

    """
    ctx.client.save_replay_buffer()
    console.out.print('Replay buffer saved.')
