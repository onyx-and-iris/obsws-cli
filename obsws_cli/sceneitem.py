"""module containing commands for manipulating items in scenes."""

from collections.abc import Callable
from typing import Annotated, Optional

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
    """Control items in OBS scenes."""


@app.command('list | ls')
def list(
    ctx: typer.Context,
    scene_name: str = typer.Argument(
        None, help='Scene name (optional, defaults to current scene)'
    ),
):
    """List all items in a scene."""
    if not scene_name:
        scene_name = ctx.obj.get_current_program_scene().scene_name

    if not validate.scene_in_scenes(ctx, scene_name):
        err_console.print(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    items = [item.get('sourceName') for item in resp.scene_items]

    if not items:
        err_console.print(f"No items found in scene '{scene_name}'.")
        raise typer.Exit(1)

    table = Table(title=f'Items in Scene: {scene_name}')
    table.add_column('Item Name', justify='left', style='cyan')

    for item in items:
        table.add_row(item)

    out_console.print(table)


def _validate_scene_name_and_item_name(
    func: Callable,
):
    """Validate the scene name and item name."""

    def wrapper(
        ctx: typer.Context,
        scene_name: str,
        item_name: str,
        parent: Optional[str] = None,
    ):
        if not validate.scene_in_scenes(ctx, scene_name):
            typer.echo(f"Scene '{scene_name}' not found.", err=True)
            raise typer.Exit(1)

        if parent:
            if not validate.item_in_scene_item_list(ctx, scene_name, parent):
                typer.echo(
                    f"Parent group '{parent}' not found in scene '{scene_name}'.",
                    err=True,
                )
                raise typer.Exit(1)
        else:
            if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
                typer.echo(
                    f"Item '{item_name}' not found in scene '{scene_name}'.", err=True
                )
                raise typer.Exit(1)

        return func(ctx, scene_name, item_name, parent)

    return wrapper


def _get_scene_name_and_item_id(
    ctx: typer.Context, scene_name: str, item_name: str, parent: Optional[str] = None
):
    if parent:
        resp = ctx.obj.get_group_scene_item_list(parent)
        for item in resp.scene_items:
            if item.get('sourceName') == item_name:
                scene_name = parent
                scene_item_id = item.get('sceneItemId')
                break
        else:
            typer.echo(f"Item '{item_name}' not found in group '{parent}'.", err=True)
            raise typer.Exit(1)
    else:
        resp = ctx.obj.get_scene_item_id(scene_name, item_name)
        scene_item_id = resp.scene_item_id

    return scene_name, scene_item_id


@_validate_scene_name_and_item_name
@app.command('show | sh')
def show(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    parent: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Show an item in a scene."""
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
    )

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=True,
    )

    typer.echo(f"Item '{item_name}' in scene '{scene_name}' has been shown.")


@_validate_scene_name_and_item_name
@app.command('hide | h')
def hide(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    parent: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Hide an item in a scene."""
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
    )

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=False,
    )

    typer.echo(f"Item '{item_name}' in scene '{scene_name}' has been hidden.")


@_validate_scene_name_and_item_name
@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    parent: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Toggle an item in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.")
        raise typer.Exit(1)

    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(
                f"Parent group '{parent}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(
                f"Item '{item_name}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)

    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
    )

    enabled = ctx.obj.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
    )
    new_state = not enabled.scene_item_enabled

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        enabled=new_state,
    )

    typer.echo(
        f"Item '{item_name}' in scene '{scene_name}' has been {'shown' if new_state else 'hidden'}."
    )


@_validate_scene_name_and_item_name
@app.command('visible | v')
def visible(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    parent: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
):
    """Check if an item in a scene is visible."""
    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(
                f"Parent group '{parent}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(
                f"Item '{item_name}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
    )

    enabled = ctx.obj.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(scene_item_id),
    )

    if parent:
        typer.echo(
            f"Item '{item_name}' in group '{parent}' in scene '{old_scene_name}' is currently {'visible' if enabled.scene_item_enabled else 'hidden'}."
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        typer.echo(
            f"Item '{item_name}' in scene '{scene_name}' is currently {'visible' if enabled.scene_item_enabled else 'hidden'}."
        )


@_validate_scene_name_and_item_name
@app.command('transform | t')
def transform(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    parent: Annotated[Optional[str], typer.Option(help='Parent group name')] = None,
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
    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(
                f"Parent group '{parent}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(
                f"Item '{item_name}' not found in scene '{scene_name}'.", err=True
            )
            raise typer.Exit(1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
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
        typer.echo('No transform options provided.', err=True)
        raise typer.Exit(1)

    transform = ctx.obj.set_scene_item_transform(
        scene_name=scene_name,
        item_id=int(scene_item_id),
        transform=transform,
    )

    if parent:
        typer.echo(
            f"Item '{item_name}' in group '{parent}' in scene '{old_scene_name}' has been transformed."
        )
    else:
        # If not in a parent group, just show the scene name
        # This is to avoid confusion with the parent group name
        # which is not the same as the scene name
        # and is not needed in this case
        typer.echo(f"Item '{item_name}' in scene '{scene_name}' has been transformed.")
