"""
cli generation for the igen
"""

import logging
from pathlib import Path

import typer

from . import __version__, image_processor


def setup_logging(debug: bool) -> None:
    """
    setup the logging for the ongoing process
    """
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(message)s")

    logger = logging.getLogger(__name__)

    stream = logging.StreamHandler()
    stream.setLevel(logging.INFO)

    logger.addHandler(stream)


cli = typer.Typer(name="igen")


def version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.callback()
def version(
    _: bool | None = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
    ),
): ...


@cli.command()
def image(img: Path, debug: bool = False, chezmoi: bool = False):
    """Process images and convert."""
    setup_logging(debug)
    image = image_processor(img)
    image.process(chezmoi)
