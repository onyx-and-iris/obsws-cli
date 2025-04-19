"""module containing commands for manipulating inputs."""

import obsws_python as obsws
import typer

from .alias import AliasGroup
from .errors import ObswsCliBadParameter
from .protocols import DataclassProtocol

app = typer.Typer(cls=AliasGroup)


@app.callback()
def main():
    """Control inputs in OBS."""


@app.command('ls')
def list(ctx: typer.Context):
    """List all inputs."""
    resp = ctx.obj['obsws'].get_input_list()
    inputs = (input.get('inputName') for input in resp.inputs)
    typer.echo('\n'.join(inputs))


def _get_input(input_name: str, resp: DataclassProtocol) -> dict | None:
    """Get an input from the input list response."""
    input_ = next(
        (input_ for input_ in resp.inputs if input_.get('inputName') == input_name),
        None,
    )

    return input_


@app.command()
def mute(ctx: typer.Context, input_name: str):
    """Mute an input."""
    try:
        resp = ctx.obj['obsws'].get_input_list()
        if (input_ := _get_input(input_name, resp)) is None:
            raise ObswsCliBadParameter(f"Input '{input_name}' not found.")

        ctx.obj['obsws'].set_input_mute(
            name=input_.get('inputName'),
            muted=True,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


@app.command()
def unmute(ctx: typer.Context, input_name: str):
    """Unmute an input."""
    try:
        resp = ctx.obj['obsws'].get_input_list()
        if (input_ := _get_input(input_name, resp)) is None:
            raise ObswsCliBadParameter(f"Input '{input_name}' not found.")

        ctx.obj['obsws'].set_input_mute(
            name=input_.get('inputName'),
            muted=False,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise


@app.command()
def toggle(ctx: typer.Context, input_name: str):
    """Toggle an input."""
    try:
        resp = ctx.obj['obsws'].get_input_list()
        if (input_ := _get_input(input_name, resp)) is None:
            raise ObswsCliBadParameter(f"Input '{input_name}' not found.")

        resp = ctx.obj['obsws'].get_input_mute(name=input_.get('inputName'))

        ctx.obj['obsws'].set_input_mute(
            name=input_.get('inputName'),
            muted=not resp.input_muted,
        )
    except obsws.error.OBSSDKRequestError as e:
        if e.code == 600:
            raise ObswsCliBadParameter(str(e)) from e
        raise
