import json
import os
from pathlib import Path

class Config():
    current_palette: str = ""
    def __init__(self, dump: dict | None = None) -> None:
        if not dump:
            self.current_palette = "catppuccin-mocha"
        else:
            self.current_palette = dump["current_palette"]

    def serialize(self) -> str:
        return f"{{ current_palette: {self.current_palette} }}"

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
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w") as f:
        json.dump(tiles, f, indent=2)
    tmp.replace(path)

def load_config() -> Config:
    path = get_config_dir() / "config.json"
    if not path.is_file():
        store_default_config()
        return Config()
    try:
        with path.open("r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        print(f"grout: failed to read {path}")
        return Config()

def save_config(cfg: Config) -> None:
    path = get_config_dir() / "config.json"
    tmp = path.with_suffix(".json.tmp")
    with tmp.open("w") as f:
        f.write(cfg.serialize())
    tmp.replace(path)

def store_default_config() -> None:
    save_config(Config())

