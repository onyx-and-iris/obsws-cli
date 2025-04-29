"""script for generating man pages for the CLI."""

import typer
from click_man.core import write_man_pages

from obsws_cli import app
from obsws_cli.__about__ import __version__


def make_man():
    """Generate man pages for the CLI."""
    cli = typer.main.get_command(app)
    name = 'obsws-cli'
    version = __version__
    target_dir = './man'
    write_man_pages(name, cli, version=version, target_dir=target_dir)


if __name__ == '__main__':
    make_man()
