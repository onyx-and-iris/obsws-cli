"""module containing commands for manipulating text inputs."""

from typing import Annotated, Optional

import typer

from . import console, validate
from .alias import SubTyperAliasGroup

app = typer.Typer(cls=SubTyperAliasGroup)


@app.callback()
def main():
    """Control text inputs in OBS."""


@app.command('current | get')
def current(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            help='Name of the text input to get.', callback=validate.input_in_inputs
        ),
    ],
):
    """Get the current text for a text input."""
    resp = ctx.obj['obsws'].get_input_settings(name=input_name)
    if not resp.input_kind.startswith('text_'):
        console.err.print(
            f'Input [yellow]{input_name}[/yellow] is not a text input.',
        )
        raise typer.Exit(1)

    current_text = resp.input_settings.get('text', '')
    if not current_text:
        current_text = '(empty)'
    console.out.print(
        f'Current text for input {console.highlight(ctx, input_name)}: {current_text}',
    )


@app.command('update | set')
def update(
    ctx: typer.Context,
    input_name: Annotated[
        str,
        typer.Argument(
            help='Name of the text input to update.', callback=validate.input_in_inputs
        ),
    ],
    new_text: Annotated[
        Optional[str],
        typer.Argument(
            help='The new text to set for the input.',
        ),
    ] = None,
):
    """Update the text of a text input."""
    resp = ctx.obj['obsws'].get_input_settings(name=input_name)
    if not resp.input_kind.startswith('text_'):
        console.err.print(
            f'Input [yellow]{input_name}[/yellow] is not a text input.',
        )
        raise typer.Exit(1)

    ctx.obj['obsws'].set_input_settings(
        name=input_name,
        settings={'text': new_text},
        overlay=True,
    )

    if not new_text:
        new_text = '(empty)'
    console.out.print(
        f'Text for input {console.highlight(ctx, input_name)} updated to: {new_text}',
    )
