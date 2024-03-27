"""
Config for the icon generator
"""

from pathlib import Path


class Config:
    """Config datastore."""

    CURRENT_DIR = Path.cwd()
    HOME = Path.home()
    CHEZMOI_DIR = HOME / ".local" / "share" / "chezmoi"
    CHEZMOI_ICONS = (
        CHEZMOI_DIR
        / "home"
        / "private_dot_local"
        / "private_share"
        / "icons"
        / "hicolor"
    )
    # Linux (Mint right now) required size:
    # 256x256, 128x128, 64x64, 48x48, 32x32, 16x16
    SIZES = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
