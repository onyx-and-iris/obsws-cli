"""module containing commands for manipulating inputs."""

from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table

from . import util, validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)
out_console = Console()
err_console = Console(stderr=True)


@app.callback()
def main():
    """Control inputs in OBS."""


@app.command('list | ls')
def list(
    ctx: typer.Context,
    input: Annotated[bool, typer.Option(help='Filter by input type.')] = False,
    output: Annotated[bool, typer.Option(help='Filter by output type.')] = False,
    colour: Annotated[bool, typer.Option(help='Filter by colour source type.')] = False,
):
    """List all inputs."""
    resp = ctx.obj.get_input_list()

    kinds = []
    if input:
        kinds.append('input')
    if output:
        kinds.append('output')
    if colour:
        kinds.append('color')
    if not any([input, output, colour]):
        kinds = ['input', 'output', 'color']

    inputs = [
        (input_.get('inputName'), input_.get('inputKind'))
        for input_ in filter(
            lambda input_: any(kind in input_.get('inputKind') for kind in kinds),
            resp.inputs,
        )
    ]

    if not inputs:
        out_console.print('No inputs found.')
        raise typer.Exit()

    table = Table(title='Inputs', padding=(0, 2))
    for column in ('Input Name', 'Kind'):
        table.add_column(
            column, justify='left' if column == 'Input Name' else 'center', style='cyan'
        )

    for input_name, input_kind in inputs:
        table.add_row(
            input_name,
            util.snakecase_to_titlecase(input_kind),
        )

    out_console.print(table)


@app.command('mute | m')
def mute(ctx: typer.Context, input_name: str):
    """Mute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f"Input '{input_name}' not found.")
        raise typer.Exit(1)

    ctx.obj.set_input_mute(
        name=input_name,
        muted=True,
    )

    out_console.print(f"Input '{input_name}' muted.")


@app.command('unmute | um')
def unmute(ctx: typer.Context, input_name: str):
    """Unmute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f"Input '{input_name}' not found.")
        raise typer.Exit(1)

    ctx.obj.set_input_mute(
        name=input_name,
        muted=False,
    )

    out_console.print(f"Input '{input_name}' unmuted.")


@app.command('toggle | tg')
def toggle(ctx: typer.Context, input_name: str):
    """Toggle an input."""
    if not validate.input_in_inputs(ctx, input_name):
        err_console.print(f"Input '{input_name}' not found.")
        raise typer.Exit(1)

    resp = ctx.obj.get_input_mute(name=input_name)
    new_state = not resp.input_muted

    ctx.obj.set_input_mute(
        name=input_name,
        muted=new_state,
    )

    out_console.print(
        f"Input '{input_name}' {'muted' if new_state else 'unmuted'}.",
    )
