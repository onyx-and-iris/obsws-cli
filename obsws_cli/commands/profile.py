"""module containing commands for manipulating profiles in OBS."""

from typing import Annotated

import typer
from rich.table import Table
from rich.text import Text

from obsws_cli import console, util, validate

app = typer.Typer()


@app.callback()
def main():
    """Control profiles in OBS."""


@app.command('list')
@app.command('ls', hidden=True)
def list_(ctx: typer.Context):
    """List profiles."""
    resp = ctx.obj['obsws'].get_profile_list()

    if not resp.profiles:
        console.out.print('No profiles found.')
        raise typer.Exit()

    table = Table(
        title='Profiles', padding=(0, 2), border_style=ctx.obj['style'].border
    )
    columns = [
        (Text('Profile Name', justify='center'), 'left', ctx.obj['style'].column),
        (Text('Current', justify='center'), 'center', None),
    ]
    for heading, justify, style in columns:
        table.add_column(heading, justify=justify, style=style)

    for profile in resp.profiles:
        table.add_row(
            profile,
            util.check_mark(
                ctx, profile == resp.current_profile_name, empty_if_false=True
            ),
        )

    console.out.print(table)


@app.command('current')
@app.command('get', hidden=True)
def current(ctx: typer.Context):
    """Get the current profile."""
    resp = ctx.obj['obsws'].get_profile_list()
    console.out.print(
        f'Current profile: {console.highlight(ctx, resp.current_profile_name)}'
    )


@app.command('switch')
@app.command('set', hidden=True)
def switch(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the profile to switch to',
            callback=validate.profile_exists,
        ),
    ],
):
    """Switch to a profile."""
    resp = ctx.obj['obsws'].get_profile_list()
    if resp.current_profile_name == profile_name:
        console.err.print(
            f'Profile [yellow]{profile_name}[/yellow] is already the current profile.'
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_current_profile(profile_name)
    console.out.print(f'Switched to profile {console.highlight(ctx, profile_name)}.')


@app.command('create')
@app.command('new', hidden=True)
def create(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the profile to create.',
            callback=validate.profile_not_exists,
        ),
    ],
):
    """Create a new profile."""
    ctx.obj['obsws'].create_profile(profile_name)
    console.out.print(f'Created profile {console.highlight(ctx, profile_name)}.')


@app.command('remove')
@app.command('rm', hidden=True)
def remove(
    ctx: typer.Context,
    profile_name: Annotated[
        str,
        typer.Argument(
            ...,
            show_default=False,
            help='Name of the profile to remove.',
            callback=validate.profile_exists,
        ),
    ],
):
    """Remove a profile."""
    ctx.obj['obsws'].remove_profile(profile_name)
    console.out.print(f'Removed profile {console.highlight(ctx, profile_name)}.')
