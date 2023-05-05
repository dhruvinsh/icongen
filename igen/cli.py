"""
cli generation for the igen
"""
import logging
from pathlib import Path

import click

from . import ImageProcess, __version__


def setup_logging(debug: bool):
    """
    setup the logging for the ongoing process
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

    logger = logging.getLogger(__name__)

    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)

    logger.addHandler(stream)


@click.command()
@click.option("--debug", is_flag=True, help="Enable debug messages")
@click.option("--chezmoi", is_flag=True, help="Copy processed img to chezmoi directory")
@click.version_option(__version__)
@click.argument("img", required=True, type=Path)
def cli(debug: bool, chezmoi: bool, img: Path):
    """
    process on image and convert to appropriate size for linux maching to use
    """
    setup_logging(debug)
    ip = ImageProcess(img)
    ip.process(chezmoi)
