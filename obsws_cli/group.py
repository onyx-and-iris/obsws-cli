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

    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
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


@app.command()
def show(ctx: typer.Context, scene_name: str, group_name: str):
    """Show a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj['obsws'].set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=True,
    )


@app.command()
def hide(ctx: typer.Context, scene_name: str, group_name: str):
    """Hide a group in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(
            f"Scene '{scene_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
    if (group := _get_group(group_name, resp)) is None:
        typer.echo(
            f"Group '{group_name}' not found in scene {scene_name}.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj['obsws'].set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(group.get('sceneItemId')),
        enabled=False,
    )
