"""module containing commands for manipulating studio mode in OBS."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control studio mode in OBS."""


@app.command('enable | on')
def enable(ctx: typer.Context):
    """Enable studio mode."""
    ctx.obj.set_studio_mode_enabled(True)
    typer.echo('Studio mode has been enabled.')


@app.command('disable | off')
def disable(ctx: typer.Context):
    """Disable studio mode."""
    ctx.obj.set_studio_mode_enabled(False)
    typer.echo('Studio mode has been disabled.')


@app.command('toggle | tg')
def toggle(ctx: typer.Context):
    """Toggle studio mode."""
    resp = ctx.obj.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        ctx.obj.set_studio_mode_enabled(False)
        typer.echo('Studio mode is now disabled.')
    else:
        ctx.obj.set_studio_mode_enabled(True)
        typer.echo('Studio mode is now enabled.')


@app.command('status | ss')
def status(ctx: typer.Context):
    """Get the status of studio mode."""
    resp = ctx.obj.get_studio_mode_enabled()
    if resp.studio_mode_enabled:
        typer.echo('Studio mode is enabled.')
    else:
        typer.echo('Studio mode is disabled.')
