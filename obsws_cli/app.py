"""Command line interface for the OBS WebSocket API."""

import importlib
import logging
from dataclasses import dataclass
from typing import Annotated, Any

import obsws_python as obsws
from cyclopts import App, Group, Parameter, config

from obsws_cli.__about__ import __version__ as version

from . import console, styles
from .context import Context
from .error import OBSWSCLIError

app = App(
    config=config.Env(
        'OBS_'
    ),  # Environment variable prefix for configuration parameters
    version=version,
    usage='[bold][yellow]Usage:[/yellow] [white]obsws-cli [OPTIONS] COMMAND [ARGS]...[/white][/bold]',
)
app.meta.group_parameters = Group('Options', sort_key=0)
for sub_app in (
    'filter',
    'group',
    'hotkey',
    'input',
    'profile',
    'projector',
    'record',
    'replaybuffer',
    'scene',
    'scenecollection',
    'sceneitem',
    'screenshot',
    'stream',
    'studiomode',
    'text',
    'virtualcam',
):
    module = importlib.import_module(f'.{sub_app}', package=__package__)
    app.command(module.app)


@Parameter(name='*')
@dataclass
class OBSConfig:
    """Dataclass to hold OBS connection parameters.

    Attributes:
        host (str): The hostname or IP address of the OBS WebSocket server.
        port (int): The port number of the OBS WebSocket server.
        password (str): The password for the OBS WebSocket server, if required.

    """

    host: str = 'localhost'
    port: int = 4455
    password: str = ''


@dataclass
class StyleConfig:
    """Dataclass to hold style parameters.

    Attributes:
        name (str): The name of the style to use for console output.
        no_border (bool): Whether to style the borders in the console output.

    """

    name: str = 'disabled'
    no_border: bool = False


def setup_logging(type_, value: Any):
    """Set up logging for the application."""
    log_level = logging.DEBUG if value else logging.CRITICAL
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


@app.meta.default
def launcher(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    obs_config: OBSConfig,
    style_config: StyleConfig,
    debug: Annotated[
        bool,
        Parameter(validator=setup_logging, help='Enable debug logging'),
    ] = False,
):
    """Command line interface for the OBS WebSocket API."""
    with obsws.ReqClient(
        host=obs_config.host,
        port=obs_config.port,
        password=obs_config.password,
    ) as client:
        additional_kwargs = {}
        command, bound, ignored = app.parse_args(tokens)
        if 'ctx' in ignored:
            # If 'ctx' is in ignored, it means it was not passed as an argument
            # and we need to add it to the bound arguments.
            additional_kwargs['ctx'] = ignored['ctx'](
                client,
                styles.request_style_obj(style_config.name, style_config.no_border),
            )
        return command(*bound.args, **bound.kwargs, **additional_kwargs)


@app.command
def obs_version(
    *,
    ctx: Annotated[Context, Parameter(parse=False)],
):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.client.get_version()
    console.out.print(
        f'OBS Client version: {console.highlight(ctx, resp.obs_version)}'
        f' with WebSocket version: {console.highlight(ctx, resp.obs_web_socket_version)}'
    )


def run():
    """Run the OBS WebSocket CLI application.

    Handles exceptions and prints error messages to the console.
    """
    try:
        app.meta()
    except OBSWSCLIError as e:
        console.err.print(f'Error: {e}')
        return e.code
