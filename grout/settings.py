from pathlib import Path

from PySide6.QtCore import Property, QObject, QStringListModel, Signal, Slot

from grout.config import Config, save_config


class SettingsController(QObject):
    changed = Signal()

    def __init__(self, config: Config, palettes_dir: Path, parent: QObject | None = None,) -> None:
        super().__init__(parent)
        self._config = config
        self._palettes_dir = palettes_dir

    @Property(str, notify=changed)
    def currentPalette(self) -> str:
        return self._config.current_palette

    @Property(str, notify=changed)
    def terminal(self) -> str:
        return self._config.terminal

    @Property(list, notify=changed)
    def palettes(self) -> list[str]:
        names: set[str] = {self._config.current_palette}
        if self._palettes_dir.is_dir():
            names |= {p.stem for p in self._palettes_dir.iterdir() if p.is_file()}
        return sorted(names)
 
    @Slot(str, str)
    def apply(self, palette: str, terminal: str) -> None:
        # Mutate the shared Config in place so Launcher (which holds the
        # same object) sees the new terminal immediately.
        self._config.current_palette = palette.strip() or self._config.current_palette
        self._config.terminal = terminal.strip() or "xterm"
        save_config(self._config)
        self.changed.emit()
