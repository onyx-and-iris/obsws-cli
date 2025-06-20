"""module containing commands for manipulating profiles in OBS."""

from typing import Annotated

import typer
from rich.table import Table

from . import console, util, validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('list | ls')
def list_(ctx: typer.Context):
    """List profiles."""
    resp = ctx.obj.get_profile_list()

    table = Table(title='Profiles', padding=(0, 2))
    columns = [
        ('Profile Name', 'left', 'cyan'),
        ('Current', 'center', None),
    ]
    for column, justify, style in columns:
        table.add_column(column, justify=justify, style=style)

    for profile in resp.profiles:
        table.add_row(
            profile,
            util.check_mark(profile == resp.current_profile_name),
        )

    console.out.print(table)


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current profile."""
    resp = ctx.obj.get_profile_list()
    console.out.print(resp.current_profile_name)


@app.command('switch | set')
def switch(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(
            ..., show_default=False, help='Name of the profile to switch to'
        ),
    ],
):
    """Switch to a profile."""
    if not validate.profile_exists(ctx, profile_name):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] not found.')
        raise typer.Exit(1)

    resp = ctx.obj.get_profile_list()
    if resp.current_profile_name == profile_name:
        console.err.print(
            f'Profile [yellow]{profile_name}[/yellow] is already the current profile.'
        )
        raise typer.Exit(1)

    ctx.obj.set_current_profile(profile_name)
    console.out.print(f'Switched to profile [green]{profile_name}[/green].')


@app.command('create | new')
def create(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Name of the profile to create.'),
    ],
):
    """Create a new profile."""
    if validate.profile_exists(ctx, profile_name):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] already exists.')
        raise typer.Exit(1)

    ctx.obj.create_profile(profile_name)
    console.out.print(f'Created profile [green]{profile_name}[/green].')


@app.command('remove | rm')
def remove(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(..., show_default=False, help='Name of the profile to remove.'),
    ],
):
    """Remove a profile."""
    if not validate.profile_exists(ctx, profile_name):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] not found.')
        raise typer.Exit(1)

    ctx.obj.remove_profile(profile_name)
    console.out.print(f'Removed profile [green]{profile_name}[/green].')
