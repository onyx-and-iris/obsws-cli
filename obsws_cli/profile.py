"""module containing commands for manipulating profiles in OBS."""

from typing import Annotated

from cyclopts import App, Argument, Parameter
from rich.table import Table
from rich.text import Text

from . import console, util, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='profile', help='Commands for managing profiles in OBS')


@app.command(name=['list', 'ls'])
def list_(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List profiles."""
    resp = ctx.client.get_profile_list()

    table = Table(title='Profiles', padding=(0, 2), border_style=ctx.style.border)
    columns = [
        (Text('Profile Name', justify='center'), 'left', ctx.style.column),
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


@app.command(name=['current', 'get'])
def current(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the current profile."""
    resp = ctx.client.get_profile_list()
    console.out.print(
        f'Current profile: {console.highlight(ctx, resp.current_profile_name)}'
    )


@app.command(name=['switch', 'set'])
def switch(
    profile_name: Annotated[
        str,
        Argument(hint='Name of the profile to switch to'),
    ],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Switch to a profile."""
    if not validate.profile_exists(ctx, profile_name):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] not found.')
        raise OBSWSCLIError(
            f'Profile [yellow]{profile_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    resp = ctx.client.get_profile_list()
    if resp.current_profile_name == profile_name:
        raise OBSWSCLIError(
            f'Profile [yellow]{profile_name}[/yellow] is already the current profile.',
            code=ExitCode.ERROR,
        )

    ctx.client.set_current_profile(profile_name)
    console.out.print(f'Switched to profile {console.highlight(ctx, profile_name)}.')


@app.command(name=['create', 'new'])
def create(
    profile_name: Annotated[
        str,
        Argument(hint='Name of the profile to create.'),
    ],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Create a new profile."""
    if validate.profile_exists(ctx, profile_name):
        raise OBSWSCLIError(
            f'Profile [yellow]{profile_name}[/yellow] already exists.',
            code=ExitCode.ERROR,
        )

    ctx.client.create_profile(profile_name)
    console.out.print(f'Created profile {console.highlight(ctx, profile_name)}.')


@app.command(name=['remove', 'rm'])
def remove(
    profile_name: Annotated[
        str,
        Argument(hint='Name of the profile to remove.'),
    ],
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Remove a profile."""
    if not validate.profile_exists(ctx, profile_name):
        console.err.print(f'Profile [yellow]{profile_name}[/yellow] not found.')
        raise OBSWSCLIError(
            f'Profile [yellow]{profile_name}[/yellow] not found.',
            code=ExitCode.ERROR,
        )

    ctx.client.remove_profile(profile_name)
    console.out.print(f'Removed profile {console.highlight(ctx, profile_name)}.')
