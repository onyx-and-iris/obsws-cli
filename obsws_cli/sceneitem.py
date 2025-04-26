"""module containing commands for manipulating items in scenes."""

from collections.abc import Callable
from typing import Annotated

import typer

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control items in OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context, scene_name: str):
    """List all items in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.")
        typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    items = (item.get('sourceName') for item in resp.scene_items)
    typer.echo('\n'.join(items))


def _validate_scene_name_and_item_name(
    func: Callable,
):
    """Validate the scene name and item name."""

    def wrapper(
        ctx: typer.Context, scene_name: str, item_name: str, parent: bool = False
    ):
        if not validate.scene_in_scenes(ctx, scene_name):
            typer.echo(f"Scene '{scene_name}' not found.")
            raise typer.Exit(code=1)

        if parent:
            if not validate.item_in_scene_item_list(ctx, scene_name, parent):
                typer.echo(
                    f"Parent group '{parent}' not found in scene '{scene_name}'."
                )
                raise typer.Exit(code=1)
        else:
            if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
                typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
                raise typer.Exit(code=1)

        return func(ctx, scene_name, item_name, parent)

    return wrapper


def _get_scene_name_and_item_id(
    ctx: typer.Context, scene_name: str, item_name: str, parent: str
):
    if parent:
        resp = ctx.obj.get_group_scene_item_list(parent)
        for item in resp.scene_items:
            if item.get('sourceName') == item_name:
                scene_name = parent
                scene_item_id = item.get('sceneItemId')
                break
        else:
            typer.echo(f"Item '{item_name}' not found in group '{parent}'.")
            raise typer.Exit(code=1)
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
    parent: Annotated[str, typer.Option(help='Parent group name')] = None,
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
    parent: Annotated[str, typer.Option(help='Parent group name')] = None,
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
    parent: Annotated[str, typer.Option(help='Parent group name')] = None,
):
    """Toggle an item in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.")
        raise typer.Exit(code=1)

    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(f"Parent group '{parent}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)

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
    parent: Annotated[str, typer.Option(help='Parent group name')] = None,
):
    """Check if an item in a scene is visible."""
    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(f"Parent group '{parent}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)

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
    parent: Annotated[str, typer.Option(help='Parent group name')] = None,
    position_x: Annotated[
        float, typer.Option(help='X position of the item in the scene')
    ] = None,
    position_y: Annotated[
        float, typer.Option(help='Y position of the item in the scene')
    ] = None,
    scale_x: Annotated[
        float, typer.Option(help='X scale of the item in the scene')
    ] = None,
    scale_y: Annotated[
        float, typer.Option(help='Y scale of the item in the scene')
    ] = None,
):
    """Set the transform of an item in a scene."""
    if parent:
        if not validate.item_in_scene_item_list(ctx, scene_name, parent):
            typer.echo(f"Parent group '{parent}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)
    else:
        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)

    old_scene_name = scene_name
    scene_name, scene_item_id = _get_scene_name_and_item_id(
        ctx, scene_name, item_name, parent
    )

    transform = {}
    if position_x is not None:
        transform['positionX'] = position_x
    if position_y is not None:
        transform['positionY'] = position_y
    if scale_x is not None:
        transform['scaleX'] = scale_x
    if scale_y is not None:
        transform['scaleY'] = scale_y

    if not transform:
        typer.echo('No transform options provided.')
        raise typer.Exit(code=1)

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
