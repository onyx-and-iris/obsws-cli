"""module containing commands for manipulating scene collections."""

from typing import Annotated

from cyclopts import App, Parameter
from rich.table import Table

from . import console, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(
    name='scenecollection', help='Commands for controlling scene collections in OBS.'
)


@app.command(name=['list', 'ls'])
def list_(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List all scene collections.

    Parameters
    ----------
    ctx : Context
        The context containing the OBS client and configuration.

    """
    resp = ctx.client.get_scene_collection_list()

    table = Table(
        title='Scene Collections',
        padding=(0, 2),
        border_style=ctx.style.border,
    )
    table.add_column('Scene Collection Name', justify='left', style=ctx.style.column)

    for scene_collection_name in resp.scene_collections:
        table.add_row(scene_collection_name)

    console.out.print(table)


@app.command(name=['current', 'get'])
def current(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the current scene collection.

    Parameters
    ----------
    ctx : Context
        The context containing the OBS client and configuration.

    """
    resp = ctx.client.get_scene_collection_list()
    console.out.print(
        f'Current scene collection: {console.highlight(ctx, resp.current_scene_collection_name)}'
    )


@app.command(name=['switch', 'set'])
def switch(
    scene_collection_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Switch to a scene collection.

    Parameters
    ----------
    scene_collection_name : str
        The name of the scene collection to switch to.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    if not validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        raise OBSWSCLIError(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] not found.',
            exit_code=ExitCode.ERROR,
        )

    current_scene_collection = (
        ctx.client.get_scene_collection_list().current_scene_collection_name
    )
    if scene_collection_name == current_scene_collection:
        raise OBSWSCLIError(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] is already active.',
            exit_code=ExitCode.ERROR,
        )

    ctx.client.set_current_scene_collection(scene_collection_name)
    console.out.print(
        f'Switched to scene collection {console.highlight(ctx, scene_collection_name)}.'
    )


@app.command(name=['create', 'new'])
def create(
    scene_collection_name: str,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Create a new scene collection.

    Parameters
    ----------
    scene_collection_name : str
        The name of the scene collection to create.
    ctx : Context
        The context containing the OBS client and configuration.

    """
    if validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        raise OBSWSCLIError(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] already exists.',
            exit_code=ExitCode.ERROR,
        )

    ctx.client.create_scene_collection(scene_collection_name)
    console.out.print(
        f'Created scene collection {console.highlight(ctx, scene_collection_name)}.'
    )
