"""module containing commands for manipulating groups in scenes."""

from typing import Annotated, Optional

import typer
from rich.table import Table

from . import console, util, validate
from .alias import SubTyperAliasGroup
from .protocols import DataclassProtocol

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control groups in OBS scenes."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
    scene_name: Annotated[
        Optional[str],
        typer.Argument(
            show_default='The current scene',
            help='Scene name to list groups for',
        ),
    ] = None,
):
    """List groups in a scene."""
    if not scene_name:
        scene_name = ctx.obj.get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    groups = [
        (item.get('sceneItemId'), item.get('sourceName'), item.get('sceneItemEnabled'))
        for item in resp.scene_items
        if item.get('isGroup')
    ]

    if not groups:
        console.out.print(f"No groups found in scene '{scene_name}'.")
        raise typer.Exit()

    table = Table(title=f'Groups in Scene: {scene_name}', padding=(0, 2))

    columns = [
        ('ID', 'center', 'cyan'),
        ('Group Name', 'left', 'cyan'),
        ('Enabled', 'center', None),
    ]
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for item_id, group_name, is_enabled in groups:
        table.add_row(
            str(item_id),
            group_name,
            util.check_mark(is_enabled),
        )

    console.out.print(table)


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
def show(
    ctx: typer.Context,
    scene_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Scene name the group is in'),
    ],
    group_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Group name to show')
    ],
):
    """Show a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        console.err.print(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].'
        )
        raise typer.Exit(1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=True,
    )

    console.out.print(f'Group [green]{group_name}[/green] is now visible.')


@app.command('hide | h')
def hide(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the group is in')
    ],
    group_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Group name to hide')
    ],
):
    """Hide a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        console.err.print(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].'
        )
        raise typer.Exit(1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=False,
    )

    console.out.print(f'Group [green]{group_name}[/green] is now hidden.')


@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the group is in')
    ],
    group_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Group name to toggle')
    ],
):
    """Toggle a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        console.err.print(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].'
        )
        raise typer.Exit(1)

    new_state = not group.get('sceneItemEnabled')
    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=new_state,
    )

    if new_state:
        console.out.print(f'Group [green]{group_name}[/green] is now visible.')
    else:
        console.out.print(f'Group [green]{group_name}[/green] is now hidden.')


@app.command('status | ss')
def status(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the group is in')
    ],
    group_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Group name to check status')
    ],
):
    """Get the status of a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        console.err.print(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].'
        )
        raise typer.Exit(1)

    enabled = ctx.obj.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
    )

    if enabled.scene_item_enabled:
        console.out.print(f'Group [green]{group_name}[/green] is now visible.')
    else:
        console.out.print(f'Group [green]{group_name}[/green] is now hidden.')
