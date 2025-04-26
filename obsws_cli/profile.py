"""module containing commands for manipulating profiles in OBS."""

import typer

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List profiles."""
    resp = ctx.obj.get_profile_list()
    for profile in resp.profiles:
        typer.echo(profile)


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current profile."""
    resp = ctx.obj.get_profile_list()
    typer.echo(resp.current_profile_name)


@app.command('switch | set')
def switch(ctx: typer.Context, profile_name: str):
    """Switch to a profile."""
    if not validate.profile_exists(ctx, profile_name):
        typer.echo(
            f"Profile '{profile_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    resp = ctx.obj.get_profile_list()
    if resp.current_profile_name == profile_name:
        typer.echo(
            f"Profile '{profile_name}' is already the current profile.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj.set_current_profile(profile_name)
    typer.echo(f"Switched to profile '{profile_name}'.")


@app.command('create | new')
def create(ctx: typer.Context, profile_name: str):
    """Create a new profile."""
    if validate.profile_exists(ctx, profile_name):
        typer.echo(
            f"Profile '{profile_name}' already exists.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj.create_profile(profile_name)
    typer.echo(f"Created profile '{profile_name}'.")


@app.command('remove | rm')
def remove(ctx: typer.Context, profile_name: str):
    """Remove a profile."""
    if not validate.profile_exists(ctx, profile_name):
        typer.echo(
            f"Profile '{profile_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj.remove_profile(profile_name)
    typer.echo(f"Removed profile '{profile_name}'.")
