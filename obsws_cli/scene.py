"""module containing commands for controlling OBS scenes."""

from typing import Annotated

from cyclopts import App, Parameter
from rich.table import Table
from rich.text import Text

from . import console, util, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='scene', help='Commands for managing OBS scenes')


@app.command(name=['list', 'ls'])
def list_(
    uuid: bool = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List all scenes.

    Parameters
    ----------
    uuid : bool
        Show UUIDs of scenes.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    resp = ctx.client.get_scene_list()
    scenes = (
        (scene.get('sceneName'), scene.get('sceneUuid'))
        for scene in reversed(resp.scenes)
    )

    active_scene = ctx.client.get_current_program_scene().scene_name

    table = Table(title='Scenes', padding=(0, 2), border_style=ctx.style.border)
    if uuid:
        columns = [
            (Text('Scene Name', justify='center'), 'left', ctx.style.column),
            (Text('Active', justify='center'), 'center', None),
            (Text('UUID', justify='center'), 'left', ctx.style.column),
        ]
    else:
        columns = [
            (Text('Scene Name', justify='center'), 'left', ctx.style.column),
            (Text('Active', justify='center'), 'center', None),
        ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

    for scene_name, scene_uuid in scenes:
        if uuid:
            table.add_row(
                scene_name,
                util.check_mark(scene_name == active_scene, empty_if_false=True),
                scene_uuid,
            )
        else:
            table.add_row(
                scene_name,
                util.check_mark(scene_name == active_scene, empty_if_false=True),
            )

    console.out.print(table)


@app.command(name=['current', 'get'])
def current(
    preview: bool = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the current program scene or preview scene.

    Parameters
    ----------
    preview : bool
        If True, get the preview scene instead of the program scene.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    if preview and not validate.studio_mode_enabled(ctx):
        raise OBSWSCLIError(
            'Studio mode is not enabled, cannot get preview scene.',
            code=ExitCode.ERROR,
        )

    if preview:
        resp = ctx.client.get_current_preview_scene()
        console.out.print(
            f'Current Preview Scene: {console.highlight(ctx, resp.current_preview_scene_name)}'
        )
    else:
        resp = ctx.client.get_current_program_scene()
        console.out.print(
            f'Current Program Scene: {console.highlight(ctx, resp.current_program_scene_name)}'
        )


@app.command(name=['switch', 'set'])
def switch(
    scene_name: str,
    /,
    preview: bool = False,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Switch to a scene.

    Parameters
    ----------
    scene_name : str
        The name of the scene to switch to.
    preview : bool
        If True, switch to the preview scene instead of the program scene.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    if preview and not validate.studio_mode_enabled(ctx):
        raise OBSWSCLIError(
            'Studio mode is not enabled, cannot switch to preview scene.',
            code=ExitCode.ERROR,
        )

    if not validate.scene_in_scenes(ctx, scene_name):
        raise OBSWSCLIError(
            f'Scene [yellow]{scene_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    if preview:
        ctx.client.set_current_preview_scene(scene_name)
        console.out.print(
            f'Switched to preview scene: {console.highlight(ctx, scene_name)}'
        )
    else:
        ctx.client.set_current_program_scene(scene_name)
        console.out.print(
            f'Switched to program scene: {console.highlight(ctx, scene_name)}'
        )
