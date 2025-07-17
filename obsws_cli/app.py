"""Command line interface for the OBS WebSocket API."""

import importlib
from dataclasses import dataclass
from typing import Annotated

import obsws_python as obsws
from cyclopts import App, Group, Parameter, config

from . import console, styles
from .context import Context

app = App(
    config=config.Env(
        'OBS_'
    ),  # Environment variable prefix for configuration parameters
)
app.meta.group_parameters = Group('Session Parameters', sort_key=0)
for sub_app in ('scene',):
    module = importlib.import_module(f'.{sub_app}', package=__package__)
    app.command(module.app)


@Parameter(name='*')
@dataclass
class OBSConfig:
    """Dataclass to hold OBS connection parameters."""

    host: str = 'localhost'
    port: int = 4455
    password: str = ''


@dataclass
class StyleConfig:
    """Dataclass to hold style parameters."""

    name: str = 'disabled'
    no_border: bool = False


@app.meta.default
def launcher(
    *tokens: Annotated[str, Parameter(show=False, allow_leading_hyphen=True)],
    obs_config: OBSConfig = Annotated[
        OBSConfig,
        Parameter(
            show=False, allow_leading_hyphen=True, help='OBS connection parameters'
        ),
    ],
    style_config: StyleConfig = Annotated[
        StyleConfig,
        Parameter(show=False, allow_leading_hyphen=True, help='Style parameters'),
    ],
):
    """Initialize the OBS WebSocket client and return the context."""
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
    """Run the OBS WebSocket CLI."""
    app.meta()
