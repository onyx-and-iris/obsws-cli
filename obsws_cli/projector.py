"""module containing commands for manipulating projectors in OBS."""

from typing import Annotated

import typer
from rich.table import Table
from rich.text import Text

from . import console
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control projectors in OBS."""


@app.command('list-monitors | ls-m')
def list_monitors(ctx: typer.Context):
    """List available monitors."""
    resp = ctx.obj['obsws'].get_monitor_list()

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
        border_style=ctx.obj['style'].border,
    )
    table.add_column(
        Text('Index', justify='center'), justify='center', style=ctx.obj['style'].column
    )
    table.add_column(
        Text('Name', justify='center'), justify='left', style=ctx.obj['style'].column
    )

    for index, monitor in monitors:
        table.add_row(str(index), monitor)

    console.out.print(table)


@app.command('open | o')
def open(
    ctx: typer.Context,
    monitor_index: Annotated[
        int,
        typer.Option(help='Index of the monitor to open the projector on.'),
    ] = 0,
    source_name: Annotated[
        str,
        typer.Argument(
            show_default='The current scene',
            help='Name of the source to project.',
        ),
    ] = '',
):
    """Open a fullscreen projector for a source on a specific monitor."""
    if not source_name:
        source_name = ctx.obj['obsws'].get_current_program_scene().scene_name

    monitors = ctx.obj['obsws'].get_monitor_list().monitors
    for monitor in monitors:
        if monitor['monitorIndex'] == monitor_index:
            ctx.obj['obsws'].open_source_projector(
                source_name=source_name,
                monitor_index=monitor_index,
            )

            console.out.print(
                f'Opened projector for source {console.highlight(ctx, source_name)} on monitor {console.highlight(ctx, monitor["monitorName"])}.'
            )

            break
    else:
        console.err.print(
            f'Monitor with index [yellow]{monitor_index}[/yellow] not found. '
            f'Use [yellow]obsws-cli projector ls-m[/yellow] to see available monitors.'
        )
        raise typer.Exit(code=1)
