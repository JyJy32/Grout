import os
from pathlib import Path
import socket

from PySide6.QtCore import QObject, QSocketNotifier, Signal


def get_socket_path():
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
    return Path(runtime_dir) / "grout.sock"

class ToggleServer(QObject):
    toggle_requested = Signal()

    def __init__(self, /, parent: QObject | None = None, *, objectName: str | None = None) -> None:
        super().__init__(parent, objectName=objectName)
        self.socket_path = get_socket_path()

        if self.socket_path.exists():
            self.socket_path.unlink()

        self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self._sock.bind(str(self.socket_path))
        self._sock.listen(1)
        self._sock.setblocking(False)

        self._notifier = QSocketNotifier(self._sock.fileno(), QSocketNotifier.Type.Read)
        self._notifier.activated.connect(self._on_activity)

    def _on_activity(self):
        try:
            conn, _ = self._sock.accept()
            data = conn.recv(64)
            conn.close()
            if data:
                self.toggle_requested.emit()
        except OSError:
            pass

    def close(self):
        self._notifier.setEnabled(False)
        self._sock.close()
        if self.socket_path.exists():
            self.socket_path.unlink()
