"""module containing commands for manipulating groups in scenes."""

import typer
from rich.console import Console
from rich.table import Table

from . import validate
from .alias import AliasGroup
from .protocols import DataclassProtocol

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control groups in OBS scenes."""


@app.command('list | ls')
def list(
    ctx: typer.Context,
    scene_name: str = typer.Argument(
        None, help='Scene name (optional, defaults to current scene)'
    ),
):
    """List groups in a scene."""
    if not scene_name:
        scene_name = ctx.obj.get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    groups = [
        (item.get('sceneItemId'), item.get('sourceName'), item.get('sceneItemEnabled'))
        for item in resp.scene_items
        if item.get('isGroup')
    ]

    if not groups:
        out_console.print(f"No groups found in scene '{scene_name}'.")
        raise typer.Exit()

    table = Table(title=f'Groups in Scene: {scene_name}', padding=(0, 2))

    for column in ('ID', 'Group Name', 'Enabled'):
        table.add_column(
            column, justify='left' if column == 'Group Name' else 'center', style='cyan'
        )

    for item_id, group_name, is_enabled in groups:
        table.add_row(
            str(item_id),
            group_name,
            ':white_heavy_check_mark:' if is_enabled else ':x:',
        )

    out_console.print(table)


def _get_group(group_name: str, resp: DataclassProtocol) -> dict | None:
    """Get a group from the scene item list response."""
    group = next(
        (
            item
            for item in resp.scene_items
            if item.get('sourceName') == group_name and item.get('isGroup')
        ),
        None,
    )
    return group


@app.command('show | sh')
def show(ctx: typer.Context, scene_name: str, group_name: str):
    """Show a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        err_console.print(f"Group '{group_name}' not found in scene {scene_name}.")
        raise typer.Exit(1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=True,
    )

    out_console.print(f"Group '{group_name}' is now visible.")


@app.command('hide | h')
def hide(ctx: typer.Context, scene_name: str, group_name: str):
    """Hide a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        err_console.print(f"Group '{group_name}' not found in scene {scene_name}.")
        raise typer.Exit(1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=False,
    )

    out_console.print(f"Group '{group_name}' is now hidden.")


@app.command('toggle | tg')
def toggle(ctx: typer.Context, scene_name: str, group_name: str):
    """Toggle a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        err_console.print(f"Group '{group_name}' not found in scene {scene_name}.")
        raise typer.Exit(1)

    new_state = not group.get('sceneItemEnabled')
    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=new_state,
    )

    if new_state:
        out_console.print(f"Group '{group_name}' is now visible.")
    else:
        out_console.print(f"Group '{group_name}' is now hidden.")


@app.command('status | ss')
def status(ctx: typer.Context, scene_name: str, group_name: str):
    """Get the status of a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        err_console.print(f"Group '{group_name}' not found in scene {scene_name}.")
        raise typer.Exit(1)

    enabled = ctx.obj.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
    )

    if enabled.scene_item_enabled:
        out_console.print(f"Group '{group_name}' is now visible.")
    else:
        out_console.print(f"Group '{group_name}' is now hidden.")
