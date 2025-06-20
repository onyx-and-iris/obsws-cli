"""module containing commands for controlling OBS scenes."""

from typing import Annotated

import typer
from rich.table import Table

from . import console, util, validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS scenes."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
    uuid: Annotated[bool, typer.Option(help='Show UUIDs of scenes')] = False,
):
    """List all scenes."""
    resp = ctx.obj.get_scene_list()
    scenes = (
        (scene.get('sceneName'), scene.get('sceneUuid'))
        for scene in reversed(resp.scenes)
    )

    active_scene = ctx.obj.get_current_program_scene().scene_name

    table = Table(title='Scenes', padding=(0, 2))
    if uuid:
        columns = [
            ('Scene Name', 'left', 'cyan'),
            ('Active', 'center', None),
            ('UUID', 'left', 'cyan'),
        ]
    else:
        table.title += ' (UUIDs hidden)'
        columns = [
            ('Scene Name', 'left', 'cyan'),
            ('Active', 'center', None),
        ]
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for scene_name, scene_uuid in scenes:
        if scene_name == active_scene:
            scene_output = f'[bold]{scene_name}[/bold]'
        else:
            scene_output = f'[dim]{scene_name}[/dim]'

        if uuid:
            table.add_row(
                scene_output,
                util.check_mark(scene_name == active_scene, empty_if_false=True),
                scene_uuid,
            )
        else:
            table.add_row(
                scene_output,
                util.check_mark(scene_name == active_scene, empty_if_false=True),
            )

    console.out.print(table)


@app.command('current | get')
def current(
    ctx: typer.Context,
    preview: Annotated[
        bool, typer.Option(help='Get the preview scene instead of the program scene')
    ] = False,
):
    """Get the current program scene or preview scene."""
    if preview and not validate.studio_mode_enabled(ctx):
        console.err.print('Studio mode is not enabled, cannot get preview scene.')
        raise typer.Exit(1)

    if preview:
        resp = ctx.obj.get_current_preview_scene()
        console.out.print(resp.current_preview_scene_name)
    else:
        resp = ctx.obj.get_current_program_scene()
        console.out.print(resp.current_program_scene_name)


@app.command('switch | set')
def switch(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., help='Name of the scene to switch to')
    ],
    preview: Annotated[
        bool,
        typer.Option(help='Switch to the preview scene instead of the program scene'),
    ] = False,
):
    """Switch to a scene."""
    if preview and not validate.studio_mode_enabled(ctx):
        console.err.print('Studio mode is not enabled, cannot set the preview scene.')
        raise typer.Exit(1)

    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)

    if preview:
        ctx.obj.set_current_preview_scene(scene_name)
        console.out.print(f'Switched to preview scene: [green]{scene_name}[/green]')
    else:
        ctx.obj.set_current_program_scene(scene_name)
        console.out.print(f'Switched to program scene: [green]{scene_name}[/green]')
