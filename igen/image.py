"""
Custom icon resizer for linux icons
"""
import copy
import logging
import shutil
import sys
from pathlib import Path

from cairosvg import svg2png  # type: ignore
from PIL import Image as pimage

from .config import Config

cfg = Config()


class ImageProcess:
    """
    Image processing class
    """

    def __init__(self, image: Path):
        self.image = image
        self.logger = logging.getLogger(self.__class__.__name__)

    def convert(self) -> Path:
        """
        accept svg file and convert to png file
        """
        self.logger.info(f"converting svg image: {self.image}")
        name = self.image.stem
        new_path = Path(f"/tmp/{name}.png")
        svg2png(url=str(self.image), write_to=str(new_path))
        self.logger.debug(f"converted to png file: {new_path}")

        return new_path

    def resizer(self) -> None:
        """
        resize png image to various iocn size, final file name is root file name append
        by size. For example Bitwarden.png will have name Bitwarden_128.png ...

        :param image: image path
        """
        img = pimage.open(self.image)

        for size in cfg.SIZES:
            cp = copy.deepcopy(img)
            img_mod = cp.resize(size)
            # for unique name resize image has ___
            filename = f"{self.image.stem}___{size[0]}.png"
            filepath = cfg.CURRENT_DIR / filename
            img_mod.save(filepath, bitmap_format="png")
            self.logger.debug(f"image resize: {size} stored: {filepath}")

    def process(self, chezmoi: bool = False):
        """
        work on given image, if svg found convert to png first and then perform the
        resize

        :param chezmoi: if chezmoi process is required
        """
        if not (self.image.exists() and self.image.is_file()):
            self.logger.error(f"Image file not found: {self.image}")
            sys.exit(1)

        # svg converter
        if self.image.name.endswith("svg"):
            self.logger.debug("SVG image detected")
            # update image with converted path
            self.image = self.convert()

        self.resizer()

        # lets make sure chezmoi is passed and CHEZMOI_ICONS does exists
        if chezmoi and cfg.CHEZMOI_ICONS.is_dir():
            for file in cfg.CURRENT_DIR.iterdir():
                # out of all the files, if the image name match with what passed
                if self.image.stem in file.name and "___" in file.name:
                    _, size = file.stem.split("___")
                    destination = (
                        cfg.CHEZMOI_ICONS / f"{size}x{size}" / "apps" / self.image.name
                    )
                    shutil.move(file, destination)
        self.logger.info("image processing completed")
