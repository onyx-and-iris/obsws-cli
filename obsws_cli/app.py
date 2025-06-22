"""Command line interface for the OBS WebSocket API."""

import importlib
import logging
from typing import Annotated

import obsws_python as obsws
import typer

from obsws_cli.__about__ import __version__ as version

from . import console, settings, styles
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
        console.out.print(f'obsws-cli version: {version}')
        raise typer.Exit()


def setup_logging(debug: bool):
    """Set up logging for the application."""
    log_level = logging.DEBUG if debug else logging.CRITICAL
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )


def validate_style(value: str):
    """Validate and return the style."""
    if value not in styles.registry:
        raise typer.BadParameter(
            f'Invalid style: {value}. Available styles: {", ".join(styles.registry.keys())}'
        )
    return value


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
    style: Annotated[
        str,
        typer.Option(
            '--style',
            '-s',
            envvar='OBS_STYLE',
            help='Set the style for the CLI output',
            show_default='disabled',
            callback=validate_style,
        ),
    ] = settings.get('style'),
    no_border: Annotated[
        bool,
        typer.Option(
            '--no-border',
            '-b',
            envvar='OBS_STYLE_NO_BORDER',
            help='Disable table border styling in the CLI output',
            show_default=False,
        ),
    ] = settings.get('style_no_border'),
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
    ctx.ensure_object(dict)
    ctx.obj['obsws'] = ctx.with_resource(obsws.ReqClient(**ctx.params))
    ctx.obj['style'] = styles.request_style_obj(style, no_border)


@app.command()
def obs_version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj['obsws'].get_version()
    console.out.print(
        f'OBS Client version: {console.highlight(ctx, resp.obs_version)}'
        f' with WebSocket version: {console.highlight(ctx, resp.obs_web_socket_version)}'
    )
