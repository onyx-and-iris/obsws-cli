"""module containing commands for manipulating virtual camera in OBS."""

from typing import Annotated

from cyclopts import App, Parameter

from . import console
from .context import Context

app = App(name='virtualcam', help='Commands for controlling the virtual camera in OBS.')


@app.command(name=['start', 's'])
def start(
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Start the virtual camera."""
    ctx.client.start_virtual_cam()
    console.out.print('Virtual camera started.')


@app.command(name=['stop', 'p'])
def stop(
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Stop the virtual camera."""
    ctx.client.stop_virtual_cam()
    console.out.print('Virtual camera stopped.')


@app.command(name=['toggle', 'tg'])
def toggle(
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle the virtual camera."""
    resp = ctx.client.toggle_virtual_cam()
    if resp.output_active:
        console.out.print('Virtual camera is enabled.')
    else:
        console.out.print('Virtual camera is disabled.')


@app.command(name=['status', 'ss'])
def status(
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the status of the virtual camera."""
    resp = ctx.client.get_virtual_cam_status()
    if resp.output_active:
        console.out.print('Virtual camera is enabled.')
    else:
        console.out.print('Virtual camera is disabled.')
