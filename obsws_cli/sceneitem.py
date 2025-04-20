"""module containing commands for manipulating items in scenes."""

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

    resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
    items = (item.get('sourceName') for item in resp.scene_items)
    typer.echo('\n'.join(items))


@app.command()
def show(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    validated: Annotated[bool, validate.skipped_option] = False,
):
    """Show an item in a scene."""
    if not validated:
        if not validate.scene_in_scenes(ctx, scene_name):
            typer.echo(f"Scene '{scene_name}' not found.")
            raise typer.Exit(code=1)

        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)

    ctx.obj['obsws'].set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(resp.scene_item_id),
        enabled=True,
    )


@app.command()
def hide(
    ctx: typer.Context,
    scene_name: str,
    item_name: str,
    validated: Annotated[bool, validate.skipped_option] = False,
):
    """Hide an item in a scene."""
    if not validated:
        if not validate.scene_in_scenes(ctx, scene_name):
            typer.echo(f"Scene '{scene_name}' not found.")
            raise typer.Exit(code=1)

        if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
            typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
            raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)
    ctx.obj['obsws'].set_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(resp.scene_item_id),
        enabled=False,
    )


@app.command('toggle | tg')
def toggle(ctx: typer.Context, scene_name: str, item_name: str):
    """Toggle an item in a scene."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.")
        raise typer.Exit(code=1)

    if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
        typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
        raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)
    enabled = ctx.obj['obsws'].get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(resp.scene_item_id),
    )
    if enabled.scene_item_enabled:
        ctx.invoke(
            hide, ctx=ctx, scene_name=scene_name, item_name=item_name, validated=True
        )
    else:
        ctx.invoke(
            show, ctx=ctx, scene_name=scene_name, item_name=item_name, validated=True
        )


@app.command()
def visible(ctx: typer.Context, scene_name: str, item_name: str):
    """Check if an item in a scene is visible."""
    if not validate.scene_in_scenes(ctx, scene_name):
        typer.echo(f"Scene '{scene_name}' not found.")
        raise typer.Exit(code=1)

    if not validate.item_in_scene_item_list(ctx, scene_name, item_name):
        typer.echo(f"Item '{item_name}' not found in scene '{scene_name}'.")
        raise typer.Exit(code=1)

    resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)
    enabled = ctx.obj['obsws'].get_scene_item_enabled(
        scene_name=scene_name,
        item_id=int(resp.scene_item_id),
    )
    typer.echo(
        f"Item '{item_name}' in scene '{scene_name}' is currently {'visible' if enabled.scene_item_enabled else 'hidden'}."
    )
