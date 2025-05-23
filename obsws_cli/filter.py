"""module containing commands for manipulating filters in scenes."""

import typer

from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control filters in OBS scenes."""


@app.command('list | ls')
def list(ctx: typer.Context, source_name: str):
    """List filters for a source."""
    resp = ctx.obj.get_source_filter_list(source_name)

    if not resp.filters:
        typer.echo(f'No filters found for source {source_name}')
        return

    for filter in resp.filters:
        typer.echo(f'Filter: {filter["filterName"]}')
        for key, value in filter.items():
            if key != 'filterName':
                typer.echo(f'  {key}: {value}')


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
        typer.echo(
            f'Filter {filter_name} is already enabled for source {source_name}',
            err=True,
        )
        raise typer.Exit(1)

    ctx.obj.set_source_filter_enabled(source_name, filter_name, enabled=True)
    typer.echo(f'Enabled filter {filter_name} for source {source_name}')


@app.command('disable | off')
def disable(
    ctx: typer.Context,
    source_name: str = typer.Argument(..., help='The source to disable the filter for'),
    filter_name: str = typer.Argument(..., help='The name of the filter to disable'),
):
    """Disable a filter for a source."""
    if not _get_filter_enabled(ctx, source_name, filter_name):
        typer.echo(
            f'Filter {filter_name} is already disabled for source {source_name}',
            err=True,
        )
        raise typer.Exit(1)

    ctx.obj.set_source_filter_enabled(source_name, filter_name, enabled=False)
    typer.echo(f'Disabled filter {filter_name} for source {source_name}')


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
        typer.echo(f'Enabled filter {filter_name} for source {source_name}')
    else:
        typer.echo(f'Disabled filter {filter_name} for source {source_name}')
