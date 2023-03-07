"""
Custom icon resizer for linux icons
"""
import argparse
import copy
import shutil
from pathlib import Path

from cairosvg import svg2png  # type: ignore
from PIL import Image

from .config import Config

cfg = Config()


def convert(image: Path) -> Path:
    """
    accept svg file and convert to png file
    """
    name = image.stem
    new_path = Path(f"/tmp/{name}.png")
    svg2png(url=str(image), write_to=str(new_path))

    return new_path


def resizer(image: Path) -> None:
    """
    resize png image to various iocn size, final file name is root file name append by
    size. For example Bitwarden.png will have name Bitwarden_128.png ...

    :param image: image path
    """
    img = Image.open(image)

    for size in cfg.SIZES:
        cp = copy.deepcopy(img)
        img_mod = cp.resize(size)
        # for unique name resize image has ___
        filename = f"{image.stem}___{size[0]}.png"
        filepath = cfg.CURRENT_DIR / filename
        img_mod.save(filepath, bitmap_format="png")


def process(cfg: argparse.Namespace):
    """
    work on given image, if svg found convert to png first and then perform the
    resize

    :param image: image that needs to process
    """
    image = cfg.img
    if cfg.img.name.endswith("svg"):
        image = convert(cfg.img)

    resizer(image)

    # lets make sure chezmoi is passed and CHEZMOI_ICONS does exists
    if cfg.chezmoi and cfg.CHEZMOI_ICONS.is_dir():
        for file in cfg.CURRENT_DIR.iterdir():
            # out of all the files, if the image name match with what passed
            if image.stem in file.name and "___" in file.name:
                _, size = file.stem.split("___")
                shutil.move(
                    file, cfg.CHEZMOI_ICONS / f"{size}x{size}" / "apps" / image.name
                )
