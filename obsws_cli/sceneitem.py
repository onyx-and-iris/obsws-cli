"""module containing commands for manipulating items in scenes."""

from typing import Annotated, Optional

from cyclopts import App, Parameter
from rich.table import Table

from . import console, util, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='sceneitem', help='Commands for controlling scene items in OBS.')


@app.command(name=['list', 'ls'])
def list_(
    scene_name: Optional[str] = None,
    /,
    uuid: bool = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List all items in a scene.

    Parameters
    ----------
    scene_name : str, optional
        The name of the scene to list items for. If not provided, the current program scene
        will be used.
    uuid : bool
        Show UUIDs of scene items.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    if not scene_name:
        scene_name = ctx.client.get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            exit_code=ExitCode.ERROR,
        )

    resp = ctx.client.get_scene_item_list(scene_name)
    items = sorted(
        (
            (
                item.get('sceneItemId'),
                item.get('sourceName'),
                item.get('isGroup'),
                item.get('sceneItemEnabled'),
                item.get('sourceUuid', 'N/A'),  # Include source UUID
            )
            for item in resp.scene_items
        ),
        key=lambda x: x[0],  # Sort by sceneItemId
    )

    if not items:
        raise OBSWSCLIError(
            f'No items found in scene [yellow]{scene_name}[/yellow].',
            exit_code=ExitCode.SUCCESS,
        )

    table = Table(
        title=f'Items in Scene: {scene_name}',
        padding=(0, 2),
        border_style=ctx.style.border,
    )
    if uuid:
        columns = [
            ('Item ID', 'center', ctx.style.column),
            ('Item Name', 'left', ctx.style.column),
            ('In Group', 'left', ctx.style.column),
            ('Enabled', 'center', None),
            ('UUID', 'left', ctx.style.column),
        ]
    else:
        columns = [
            ('Item ID', 'center', ctx.style.column),
            ('Item Name', 'left', ctx.style.column),
            ('In Group', 'left', ctx.style.column),
            ('Enabled', 'center', None),
        ]
    # Add columns to the table
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

    for item_id, item_name, is_group, is_enabled, source_uuid in items:
        if is_group:
            resp = ctx.client.get_group_scene_item_list(item_name)
            group_items = sorted(
                (
                    (
                        gi.get('sceneItemId'),
                        gi.get('sourceName'),
                        gi.get('sceneItemEnabled'),
                        gi.get('sourceUuid', 'N/A'),  # Include source UUID
                    )
                    for gi in resp.scene_items
                ),
                key=lambda x: x[0],  # Sort by sceneItemId
            )
            for (
                group_item_id,
                group_item_name,
                group_item_enabled,
                group_item_source_uuid,
            ) in group_items:
                if uuid:
                    table.add_row(
                        str(group_item_id),
                        group_item_name,
                        item_name,
                        util.check_mark(is_enabled and group_item_enabled),
                        group_item_source_uuid,
                    )
                else:
                    table.add_row(
                        str(group_item_id),
                        group_item_name,
                        item_name,
                        util.check_mark(is_enabled and group_item_enabled),
                    )
        else:
            if uuid:
                table.add_row(
                    str(item_id),
                    item_name,
                    '',
                    util.check_mark(is_enabled),
                    source_uuid,
                )
            else:
                table.add_row(
                    str(item_id),
                    item_name,
                    '',
                    util.check_mark(is_enabled),
                )

    console.out.print(table)


def _validate_sources(
    ctx: Context,
    scene_name: str,
    item_name: str,
    group: Optional[str] = None,
):
    """Validate the scene name and item name."""
    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            exit_code=ExitCode.ERROR,
        )

    if group:
        if not validate.item_in_scene_item_list(ctx, scene_name, group):
            raise OBSWSCLIError(
                f'Group [yellow]{group}[/yellow] not found in scene [yellow]{scene_name}[/yellow].',
                exit_code=ExitCode.ERROR,
            )
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            raise OBSWSCLIError(
                f'Item [yellow]{item_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow]. Is the item in a group? '
                f'If so use the [yellow]--group[/yellow] option to specify the parent group.\n'
                'Use [yellow]obsws-cli sceneitem ls[/yellow] for a list of items in the scene.',
                exit_code=ExitCode.ERROR,
            )


def _get_scene_name_and_item_id(
    ctx: Context,
    scene_name: str,
    item_name: str,
    group: Optional[str] = None,
):
    """Get the scene name and item ID for the given scene and item name."""
    if group:
        resp = ctx.client.get_group_scene_item_list(group)
        for item in resp.scene_items:
            if item.get('sourceName') == item_name:
                scene_name = group
                scene_item_id = item.get('sceneItemId')
                break
        else:
            raise OBSWSCLIError(
                f'Item [yellow]{item_name}[/yellow] not found in group [yellow]{group}[/yellow].',
                exit_code=ExitCode.ERROR,
            )
    else:
        resp = ctx.client.get_scene_item_id(scene_name, item_name)
        scene_item_id = resp.scene_item_id

    return scene_name, scene_item_id


@app.command(name=['show', 'sh'])
def show(
    scene_name: str,
    item_name: str,
    /,
    group: Optional[str] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Show an item in a scene.

    Parameters
    ----------
    scene_name : str
        The name of the scene the item is in.
    item_name : str
        The name of the item to show in the scene.
    group : str, optional
        The name of the parent group the item is in, if applicable.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    _validate_sources(ctx, scene_name, item_name, group)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=True,
    )

    if group:
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} '
            f'in scene {console.highlight(ctx, old_scene_name)} has been shown.'
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} has been shown.'
        )


@app.command(name=['hide', 'h'])
def hide(
    scene_name: str,
    item_name: str,
    /,
    group: Optional[str] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Hide an item in a scene.

    Parameters
    ----------
    scene_name : str
        The name of the scene the item is in.
    item_name : str
        The name of the item to hide in the scene.
    group : str, optional
        The name of the parent group the item is in, if applicable.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    _validate_sources(ctx, scene_name, item_name, group)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=False,
    )

    if group:
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} in scene {console.highlight(ctx, old_scene_name)} has been hidden.'
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} has been hidden.'
        )


@app.command(name=['toggle', 'tg'])
def toggle(
    scene_name: str,
    item_name: str,
    /,
    group: Optional[str] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Toggle an item in a scene.

    Parameters
    ----------
    scene_name : str
        The name of the scene the item is in.
    item_name : str
        The name of the item to toggle in the scene.
    group : str, optional
        The name of the parent group the item is in, if applicable.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    _validate_sources(ctx, scene_name, item_name, group)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    enabled = ctx.client.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
    )
    new_state = not enabled.scene_item_enabled

    ctx.client.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=new_state,
    )

    if group:
        if new_state:
            console.out.print(
                f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} '
                f'in scene {console.highlight(ctx, old_scene_name)} has been shown.'
            )
        else:
            console.out.print(
                f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} '
                f'in scene {console.highlight(ctx, old_scene_name)} has been hidden.'
            )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        if new_state:
            console.out.print(
                f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} has been shown.'
            )
        else:
            console.out.print(
                f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} has been hidden.'
            )


@app.command(name=['visible', 'v'])
def visible(
    scene_name: str,
    item_name: str,
    /,
    group: Optional[str] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Check if an item in a scene is visible.

    Parameters
    ----------
    scene_name : str
        The name of the scene the item is in.
    item_name : str
        The name of the item to check visibility in the scene.
    group : str, optional
        The name of the parent group the item is in, if applicable.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    _validate_sources(ctx, scene_name, item_name, group)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    enabled = ctx.client.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
    )

    if group:
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} '
            f'in scene {console.highlight(ctx, old_scene_name)} is currently {"visible" if enabled.scene_item_enabled else "hidden"}.'
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} '
            f'is currently {"visible" if enabled.scene_item_enabled else "hidden"}.'
        )


@app.command(name=['transform', 't'])
def transform(
    scene_name: str,
    item_name: str,
    /,
    group: Optional[str] = None,
    alignment: Optional[int] = None,
    bounds_alignment: Optional[int] = None,
    bounds_height: Optional[float] = None,
    bounds_type: Optional[str] = None,
    bounds_width: Optional[float] = None,
    crop_to_bounds: Optional[bool] = None,
    crop_bottom: Optional[float] = None,
    crop_left: Optional[float] = None,
    crop_right: Optional[float] = None,
    crop_top: Optional[float] = None,
    position_x: Optional[float] = None,
    position_y: Optional[float] = None,
    rotation: Optional[float] = None,
    scale_x: Optional[float] = None,
    scale_y: Optional[float] = None,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Set the transform of an item in a scene.

    Parameters
    ----------
    scene_name : str
        The name of the scene the item is in.
    item_name : str
        The name of the item to transform in the scene.
    group : str, optional
        The name of the parent group the item is in, if applicable.
    alignment : int, optional
        Alignment of the item in the scene.
    bounds_alignment : int, optional
        Bounds alignment of the item in the scene.
    bounds_height : float, optional
        Height of the item in the scene.
    bounds_type : str, optional
        Type of bounds for the item in the scene.
    bounds_width : float, optional
        Width of the item in the scene.
    crop_to_bounds : bool, optional
        Crop the item to the bounds.
    crop_bottom : float, optional
        Bottom crop of the item in the scene.
    crop_left : float, optional
        Left crop of the item in the scene.
    crop_right : float, optional
        Right crop of the item in the scene.
    crop_top : float, optional
        Top crop of the item in the scene.
    position_x : float, optional
        X position of the item in the scene.
    position_y : float, optional
        Y position of the item in the scene.
    rotation : float, optional
        Rotation of the item in the scene.
    scale_x : float, optional
        X scale of the item in the scene.
    scale_y : float, optional
        Y scale of the item in the scene.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    _validate_sources(ctx, scene_name, item_name, group)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    transform = {}
    if alignment is not None:
        transform['alignment'] = alignment
    if bounds_alignment is not None:
        transform['boundsAlignment'] = bounds_alignment
    if bounds_height is not None:
        transform['boundsHeight'] = bounds_height
    if bounds_type is not None:
        transform['boundsType'] = bounds_type
    if bounds_width is not None:
        transform['boundsWidth'] = bounds_width
    if crop_to_bounds is not None:
        transform['cropToBounds'] = crop_to_bounds
    if crop_bottom is not None:
        transform['cropBottom'] = crop_bottom
    if crop_left is not None:
        transform['cropLeft'] = crop_left
    if crop_right is not None:
        transform['cropRight'] = crop_right
    if crop_top is not None:
        transform['cropTop'] = crop_top
    if position_x is not None:
        transform['positionX'] = position_x
    if position_y is not None:
        transform['positionY'] = position_y
    if rotation is not None:
        transform['rotation'] = rotation
    if scale_x is not None:
        transform['scaleX'] = scale_x
    if scale_y is not None:
        transform['scaleY'] = scale_y

    if not transform:
        raise OBSWSCLIError(
            'No transform options provided. Use at least one of the transform options.',
            exit_code=ExitCode.ERROR,
        )

    transform = ctx.client.set_scene_item_transform(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        transform=transform,
    )

    if group:
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in group {console.highlight(ctx, group)} '
            f'in scene {console.highlight(ctx, old_scene_name)} has been transformed.'
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        console.out.print(
            f'Item {console.highlight(ctx, item_name)} in scene {console.highlight(ctx, scene_name)} has been transformed.'
        )
