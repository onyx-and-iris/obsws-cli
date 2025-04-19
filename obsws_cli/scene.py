"""module containing commands for controlling OBS scenes."""

import obsws_python as obsws
import typer

from .alias import AliasGroup
from .errors import ObswsCliBadParameter

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scenes."""
    resp = ctx.obj['obsws'].get_scene_list()
    scenes = (scene.get('sceneName') for scene in reversed(resp.scenes))
    typer.echo('\n'.join(scenes))


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current program scene."""
    resp = ctx.obj['obsws'].get_current_program_scene()
    typer.echo(resp.current_program_scene_name)


@app.command('switch | set')
def switch(ctx: typer.Context, scene_name: str):
    """Switch to a scene."""
    try:
        ctx.obj['obsws'].set_current_program_scene(scene_name)
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(f"Scene '{scene_name}' not found.")
        raise
