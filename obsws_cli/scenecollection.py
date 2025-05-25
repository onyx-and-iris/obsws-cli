"""module containing commands for manipulating scene collections."""

import typer
from rich.console import Console
from rich.table import Table

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control scene collections in OBS."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scene collections."""
    resp = ctx.obj.get_scene_collection_list()

    table = Table(title='Scene Collections', padding=(0, 2))
    table.add_column('Scene Collection Name', justify='left', style='cyan')

    for scene_collection_name in resp.scene_collections:
        table.add_row(scene_collection_name)

    out_console.print(table)


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current scene collection."""
    resp = ctx.obj.get_scene_collection_list()
    out_console.print(resp.current_scene_collection_name)


@app.command('switch | set')
def switch(ctx: typer.Context, scene_collection_name: str):
    """Switch to a scene collection."""
    if not validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        err_console.print(f"Scene collection '{scene_collection_name}' not found.")
        raise typer.Exit(1)

    current_scene_collection = (
        ctx.obj.get_scene_collection_list().current_scene_collection_name
    )
    if scene_collection_name == current_scene_collection:
        err_console.print(
            f'Scene collection "{scene_collection_name}" is already active.'
        )
        raise typer.Exit(1)

    ctx.obj.set_current_scene_collection(scene_collection_name)
    out_console.print(f"Switched to scene collection '{scene_collection_name}'")


@app.command('create | new')
def create(ctx: typer.Context, scene_collection_name: str):
    """Create a new scene collection."""
    if validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        err_console.print(f"Scene collection '{scene_collection_name}' already exists.")
        raise typer.Exit(1)

    ctx.obj.create_scene_collection(scene_collection_name)
    out_console.print(f'Created scene collection {scene_collection_name}')
