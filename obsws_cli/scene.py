"""module containing commands for controlling OBS scenes."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scenes."""
    resp = ctx.obj.get_scene_list()
    scenes = (
        (scene.get('sceneName'), scene.get('sceneUuid'))
        for scene in reversed(resp.scenes)
    )

    table = Table(title='Scenes', padding=(0, 2))
    for column in ('Scene Name', 'UUID'):
        table.add_column(column, justify='left', style='cyan')

    for scene_name, scene_uuid in scenes:
        table.add_row(
            scene_name,
            scene_uuid,
        )

    out_console.print(table)


@app.command('current | get')
def current(
    ctx: typer.Context,
    preview: Annotated[
        bool, typer.Option(help='Get the preview scene instead of the program scene')
    ] = False,
):
    """Get the current program scene or preview scene."""
    if preview and not validate.studio_mode_enabled(ctx):
        err_console.print('Studio mode is not enabled, cannot get preview scene.')
        raise typer.Exit(1)

    if preview:
        resp = ctx.obj.get_current_preview_scene()
        out_console.print(resp.current_preview_scene_name)
    else:
        resp = ctx.obj.get_current_program_scene()
        out_console.print(resp.current_program_scene_name)


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
        err_console.print('Studio mode is not enabled, cannot set the preview scene.')
        raise typer.Exit(1)

    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    if preview:
        ctx.obj.set_current_preview_scene(scene_name)
        out_console.print(f'Switched to preview scene: {scene_name}')
    else:
        ctx.obj.set_current_program_scene(scene_name)
        out_console.print(f'Switched to program scene: {scene_name}')
