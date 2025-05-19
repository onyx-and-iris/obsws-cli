"""module containing commands for controlling OBS scenes."""

from typing import Annotated

import typer

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scenes."""
    resp = ctx.obj.get_scene_list()
    scenes = (scene.get('sceneName') for scene in reversed(resp.scenes))
    typer.echo('\n'.join(scenes))


@app.command('current | get')
def current(
    ctx: typer.Context,
    preview: Annotated[
        bool, typer.Option(help='Get the preview scene instead of the program scene')
    ] = False,
):
    """Get the current program scene or preview scene."""
    if preview and not validate.studio_mode_enabled(ctx):
        typer.echo('Studio mode is not enabled, cannot get preview scene.', err=True)
        raise typer.Exit(1)

    if preview:
        resp = ctx.obj.get_current_preview_scene()
        typer.echo(resp.current_preview_scene_name)
    else:
        resp = ctx.obj.get_current_program_scene()
        typer.echo(resp.current_program_scene_name)


@app.command('switch | set')
def switch(
    ctx: typer.Context,
    scene_name: str,
    preview: Annotated[
        bool,
        typer.Option(help='Switch to the preview scene instead of the program scene'),
    ] = False,
):
    """Switch to a scene."""
    if preview and not validate.studio_mode_enabled(ctx):
        typer.echo(
            'Studio mode is not enabled, cannot set the preview scene.', err=True
        )
        raise typer.Exit(1)

    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.", err=True)
        raise typer.Exit(1)

    if preview:
        ctx.obj.set_current_preview_scene(scene_name)
        typer.echo(f'Switched to preview scene: {scene_name}')
    else:
        ctx.obj.set_current_program_scene(scene_name)
        typer.echo(f'Switched to program scene: {scene_name}')
