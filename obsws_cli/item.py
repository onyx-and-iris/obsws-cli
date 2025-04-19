"""module containing commands for manipulating items in scenes."""

import obsws_python as obsws
import typer

from .alias import AliasGroup
from .errors import ObswsCliBadParameter

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control items in OBS scenes."""


@app.command()
def show(ctx: typer.Context, scene_name: str, item_name: str):
    """Show an item in a scene."""
    try:
        resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)

        ctx.obj['obsws'].set_scene_item_enabled(
            scene_name=scene_name,
            item_id=int(resp.scene_item_id),
            enabled=True,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


@app.command()
def hide(ctx: typer.Context, scene_name: str, item_name: str):
    """Hide an item in a scene."""
    try:
        resp = ctx.obj['obsws'].get_scene_item_id(scene_name, item_name)

        ctx.obj['obsws'].set_scene_item_enabled(
            scene_name=scene_name,
            item_id=int(resp.scene_item_id),
            enabled=False,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


@app.command('list | ls')
def list(ctx: typer.Context, scene_name: str):
    """List all items in a scene."""
    try:
        resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
        items = (item.get('sourceName') for item in resp.scene_items)
        typer.echo('\n'.join(items))
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise
