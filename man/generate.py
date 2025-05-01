"""script for generating man pages for the CLI."""

# /// script
# dependencies = [
#   "typer>=0.15.2",
#   "click-man>=0.5.1",
#   "obsws-cli",
# ]
#
# [tool.uv.sources]
# obsws-cli = { path = "../" }
# ///

import argparse
from pathlib import Path

import typer
from click_man.core import write_man_pages

from obsws_cli import app
from obsws_cli.__about__ import __version__


def main(target_dir: str):
    """Generate man pages for the CLI."""
    cli = typer.main.get_command(app)
    name = 'obsws-cli'
    version = __version__
    write_man_pages(name, cli, version=version, target_dir=target_dir)


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate man pages for the CLI.')
    parser.add_argument(
        '--output',
        type=str,
        default=str(Path(__file__).parent),
        help='Directory to save man pages',
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    main(args.output)
