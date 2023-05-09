"""
Custom icon resizer for linux icons
"""
import copy
import logging
import shutil
from pathlib import Path
from typing import Union

from cairosvg import svg2png  # type: ignore
from PIL import Image as pimage

from .config import Config

cfg = Config()


class Image:
    """
    Base image class with common image processing
    """

    def __init__(self, image: Path) -> None:
        self.image = image
        self.logger = logging.getLogger(self.__class__.__name__)

        if not (self.image.exists() and self.image.is_file()):
            raise ValueError("Provide image/path is not valid")

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

    def process(self, chezmoi: bool = False) -> None:
        """
        work on given image, if svg found convert to png first and then perform the
        resize

        :param chezmoi: if chezmoi process is required
        """
        self.resizer()

        # lets make sure chezmoi is passed and CHEZMOI_ICONS does exists
        if chezmoi and cfg.CHEZMOI_ICONS.is_dir():
            self.logger.info("working on chezmoi images..")
            for file in cfg.CURRENT_DIR.iterdir():
                # out of all the files, if the image name match with what passed
                if self.image.stem in file.name and "___" in file.name:
                    _, size = file.stem.split("___")
                    destination = (
                        cfg.CHEZMOI_ICONS / f"{size}x{size}" / "apps" / self.image.name
                    )
                    shutil.move(file, destination)
        self.logger.info("image processing completed")


class SvgImage(Image):
    """
    SVG image processing.
    """

    def __init__(self, image: Path) -> None:
        super().__init__(image)

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

    def process(self, chezmoi: bool = False) -> None:
        """
        Process an SVG image and perform the convertion and resize

        :param chezmoi: if chezmoi process is required
        """
        # convert svg to png
        self.image = self.convert()

        super().process(chezmoi)


class PngImage(Image):
    """
    PNG image processing.
    """

    def __init__(self, image: Path) -> None:
        super().__init__(image)


def image_processor(image_path: Path) -> Union[SvgImage, PngImage]:
    """
    Create an instance of SvgImage or PngImage based on the file extension of the image
    file.

    :param image_path: The path to the image file.
    :return: An instance of SvgImage or PngImage.
    """
    if image_path.suffix.lower() == ".svg":
        return SvgImage(image_path)
    elif image_path.suffix.lower() == ".png":
        return PngImage(image_path)
    else:
        raise ValueError(f"Unsupported image format: {image_path.suffix}")
