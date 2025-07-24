"""module containing commands for manipulating projectors in OBS."""

from typing import Annotated

from cyclopts import App, Argument, Parameter
from rich.table import Table
from rich.text import Text

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='projector', help='Commands for managing projectors in OBS')


@app.command(name=['list-monitors', 'ls-m'])
def list_monitors(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """List available monitors."""
    resp = ctx.client.get_monitor_list()

    if not resp.monitors:
        console.out.print('No monitors found.')
        return

    monitors = sorted(
        ((m['monitorIndex'], m['monitorName']) for m in resp.monitors),
        key=lambda m: m[0],
    )

    table = Table(
        title='Available Monitors',
        padding=(0, 2),
        border_style=ctx.style.border,
    )
    table.add_column(
        Text('Index', justify='center'), justify='center', style=ctx.style.column
    )
    table.add_column(
        Text('Name', justify='center'), justify='left', style=ctx.style.column
    )

    for index, monitor in monitors:
        table.add_row(str(index), monitor)

    console.out.print(table)


@app.command(name=['open', 'o'])
def open(
    source_name: Annotated[
        str,
        Argument(
            hint='Name of the source to project.',
        ),
    ] = '',
    /,
    monitor_index: Annotated[
        int,
        Parameter(help='Index of the monitor to open the projector on.'),
    ] = 0,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Open a fullscreen projector for a source on a specific monitor."""
    if not source_name:
        source_name = ctx.client.get_current_program_scene().scene_name

    monitors = ctx.client.get_monitor_list().monitors
    for monitor in monitors:
        if monitor['monitorIndex'] == monitor_index:
            ctx.client.open_source_projector(
                source_name=source_name,
                monitor_index=monitor_index,
            )

            console.out.print(
                f'Opened projector for source {console.highlight(ctx, source_name)} on monitor {console.highlight(ctx, monitor["monitorName"])}.'
            )

            break
    else:
        raise OBSWSCLIError(
            f'Monitor with index [yellow]{monitor_index}[/yellow] not found. '
            f'Use [yellow]obsws-cli projector ls-m[/yellow] to see available monitors.',
            ExitCode.ERROR,
        )
