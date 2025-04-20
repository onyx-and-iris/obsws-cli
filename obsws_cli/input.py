"""module containing commands for manipulating inputs."""

from typing import Annotated

import typer

from . import validate
from .alias import AliasGroup

app = typer.Typer(cls=AliasGroup)


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
    resp = ctx.obj['obsws'].get_input_list()

    filters = []
    if input:
        filters.append('input')
    if output:
        filters.append('output')
    if colour:
        filters.append('color')

    inputs = filter(
        lambda input_: any(kind in input_.get('inputKind') for kind in filters),
        resp.inputs,
    )
    typer.echo('\n'.join(input_.get('inputName') for input_ in inputs))


@app.command()
def mute(ctx: typer.Context, input_name: str):
    """Mute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        typer.echo(
            f"Input '{input_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=True,
    )


@app.command()
def unmute(ctx: typer.Context, input_name: str):
    """Unmute an input."""
    if not validate.input_in_inputs(ctx, input_name):
        typer.echo(
            f"Input '{input_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=False,
    )


@app.command('toggle | tg')
def toggle(ctx: typer.Context, input_name: str):
    """Toggle an input."""
    if not validate.input_in_inputs(ctx, input_name):
        typer.echo(
            f"Input '{input_name}' not found.",
            err=True,
        )
        raise typer.Exit(code=1)

    # Get the current mute state
    resp = ctx.obj['obsws'].get_input_mute(name=input_name)
    new_state = not resp.input_muted

    ctx.obj['obsws'].set_input_mute(
        name=input_name,
        muted=new_state,
    )
