"""Command line interface for the OBS WebSocket API."""

import importlib
import logging
import pkgutil
from typing import Annotated

import obsws_python as obsws
import typer

from obsws_cli.__about__ import __version__ as version

from . import commands, console, envconfig, styles
from .alias import RootTyperAliasGroup

app = typer.Typer(cls=RootTyperAliasGroup)
for importer, modname, ispkg in pkgutil.iter_modules(
    commands.__path__, commands.__name__ + '.'
):
    subtyper = importlib.import_module(modname)
    app.add_typer(subtyper.app, name=modname.split('.')[-1])


def version_callback(value: bool):
    """Show the version of the CLI."""
    if value:
        console.out.print(f'obsws-cli version: {version}')
        raise typer.Exit()


def setup_logging(loglevel: str):
    """Set up logging for the application."""
    level_map = logging.getLevelNamesMapping()
    try:
        level_int = level_map[loglevel.upper()]
    except KeyError:
        possible_levels = ', '.join(
            sorted(level_map.keys(), key=lambda k: level_map[k])
        )
        raise typer.BadParameter(
            f'Invalid log level: {loglevel}. Valid options are: {possible_levels}'
        ) from None

    logging.basicConfig(
        level=level_int,
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
            envvar='OBSWS_CLI_HOST',
            help='WebSocket host',
            show_default='localhost',
        ),
    ] = envconfig.get('host'),
    port: Annotated[
        int,
        typer.Option(
            '--port',
            '-P',
            envvar='OBSWS_CLI_PORT',
            help='WebSocket port',
            show_default=4455,
        ),
    ] = envconfig.get('port'),
    password: Annotated[
        str,
        typer.Option(
            '--password',
            '-p',
            envvar='OBSWS_CLI_PASSWORD',
            help='WebSocket password',
            show_default=False,
        ),
    ] = envconfig.get('password'),
    timeout: Annotated[
        int,
        typer.Option(
            '--timeout',
            '-T',
            envvar='OBSWS_CLI_TIMEOUT',
            help='WebSocket timeout',
            show_default=5,
        ),
    ] = envconfig.get('timeout'),
    style: Annotated[
        str,
        typer.Option(
            '--style',
            '-s',
            envvar='OBSWS_CLI_STYLE',
            help='Set the style for the CLI output',
            show_default='disabled',
            callback=validate_style,
        ),
    ] = envconfig.get('style'),
    no_border: Annotated[
        bool,
        typer.Option(
            '--no-border',
            '-b',
            envvar='OBSWS_CLI_STYLE_NO_BORDER',
            help='Disable table border styling in the CLI output',
            show_default=False,
        ),
    ] = envconfig.get('style_no_border'),
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
    loglevel: Annotated[
        str,
        typer.Option(
            '--loglevel',
            '-l',
            envvar='OBSWS_CLI_LOGLEVEL',
            is_eager=True,
            help='Set the logging level',
            show_default=False,
            callback=setup_logging,
        ),
    ] = envconfig.get('loglevel'),
):
    """obsws_cli is a command line interface for the OBS WebSocket API."""
    ctx.ensure_object(dict)
    ctx.obj['obsws'] = ctx.with_resource(
        obsws.ReqClient(host=host, port=port, password=password, timeout=timeout)
    )
    ctx.obj['style'] = styles.request_style_obj(style, no_border)


@app.command()
def obs_version(ctx: typer.Context):
    """Get the OBS Client and WebSocket versions."""
    resp = ctx.obj['obsws'].get_version()
    console.out.print(
        f'OBS Client version: {console.highlight(ctx, resp.obs_version)}'
        f' with WebSocket version: {console.highlight(ctx, resp.obs_web_socket_version)}'
    )
