from pathlib import Path

from grout.config import get_config_dir

def _discover_in_dir(dir: Path) -> dict[str, Path]:
    widgets = {}
    for item in dir.iterdir():
        if not item.is_dir():
             continue
        for f in item.iterdir():
            if f.is_file() and f.name == "Widget.qml":
                widgets[item.name] = f

    return widgets

def discover_widgets() -> dict[str, Path]:
    config_dir = get_config_dir()
    widgets = _discover_in_dir(config_dir)
    widgets |= _discover_in_dir(Path(__file__).parent.parent / "widgets")

    return widgets

