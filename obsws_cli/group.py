"""module containing commands for manipulating groups in scenes."""

import obsws_python as obsws
import typer

from .alias import AliasGroup
from .errors import ObswsCliBadParameter
from .protocols import DataclassProtocol

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control groups in OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context, scene_name: str):
    """List groups in a scene."""
    try:
        resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
        groups = (
            item.get('sourceName') for item in resp.scene_items if item.get('isGroup')
        )
        typer.echo('\n'.join(groups))
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


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
    try:
        resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
        if (group := _get_group(group_name, resp)) is None:
            raise ObswsCliBadParameter(f"Group '{group_name}' not found in scene.")

        ctx.obj['obsws'].set_scene_item_enabled(
            scene_name=scene_name,
            item_id=int(group.get('sceneItemId')),
            enabled=True,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


@app.command()
def hide(ctx: typer.Context, scene_name: str, group_name: str):
    """Hide a group in a scene."""
    try:
        resp = ctx.obj['obsws'].get_scene_item_list(scene_name)
        if (group := _get_group(group_name, resp)) is None:
            raise ObswsCliBadParameter(f"Group '{group_name}' not found in scene.")

        ctx.obj['obsws'].set_scene_item_enabled(
            scene_name=scene_name,
            item_id=int(group.get('sceneItemId')),
            enabled=False,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise
