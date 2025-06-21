"""module containing commands for manipulating studio mode in OBS."""

import typer

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control studio mode in OBS."""


@app.command('enable | on')
def enable(ctx: typer.Context):
    """Enable studio mode."""
    ctx.obj['obsws'].set_studio_mode_enabled(True)
    console.out.print('Studio mode has been enabled.')


@app.command('disable | off')
def disable(ctx: typer.Context):
    """Disable studio mode."""
    ctx.obj['obsws'].set_studio_mode_enabled(False)
    console.out.print('Studio mode has been disabled.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle studio mode."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        ctx.obj['obsws'].set_studio_mode_enabled(False)
        console.out.print('Studio mode is now disabled.')
    else:
        ctx.obj['obsws'].set_studio_mode_enabled(True)
        console.out.print('Studio mode is now enabled.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of studio mode."""
    resp = ctx.obj['obsws'].get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        console.out.print('Studio mode is enabled.')
    else:
        console.out.print('Studio mode is disabled.')
