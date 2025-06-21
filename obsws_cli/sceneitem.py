"""module containing commands for manipulating items in scenes."""

from typing import Annotated, Optional

import typer
from rich.table import Table

from . import console, util, validate
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control items in OBS scenes."""


@app.command('list | ls')
def list_(
    ctx: typer.Context,
    scene_name: Annotated[
        Optional[str],
        typer.Argument(
            show_default='The current scene',
            help='Scene name to list items for',
        ),
    ] = None,
    uuid: Annotated[bool, typer.Option(help='Show UUIDs of scene items')] = False,
):
    """List all items in a scene."""
    if not scene_name:
        scene_name = ctx.obj['obsws'].get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
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
        console.out.print(
            f'No items found in scene {console.highlight(ctx, scene_name)}.'
        )
        raise typer.Exit()

    table = Table(
        title=f'Items in Scene: {scene_name}',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    if uuid:
        columns = [
            ('Item ID', 'center', ctx.obj['style'].column),
            ('Item Name', 'left', ctx.obj['style'].column),
            ('In Group', 'left', ctx.obj['style'].column),
            ('Enabled', 'center', None),
            ('UUID', 'left', ctx.obj['style'].column),
        ]
    else:
        columns = [
            ('Item ID', 'center', ctx.obj['style'].column),
            ('Item Name', 'left', ctx.obj['style'].column),
            ('In Group', 'left', ctx.obj['style'].column),
            ('Enabled', 'center', None),
        ]
    # Add columns to the table
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for item_id, item_name, is_group, is_enabled, source_uuid in items:
        if is_group:
            resp = ctx.obj['obsws'].get_group_scene_item_list(item_name)
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
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    group: Optional[str] = None,
) -> bool:
    """Validate the scene name and item name."""
    if not validate.scene_in_scenes(ctx, scene_name):
        console.err.print(f'Scene [yellow]{scene_name}[/yellow] not found.')
        return False

    if group:
        if not validate.item_in_scene_item_list(ctx, scene_name, group):
            console.err.print(
                f'Group [yellow]{group}[/yellow] not found in scene [yellow]{scene_name}[/yellow].'
            )
            return False
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            console.err.print(
                f'Item [yellow]{item_name}[/yellow] not found in scene [yellow]{scene_name}[/yellow]. Is the item in a group? '
                f'If so use the [yellow]--group[/yellow] option to specify the parent group.\n'
                'Use [yellow]obsws-cli sceneitem ls[/yellow] for a list of items in the scene.'
            )
            return False

    return True


def _get_scene_name_and_item_id(
    ctx: typer.Context, scene_name: str, item_name: str, group: Optional[str] = None
):
    """Get the scene name and item ID for the given scene and item name."""
    if group:
        resp = ctx.obj['obsws'].get_group_scene_item_list(group)
        for item in resp.scene_items:
            if item.get('sourceName') == item_name:
                scene_name = group
                scene_item_id = item.get('sceneItemId')
                break
        else:
            console.err.print(
                f'Item [yellow]{item_name}[/yellow] not found in group [yellow]{group}[/yellow].'
            )
            raise typer.Exit(1)
    else:
        resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)
        scene_item_id = resp.scene_item_id

    return scene_name, scene_item_id


@app.command('show | sh')
def show(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the item is in')
    ],
    item_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Item name to show in the scene'),
    ],
    group: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Show an item in a scene."""
    if not _validate_sources(ctx, scene_name, item_name, group):
        raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    ctx.obj['obsws'].set_scene_item_enabled(
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


@app.command('hide | h')
def hide(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the item is in')
    ],
    item_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Item name to hide in the scene'),
    ],
    group: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Hide an item in a scene."""
    if not _validate_sources(ctx, scene_name, item_name, group):
        raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    ctx.obj['obsws'].set_scene_item_enabled(
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


@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the item is in')
    ],
    item_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='Item name to toggle in the scene'
        ),
    ],
    group: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Toggle an item in a scene."""
    if not _validate_sources(ctx, scene_name, item_name, group):
        raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    enabled = ctx.obj['obsws'].get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
    )
    new_state = not enabled.scene_item_enabled

    ctx.obj['obsws'].set_scene_item_enabled(
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


@app.command('visible | v')
def visible(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the item is in')
    ],
    item_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='Item name to check visibility in the scene'
        ),
    ],
    group: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Check if an item in a scene is visible."""
    if not _validate_sources(ctx, scene_name, item_name, group):
        raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, group
    )

    enabled = ctx.obj['obsws'].get_scene_item_enabled(
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


@app.command('transform | t')
def transform(
    ctx: typer.Context,
    scene_name: Annotated[
        str, typer.Argument(..., show_default=False, help='Scene name the item is in')
    ],
    item_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='Item name to transform in the scene'
        ),
    ],
    group: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
    alignment: Annotated[
        Optional[int], typer.Option(help='Alignment of the item in the scene')
    ] = None,
    bounds_alignment: Annotated[
        Optional[int], typer.Option(help='Bounds alignment of the item in the scene')
    ] = None,
    bounds_height: Annotated[
        Optional[float], typer.Option(help='Height of the item in the scene')
    ] = None,
    bounds_type: Annotated[
        Optional[str], typer.Option(help='Type of bounds for the item in the scene')
    ] = None,
    bounds_width: Annotated[
        Optional[float], typer.Option(help='Width of the item in the scene')
    ] = None,
    crop_to_bounds: Annotated[
        Optional[bool], typer.Option(help='Crop the item to the bounds')
    ] = None,
    crop_bottom: Annotated[
        Optional[float], typer.Option(help='Bottom crop of the item in the scene')
    ] = None,
    crop_left: Annotated[
        Optional[float], typer.Option(help='Left crop of the item in the scene')
    ] = None,
    crop_right: Annotated[
        Optional[float], typer.Option(help='Right crop of the item in the scene')
    ] = None,
    crop_top: Annotated[
        Optional[float], typer.Option(help='Top crop of the item in the scene')
    ] = None,
    position_x: Annotated[
        Optional[float], typer.Option(help='X position of the item in the scene')
    ] = None,
    position_y: Annotated[
        Optional[float], typer.Option(help='Y position of the item in the scene')
    ] = None,
    rotation: Annotated[
        Optional[float], typer.Option(help='Rotation of the item in the scene')
    ] = None,
    scale_x: Annotated[
        Optional[float], typer.Option(help='X scale of the item in the scene')
    ] = None,
    scale_y: Annotated[
        Optional[float], typer.Option(help='Y scale of the item in the scene')
    ] = None,
):
    """Set the transform of an item in a scene."""
    if not _validate_sources(ctx, scene_name, item_name, group):
        raise typer.Exit(1)

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
        console.err.print('No transform options provided.')
        raise typer.Exit(1)

    transform = ctx.obj['obsws'].set_scene_item_transform(
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
