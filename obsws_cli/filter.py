"""module containing commands for manipulating filters in scenes."""

import obsws_python as obsws
import typer
from rich.console import Console
from rich.table import Table

from . import util
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control filters in OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context, source_name: str):
    """List filters for a source."""
    try:
        resp = ctx.obj.get_source_filter_list(source_name)
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            err_console.print(f"No source was found by the name of '{source_name}'.")
            raise typer.Exit(1)
        else:
            raise

    if not resp.filters:
        out_console.print(f'No filters found for source {source_name}')
        raise typer.Exit()

    table = Table(title=f'Filters for Source: {source_name}', padding=(0, 2))

    for column in ('Filter Name', 'Kind', 'Enabled', 'Settings'):
        table.add_column(
            column,
            justify='left' if column in ('Filter Name', 'Kind') else 'center',
            style='cyan',
        )

    for filter in resp.filters:
        table.add_row(
            filter['filterName'],
            util.snakecase_to_titlecase(filter['filterKind']),
            ':white_heavy_check_mark:' if filter['filterEnabled'] else ':x:',
            '\n'.join(
                [
                    f'{util.snakecase_to_titlecase(k):<20} {v:>10}'
                    for k, v in filter['filterSettings'].items()
                ]
            ),
        )

    out_console.print(table)


def _get_filter_enabled(ctx: typer.Context, source_name: str, filter_name: str):
    """Get the status of a filter for a source."""
    resp = ctx.obj.get_source_filter(source_name, filter_name)
    return resp.filter_enabled


@app.command('enable | on')
def enable(
    ctx: typer.Context,
    source_name: str = typer.Argument(..., help='The source to enable the filter for'),
    filter_name: str = typer.Argument(..., help='The name of the filter to enable'),
):
    """Enable a filter for a source."""
    if _get_filter_enabled(ctx, source_name, filter_name):
        err_console.print(
            f'Filter {filter_name} is already enabled for source {source_name}'
        )
        raise typer.Exit(1)

    ctx.obj.set_source_filter_enabled(source_name, filter_name, enabled=True)
    out_console.print(f'Enabled filter {filter_name} for source {source_name}')


@app.command('disable | off')
def disable(
    ctx: typer.Context,
    source_name: str = typer.Argument(..., help='The source to disable the filter for'),
    filter_name: str = typer.Argument(..., help='The name of the filter to disable'),
):
    """Disable a filter for a source."""
    if not _get_filter_enabled(ctx, source_name, filter_name):
        err_console.print(
            f'Filter {filter_name} is already disabled for source {source_name}'
        )
        raise typer.Exit(1)

    ctx.obj.set_source_filter_enabled(source_name, filter_name, enabled=False)
    out_console.print(f'Disabled filter {filter_name} for source {source_name}')


@app.command('toggle | tg')
def toggle(
    ctx: typer.Context,
    source_name: str = typer.Argument(..., help='The source to toggle the filter for'),
    filter_name: str = typer.Argument(..., help='The name of the filter to toggle'),
):
    """Toggle a filter for a source."""
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    new_state = not is_enabled

    ctx.obj.set_source_filter_enabled(source_name, filter_name, enabled=new_state)
    if new_state:
        out_console.print(f'Enabled filter {filter_name} for source {source_name}')
    else:
        out_console.print(f'Disabled filter {filter_name} for source {source_name}')


@app.command('status | ss')
def status(
    ctx: typer.Context,
    source_name: str = typer.Argument(
        ..., help='The source to get the filter status for'
    ),
    filter_name: str = typer.Argument(
        ..., help='The name of the filter to get the status for'
    ),
):
    """Get the status of a filter for a source."""
    is_enabled = _get_filter_enabled(ctx, source_name, filter_name)
    if is_enabled:
        out_console.print(f'Filter {filter_name} is enabled for source {source_name}')
    else:
        out_console.print(f'Filter {filter_name} is disabled for source {source_name}')
