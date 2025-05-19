"""module containing commands for manipulating scene collections."""

import typer

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control scene collections in OBS."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scene collections."""
    resp = ctx.obj.get_scene_collection_list()
    typer.echo('\n'.join(resp.scene_collections))


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current scene collection."""
    resp = ctx.obj.get_scene_collection_list()
    typer.echo(resp.current_scene_collection_name)


@app.command('switch | set')
def switch(ctx: typer.Context, scene_collection_name: str):
    """Switch to a scene collection."""
    if not validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        typer.echo(f"Scene collection '{scene_collection_name}' not found.", err=True)
        raise typer.Exit(1)

    current_scene_collection = (
        ctx.obj.get_scene_collection_list().current_scene_collection_name
    )
    if scene_collection_name == current_scene_collection:
        typer.echo(
            f'Scene collection "{scene_collection_name}" is already active.', err=True
        )
        raise typer.Exit(1)

    ctx.obj.set_current_scene_collection(scene_collection_name)
    typer.echo(f"Switched to scene collection '{scene_collection_name}'")


@app.command('create | new')
def create(ctx: typer.Context, scene_collection_name: str):
    """Create a new scene collection."""
    if validate.scene_collection_in_scene_collections(ctx, scene_collection_name):
        typer.echo(
            f"Scene collection '{scene_collection_name}' already exists.", err=True
        )
        raise typer.Exit(1)

    ctx.obj.create_scene_collection(scene_collection_name)
    typer.echo(f'Created scene collection {scene_collection_name}')
