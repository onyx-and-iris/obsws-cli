"""module containing commands for manipulating scene collections."""

import obsws_python as obsws
import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control scene collections in OBS."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List all scene collections."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    typer.echo('\n'.join(resp.scene_collections))


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current scene collection."""
    resp = ctx.obj['obsws'].get_scene_collection_list()
    typer.echo(resp.current_scene_collection_name)


@app.command('switch | set')
def switch(ctx: typer.Context, scene_collection_name: str):
    """Switch to a scene collection."""
    current_scene_collection = (
        ctx.obj['obsws'].get_scene_collection_list().current_scene_collection_name
    )
    if scene_collection_name == current_scene_collection:
        typer.echo(
            f'Scene collection "{scene_collection_name}" is already active.', err=True
        )
        raise typer.Exit(code=1)

    try:
        ctx.obj['obsws'].set_current_scene_collection(scene_collection_name)
        typer.echo(f'Switched to scene collection {scene_collection_name}')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            typer.echo(
                f'Scene collection "{scene_collection_name}" does not exist.',
                err=True,
            )
        raise typer.Exit(code=e.code)


@app.command('create | new')
def create(ctx: typer.Context, scene_collection_name: str):
    """Create a new scene collection."""
    try:
        ctx.obj['obsws'].create_scene_collection(scene_collection_name)
        typer.echo(f'Created scene collection {scene_collection_name}')
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 601:
            typer.echo(
                f'Scene collection "{scene_collection_name}" already exists.',
                err=True,
            )
        raise typer.Exit(code=e.code)
