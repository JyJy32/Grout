#!/usr/bin/env python
import sys
from pathlib import Path
from typing import cast
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QGuiApplication, QWindow
from PySide6.QtQml import QQmlApplicationEngine

from grout.apps import get_desktop_entries
from grout.daemon import ToggleServer
from grout.models import AppListModel

# debug:
pinned = [
    {"name": "Firefox", "exec": "...", "colSpan": 2, "rowSpan": 2},  # big tile
    {"name": "Terminal", "exec": "...", "colSpan": 1, "rowSpan": 1}, # normal tile
    {"name": "Files", "exec": "...", "colSpan": 1, "rowSpan": 1},    # wide tile
]

def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    apps = get_desktop_entries()
    app_model = AppListModel(apps)

    proxy = QSortFilterProxyModel()
    proxy.setSourceModel(app_model)
    proxy.setFilterRole(AppListModel.NameRole)
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity(False))
    proxy.setDynamicSortFilter(True)

    engine.rootContext().setContextProperty("searchModel", proxy)
    engine.rootContext().setContextProperty("pinnedTiles", pinned)

    qml_path = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(str(qml_path))

    if not engine.rootObjects():
        sys.exit(-1)

    window = cast(QWindow, engine.rootObjects()[0])
    window.setVisible(False)

    server: ToggleServer = ToggleServer()

    def handle_toggle():
        if window.isVisible():
            window.setVisible(False)
        else:
            window.setVisible(True)
            window.requestActivate()
            window.raise_()

    server.toggle_requested.connect(handle_toggle)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
