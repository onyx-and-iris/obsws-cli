"""module containing commands for manipulating projectors in OBS."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control projectors in OBS."""


@app.command('list-monitors | ls-m')
def list_monitors(ctx: typer.Context):
    """List available monitors."""
    resp = ctx.obj.get_monitor_list()

    if not resp.monitors:
        out_console.print('No monitors found.')
        return

    monitors = sorted(
        ((m['monitorIndex'], m['monitorName']) for m in resp.monitors),
        key=lambda m: m[0],
    )

    table = Table(title='Available Monitors', padding=(0, 2))
    table.add_column('Index', justify='center', style='cyan')
    table.add_column('Name', style='cyan')

    for index, monitor in monitors:
        table.add_row(str(index), monitor)

    out_console.print(table)


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
            help='Name of the source to project. (optional, defaults to current scene)'
        ),
    ] = '',
):
    """Open a fullscreen projector for a source on a specific monitor."""
    if not source_name:
        source_name = ctx.obj.get_current_program_scene().scene_name

    ctx.obj.open_source_projector(
        source_name=source_name,
        monitor_index=monitor_index,
    )

    out_console.print(
        f'Opened projector for source [bold]{source_name}[/] on monitor [bold]{monitor_index}[/].'
    )
