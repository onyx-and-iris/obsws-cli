"""module for taking screenshots using OBS WebSocket API."""

from pathlib import Path
from typing import Annotated

import obsws_python as obsws
from cyclopts import App, Parameter, validators

from . import console
from .context import Context
from .enum import ExitCode
from .error import OBSWSCLIError

app = App(name='screenshot', help='Commands for taking screenshots using OBS.')


@app.command(name=['save', 'sv'])
def save(
    source_name: str,
    # Since the CLI and OBS may be running on different platforms,
    # we won't validate the path here.
    output_path: Path,
    /,
    width: float = 1920,
    height: float = 1080,
    quality: Annotated[
        float, Parameter(validator=validators.Number(gte=-1, lte=100))
    ] = -1.0,
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Take a screenshot and save it to a file.

    Parameters
    ----------
    source_name : str
        Name of the source to take a screenshot of.
    output_path : Path
        Path to save the screenshot (must include file name and extension).
    width : float
        Width of the screenshot.
    height : float
        Height of the screenshot.
    quality : float
        Quality of the screenshot. A value of -1 uses the default quality.
    ctx : Context
        Context containing the OBS WebSocket client instance.

    """
    try:
        ctx.client.save_source_screenshot(
            name=source_name,
            img_format=output_path.suffix.lstrip('.').lower(),
            file_path=str(output_path),
            width=width,
            height=height,
            quality=quality,
        )
    except obsws.error.OBSSDKRequestError as e:
        match e.code:
            case 403:
                raise OBSWSCLIError(
                    'The [yellow]image format[/yellow] (file extension) must be included in the file name, '
                    "for example: '/path/to/screenshot.png'.",
                    code=ExitCode.ERROR,
                )
            case 600:
                raise OBSWSCLIError(
                    'No source was found by the name of [yellow]{source_name}[/yellow]',
                    code=ExitCode.ERROR,
                )
            case _:
                raise

    console.out.print(f'Screenshot saved to {console.highlight(ctx, output_path)}.')
