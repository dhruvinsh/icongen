# 🖼️ Icon Generator

This tiny tool allows to generate icon from png and svg to linux compatible various icon sizes

# Usage:

For me, Linux dotfiles are managed via chezmoi tool and I had a need to convert `png` and `svg` full size icon to be converted and placed under chezmoi directory. `--chezmoi` flag does the same here for me.

Chezmoi puts the icon in my config at `CHEZMOI_DIF/home/private_dot_local/private_share/icons/hicolor/<size>x<size>`

Currently supported size are:

- 256
- 128
- 64
- 48
- 32
- 16

If `--chezmoi` flag is not provided then it place the converted icon as `<name>___<size>.png`

```
Usage: igen [OPTIONS] IMG

  process on image and convert to appropriate size for linux maching to use

Options:
  --debug    Enable debug messages
  --chezmoi  Copy processed img to chezmoi directory
  --version  Show the version and exit.
  --help     Show this message and exit.
```
