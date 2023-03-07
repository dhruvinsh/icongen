from argparse import ArgumentParser
from pathlib import Path

from src import __version__, process

parser = ArgumentParser(
    prog="icon generator",
    description="general purpose icon generator for linux systems",
)
parser.add_argument(
    "--img", required=True, type=Path, help="Provide svg or png image file"
)
parser.add_argument(
    "--debug",
    action="store_true",
    default=False,
    help="Enable debug messages",
)
parser.add_argument(
    "--chezmoi",
    action="store_true",
    default=False,
    help="Copy various size png to chezmoi directory",
)
parser.add_argument(
    "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
)

args = parser.parse_args()

process(args)
