"""module containing commands for manipulating scene collections."""

from typing import Annotated

import typer
from rich.table import Table

from obsws_cli import console, validate

app = typer.Typer()


@app.callback()
def main():
    """Control scene collections in OBS."""


@app.command('list')
@app.command('ls', hidden=True)
def list_(ctx: typer.Context):
    """List all scene collections."""
    resp = ctx.obj['obsws'].get_scene_collection_list()

    if not resp.scene_collections:
        console.out.print('No scene collections found.')
        raise typer.Exit()

    table = Table(
        title='Scene Collections',
        padding=(0, 2),
        border_style=ctx.obj['style'].border,
    )
    table.add_column(
        'Scene Collection Name', justify='left', style=ctx.obj['style'].column
    )

    for scene_collection_name in resp.scene_collections:
        table.add_row(scene_collection_name)

    console.out.print(table)


@app.command('current')
@app.command('get', hidden=True)
def current(ctx: typer.Context):
    """Get the current scene collection."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    console.out.print(
        f'Current scene collection: {console.highlight(ctx, resp.current_scene_collection_name)}'
    )


@app.command('switch')
@app.command('set', hidden=True)
def switch(
    ctx: typer.Context,
    scene_collection_name: Annotated[
        str,
        typer.Argument(
            ...,
            help='Name of the scene collection to switch to',
            callback=validate.scene_collection_in_scene_collections,
        ),
    ],
):
    """Switch to a scene collection."""
    current_scene_collection = (
        ctx.obj['obsws'].get_scene_collection_list().current_scene_collection_name
    )
    if scene_collection_name == current_scene_collection:
        console.err.print(
            f'Scene collection [yellow]{scene_collection_name}[/yellow] is already active.'
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_current_scene_collection(scene_collection_name)
    console.out.print(
        f'Switched to scene collection {console.highlight(ctx, scene_collection_name)}.'
    )


@app.command('create')
@app.command('new', hidden=True)
def create(
    ctx: typer.Context,
    scene_collection_name: Annotated[
        str,
        typer.Argument(
            ...,
            help='Name of the scene collection to create',
            callback=validate.scene_collection_not_in_scene_collections,
        ),
    ],
):
    """Create a new scene collection."""
    ctx.obj['obsws'].create_scene_collection(scene_collection_name)
    console.out.print(
        f'Created scene collection {console.highlight(ctx, scene_collection_name)}.'
    )
