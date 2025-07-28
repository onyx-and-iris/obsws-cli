"""module containing commands for manipulating studio mode in OBS."""

from typing import Annotated

from cyclopts import App, Parameter

from . import console
from .context import Context

app = App(name='studiomode', help='Commands for controlling studio mode in OBS.')


@app.command(name=['enable', 'on'])
def enable(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Enable studio mode.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    ctx.client.set_studio_mode_enabled(True)
    console.out.print('Studio mode has been enabled.')


@app.command(name=['disable', 'off'])
def disable(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Disable studio mode.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    ctx.client.set_studio_mode_enabled(False)
    console.out.print('Studio mode has been disabled.')


@app.command(name=['toggle', 'tg'])
def toggle(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle studio mode.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    resp = ctx.client.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        ctx.client.set_studio_mode_enabled(False)
        console.out.print('Studio mode is now disabled.')
    else:
        ctx.client.set_studio_mode_enabled(True)
        console.out.print('Studio mode is now enabled.')


@app.command(name=['status', 'ss'])
def status(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the status of studio mode.

    Parameters
    ----------
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    resp = ctx.client.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        console.out.print('Studio mode is enabled.')
    else:
        console.out.print('Studio mode is disabled.')
