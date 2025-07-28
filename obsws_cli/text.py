"""module containing commands for manipulating text inputs."""

from typing import Annotated, Optional

from cyclopts import App, Parameter

from . import console, validate
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='text', help='Commands for controlling text inputs in OBS.')


@app.command(name=['current', 'get'])
def current(
    input_name: str,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the current text for a text input.

    Parameters
    ----------
    input_name : str
        The name of the text input to retrieve the current text from.
    ctx : Context
        The context containing the OBS client and other settings.

    """
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
    input_name: str,
    new_text: Optional[str] = None,
    /,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Update the text of a text input.

    Parameters
    ----------
    input_name : str
        The name of the text input to update.
    new_text : Optional[str]
        The new text to set for the input. If not provided, the text will be cleared
        (set to an empty string).
    ctx : Context
        The context containing the OBS client and other settings.

    """
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
