"""Command line interface for the OBS WebSocket API."""

import importlib
import logging
from typing import Annotated

import obsws_python as obsws
import typer

from obsws_cli.__about__ import __version__ as obsws_cli_version

from . import console, settings
from .alias import RootTyperAliasGroup

app = typer.Typer(cls=RootTyperAliasGroup)
for sub_typer in (
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
    'virtualcam',
):
    module = importlib.import_module(f'.{sub_typer}', package=__package__)
    app.add_typer(module.app, name=sub_typer)


def version_callback(value: bool):
    """Show the version of the CLI."""
    if value:
        console.out.print(f'obsws-cli version: {obsws_cli_version}')
        raise typer.Exit()


def setup_logging(debug: bool):
    """Set up logging for the application."""
    log_level = logging.DEBUG if debug else logging.CRITICAL
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


@app.callback()
def main(
    ctx: typer.Context,
    host: Annotated[
        str,
        typer.Option(
            '--host',
            '-H',
            envvar='OBS_HOST',
            help='WebSocket host',
            show_default='localhost',
        ),
    ] = settings.get('host'),
    port: Annotated[
        int,
        typer.Option(
            '--port',
            '-P',
            envvar='OBS_PORT',
            help='WebSocket port',
            show_default=4455,
        ),
    ] = settings.get('port'),
    password: Annotated[
        str,
        typer.Option(
            '--password',
            '-p',
            envvar='OBS_PASSWORD',
            help='WebSocket password',
            show_default=False,
        ),
    ] = settings.get('password'),
    timeout: Annotated[
        int,
        typer.Option(
            '--timeout',
            '-T',
            envvar='OBS_TIMEOUT',
            help='WebSocket timeout',
            show_default=5,
        ),
    ] = settings.get('timeout'),
    version: Annotated[
        bool,
        typer.Option(
            '--version',
            '-v',
            is_eager=True,
            help='Show the CLI version and exit',
            show_default=False,
            callback=version_callback,
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            '--debug',
            '-d',
            envvar='OBS_DEBUG',
            is_eager=True,
            help='Enable debug logging',
            show_default=False,
            callback=setup_logging,
            hidden=True,
        ),
    ] = settings.get('debug'),
):
    """obsws_cli is a command line interface for the OBS WebSocket API."""
    ctx.obj = ctx.with_resource(obsws.ReqClient(**ctx.params))


@app.command()
def obs_version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj.get_version()
    console.out.print(
        f'OBS Client version: {resp.obs_version} with WebSocket version: {resp.obs_web_socket_version}'
    )
