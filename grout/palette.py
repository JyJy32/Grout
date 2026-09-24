import json
import os
from pathlib import Path

from grout.config import Config, get_config_dir

def _discover_in_dir(dir: Path) -> dict[str, Path]:
    palettes = {}
    for item in dir.iterdir():
        if item.is_dir():
             continue
        if item.is_file() and item.suffix == ".json":
            palettes[item.stem] = item

    return palettes

def discover_palettes() -> dict[str, Path]:
    config_dir = get_config_dir() / "themes"
    config_dir.mkdir(parents=True, exist_ok=True)
    palettes = _discover_in_dir(config_dir)
    palettes |= _discover_in_dir(Path(__file__).parent.parent / "themes")
    return palettes


def get_user_palette_path(config: Config) -> Path:
    palettes = discover_palettes()
    if not config.current_palette in palettes.keys():
        print(f"grout: selected palette: {config.current_palette} not available")
        return palettes["catppuccin-mocha"]
    return palettes[config.current_palette]

def load_palette(path: Path) -> dict:
    with path.open("r") as f:
        palette = json.load(f)
    return palette
