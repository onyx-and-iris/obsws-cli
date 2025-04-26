"""module containing commands for manipulating groups in scenes."""

import typer

from . import validate
from .alias import AliasGroup
from .protocols import DataclassProtocol

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control groups in OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context, scene_name: str):
    """List groups in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    groups = (
        item.get('sourceName') for item in resp.scene_items if item.get('isGroup')
    )
    typer.echo('\n'.join(groups))


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
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=True,
    )

    typer.echo(f"Group '{group_name}' is now visible.")


@app.command('hide | h')
def hide(ctx: typer.Context, scene_name: str, group_name: str):
    """Hide a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=False,
    )

    typer.echo(f"Group '{group_name}' is now hidden.")


@app.command('toggle | tg')
def toggle(ctx: typer.Context, scene_name: str, group_name: str):
    """Toggle a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    new_state = not group.get('sceneItemEnabled')
    ctx.obj.set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=new_state,
    )

    if new_state:
        typer.echo(f"Group '{group_name}' is now visible.")
    else:
        typer.echo(f"Group '{group_name}' is now hidden.")


@app.command('status | ss')
def status(ctx: typer.Context, scene_name: str, group_name: str):
    """Get the status of a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    enabled = ctx.obj.get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
    )

    if enabled.scene_item_enabled:
        typer.echo(f"Group '{group_name}' is now visible.")
    else:
        typer.echo(f"Group '{group_name}' is now hidden.")
