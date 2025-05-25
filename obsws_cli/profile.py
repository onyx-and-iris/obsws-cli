"""module containing commands for manipulating profiles in OBS."""

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
    """Control profiles in OBS."""


@app.command('list | ls')
def list(ctx: typer.Context):
    """List profiles."""
    resp = ctx.obj.get_profile_list()

    table = Table(title='Profiles', padding=(0, 2))
    for column in ('Profile Name', 'Current'):
        table.add_column(
            column,
            justify='left' if column == 'Profile Name' else 'center',
            style='cyan',
        )

    for profile in resp.profiles:
        table.add_row(
            profile,
            ':white_heavy_check_mark:' if profile == resp.current_profile_name else '',
        )

    out_console.print(table)


@app.command('current | get')
def current(ctx: typer.Context):
    """Get the current profile."""
    resp = ctx.obj.get_profile_list()
    out_console.print(resp.current_profile_name)


@app.command('switch | set')
def switch(ctx: typer.Context, profile_name: str):
    """Switch to a profile."""
    if not validate.profile_exists(ctx, profile_name):
        err_console.print(f"Profile '{profile_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_profile_list()
    if resp.current_profile_name == profile_name:
        err_console.print(f"Profile '{profile_name}' is already the current profile.")
        raise typer.Exit(1)

    ctx.obj.set_current_profile(profile_name)
    out_console.print(f"Switched to profile '{profile_name}'.")


@app.command('create | new')
def create(ctx: typer.Context, profile_name: str):
    """Create a new profile."""
    if validate.profile_exists(ctx, profile_name):
        err_console.print(f"Profile '{profile_name}' already exists.")
        raise typer.Exit(1)

    ctx.obj.create_profile(profile_name)
    out_console.print(f"Created profile '{profile_name}'.")


@app.command('remove | rm')
def remove(ctx: typer.Context, profile_name: str):
    """Remove a profile."""
    if not validate.profile_exists(ctx, profile_name):
        err_console.print(f"Profile '{profile_name}' not found.")
        raise typer.Exit(1)

    ctx.obj.remove_profile(profile_name)
    out_console.print(f"Removed profile '{profile_name}'.")
