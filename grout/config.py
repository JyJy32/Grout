import json
import os
from pathlib import Path

def get_config_dir() -> Path:
    config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
    config_dir = config_home / "grout"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir

def load_tiles(default_tiles: list[dict] = []) -> list[dict]:
    path = get_config_dir() / "tiles.json"
    if not path.is_file():
        return default_tiles
    try:
        with path.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"grout: failed to read {path}")
        return default_tiles

def save_tiles(tiles: list[dict]) -> None:
    path = get_config_dir() / "tiles.json"
    tmp = path.with_suffix(".jsos.tmp")
    with tmp.open("w") as f:
        json.dump(tiles, f, indent=2)
    tmp.replace(path)
