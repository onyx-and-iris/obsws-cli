"""module containing commands for manipulating studio mode in OBS."""

import typer

from obsws_cli import console

app = typer.Typer()


@app.callback()
def main():
    """Control studio mode in OBS."""


@app.command('enable')
@app.command('on', hidden=True)
def enable(ctx: typer.Context):
    """Enable studio mode."""
    ctx.obj['obsws'].set_studio_mode_enabled(True)
    console.out.print('Studio mode has been enabled.')


@app.command('disable')
@app.command('off', hidden=True)
def disable(ctx: typer.Context):
    """Disable studio mode."""
    ctx.obj['obsws'].set_studio_mode_enabled(False)
    console.out.print('Studio mode has been disabled.')


@app.command('toggle')
@app.command('tg', hidden=True)
def toggle(ctx: typer.Context):
    """Toggle studio mode."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        ctx.obj['obsws'].set_studio_mode_enabled(False)
        console.out.print('Studio mode is now disabled.')
    else:
        ctx.obj['obsws'].set_studio_mode_enabled(True)
        console.out.print('Studio mode is now enabled.')


@app.command('status')
@app.command('ss', hidden=True)
def status(ctx: typer.Context):
    """Get the status of studio mode."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        console.out.print('Studio mode is enabled.')
    else:
        console.out.print('Studio mode is disabled.')
