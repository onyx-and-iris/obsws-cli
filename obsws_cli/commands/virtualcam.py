"""module containing commands for manipulating virtual camera in OBS."""

import typer

from obsws_cli import console

app = typer.Typer()


@app.callback()
def main():
    """Control virtual camera in OBS."""


@app.command('start')
@app.command('s', hidden=True)
def start(ctx: typer.Context):
    """Start the virtual camera."""
    ctx.obj['obsws'].start_virtual_cam()
    console.out.print('Virtual camera started.')


@app.command('stop')
@app.command('p', hidden=True)
def stop(ctx: typer.Context):
    """Stop the virtual camera."""
    ctx.obj['obsws'].stop_virtual_cam()
    console.out.print('Virtual camera stopped.')


@app.command('toggle')
@app.command('tg', hidden=True)
def toggle(ctx: typer.Context):
    """Toggle the virtual camera."""
    resp = ctx.obj['obsws'].toggle_virtual_cam()
    if resp.output_active:
        console.out.print('Virtual camera is enabled.')
    else:
        console.out.print('Virtual camera is disabled.')


@app.command('status')
@app.command('ss', hidden=True)
def status(ctx: typer.Context):
    """Get the status of the virtual camera."""
    resp = ctx.obj['obsws'].get_virtual_cam_status()
    if resp.output_active:
        console.out.print('Virtual camera is enabled.')
    else:
        console.out.print('Virtual camera is disabled.')
