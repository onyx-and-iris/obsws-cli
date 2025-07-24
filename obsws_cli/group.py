"""module containing commands for manipulating groups in scenes."""

from typing import Annotated, Optional

from cyclopts import App, Argument, Parameter
from rich.table import Table
from rich.text import Text

from . import console, util, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError
from .protocols import DataclassProtocol

app = App(name='group', help='Commands for managing groups in OBS scenes')


@app.command(name=['list', 'ls'])
def list_(
    scene_name: Annotated[
        Optional[str],
        Argument(
            hint='Scene name to list groups for',
        ),
    ] = None,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List groups in a scene."""
    if not scene_name:
        scene_name = ctx.client.get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    groups = [
        (item.get('sceneItemId'), item.get('sourceName'), item.get('sceneItemEnabled'))
        for item in resp.scene_items
        if item.get('isGroup')
    ]

    if not groups:
        raise OBSWSCLIError(
            f'No groups found in scene {console.highlight(ctx, scene_name)}.',
            code=ExitCode.SUCCESS,
        )

    table = Table(
        title=f'Groups in Scene: {scene_name}',
        padding=(0, 2),
        border_style=ctx.style.border,
    )

    columns = [
        (Text('ID', justify='center'), 'center', ctx.style.column),
        (Text('Group Name', justify='center'), 'left', ctx.style.column),
        (Text('Enabled', justify='center'), 'center', None),
    ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

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


@app.command(name=['show', 'sh'])
def show(
    scene_name: Annotated[
        str,
        Argument(hint='Scene name the group is in'),
    ],
    group_name: Annotated[str, Argument(hint='Group name to show')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Show a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        raise OBSWSCLIError(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].',
            code=ExitCode.ERROR,
        )

    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=True,
    )

    console.out.print(f'Group {console.highlight(ctx, group_name)} is now visible.')


@app.command(name=['hide', 'h'])
def hide(
    scene_name: Annotated[str, Argument(hint='Scene name the group is in')],
    group_name: Annotated[str, Argument(hint='Group name to hide')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Hide a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        raise OBSWSCLIError(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].',
            code=ExitCode.ERROR,
        )

    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=False,
    )

    console.out.print(f'Group {console.highlight(ctx, group_name)} is now hidden.')


@app.command(name=['toggle', 'tg'])
def toggle(
    scene_name: Annotated[str, Argument(hint='Scene name the group is in')],
    group_name: Annotated[str, Argument(hint='Group name to toggle')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        raise OBSWSCLIError(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].',
            code=ExitCode.ERROR,
        )

    new_state = not group.get('sceneItemEnabled')
    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=new_state,
    )

    if new_state:
        console.out.print(f'Group {console.highlight(ctx, group_name)} is now visible.')
    else:
        console.out.print(f'Group {console.highlight(ctx, group_name)} is now hidden.')


@app.command(name=['status', 'ss'])
def status(
    scene_name: Annotated[str, Argument(hint='Scene name the group is in')],
    group_name: Annotated[str, Argument(hint='Group name to check status')],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the status of a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        raise OBSWSCLIError(
            f'Group [yellow]{group_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow].',
            code=ExitCode.ERROR,
        )

    enabled = ctx.client.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
    )

    if enabled.scene_item_enabled:
        console.out.print(f'Group {console.highlight(ctx, group_name)} is now visible.')
    else:
        console.out.print(f'Group {console.highlight(ctx, group_name)} is now hidden.')
