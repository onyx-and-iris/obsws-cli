"""module containing commands for controlling OBS scenes."""

from typing import Annotated

import obsws_python as obsws
import typer

from .alias import AliasGroup
from .errors import ObswsCliBadParameter, ObswsCliError

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scenes."""
    resp = ctx.obj['obsws'].get_scene_list()
    scenes = (scene.get('sceneName') for scene in reversed(resp.scenes))
    typer.echo('\n'.join(scenes))


@app.command('current | get')
def current(
    ctx: typer.Context,
    preview: Annotated[
        bool, typer.Option(help='Get the preview scene instead of the program scene')
    ] = False,
):
    """Get the current program scene or preview scene."""
    try:
        if preview:
            resp = ctx.obj['obsws'].get_current_preview_scene()
            typer.echo(resp.current_preview_scene_name)
        else:
            resp = ctx.obj['obsws'].get_current_program_scene()
            typer.echo(resp.current_program_scene_name)
    except obsws.error.OBSSDKRequestError as e:
        match e.code:
            case 506:
                raise ObswsCliError(
                    'Not in studio mode, cannot get preview scene.'
                ) from e
        raise


@app.command('switch | set')
def switch(
    ctx: typer.Context,
    scene_name: str,
    preview: Annotated[
        bool,
        typer.Option(help='Switch to the preview scene instead of the program scene'),
    ] = False,
):
    """Switch to a scene."""
    try:
        if preview:
            ctx.obj['obsws'].set_current_preview_scene(scene_name)
        else:
            ctx.obj['obsws'].set_current_program_scene(scene_name)
    except obsws.error.OBSSDKRequestError as e:
        match e.code:
            case 506:
                raise ObswsCliError(
                    'Not in studio mode, cannot set preview scene.'
                ) from e
            case 600:
                raise ObswsCliBadParameter(f"Scene '{scene_name}' not found.") from e
        raise
