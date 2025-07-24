"""module containing commands for manipulating text inputs."""

from typing import Annotated, Optional

from cyclopts import App, Argument, Parameter

from . import console, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='text', help='Commands for controlling text inputs in OBS.')


@app.command(name=['current', 'get'])
def current(
    input_name: Annotated[str, Argument(hint='Name of the text input to get.')],
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the current text for a text input."""
    if not validate.input_in_inputs(ctx, input_name):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] not found.', code=ExitCode.ERROR
        )

    resp = ctx.client.get_input_settings(name=input_name)
    if not resp.input_kind.startswith('text_'):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] is not a text input.',
            code=ExitCode.ERROR,
        )

    current_text = resp.input_settings.get('text', '')
    if not current_text:
        current_text = '(empty)'
    console.out.print(
        f'Current text for input {console.highlight(ctx, input_name)}: {current_text}',
    )


@app.command(name=['update', 'set'])
def update(
    input_name: Annotated[str, Argument(hint='Name of the text input to update.')],
    new_text: Annotated[
        Optional[str],
        Argument(hint='The new text to set for the input.'),
    ] = None,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Update the text of a text input."""
    if not validate.input_in_inputs(ctx, input_name):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] not found.', code=ExitCode.ERROR
        )

    resp = ctx.client.get_input_settings(name=input_name)
    if not resp.input_kind.startswith('text_'):
        raise OBSWSCLIError(
            f'Input [yellow]{input_name}[/yellow] is not a text input.',
            code=ExitCode.ERROR,
        )

    ctx.client.set_input_settings(
        name=input_name,
        settings={'text': new_text},
        overlay=True,
    )

    if not new_text:
        new_text = '(empty)'
    console.out.print(
        f'Text for input {console.highlight(ctx, input_name)} updated to: {new_text}',
    )
