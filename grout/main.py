#!/usr/bin/env python
import sys
from pathlib import Path
from typing import cast
from PySide6.QtCore import QSortFilterProxyModel, QUrl, Qt
from PySide6.QtGui import QGuiApplication, QWindow
from PySide6.QtQml import QQmlApplicationEngine

from grout import launcher
from grout.apps import get_desktop_entries
from grout.daemon import ToggleServer
from grout.models import AppListModel, TileListModel
from grout.launcher import Launcher


def main():
    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()

    launcher = Launcher()
    engine.rootContext().setContextProperty("launcher", launcher)

    apps = get_desktop_entries()
    app_model = AppListModel(apps)

    proxy = QSortFilterProxyModel()
    proxy.setSourceModel(app_model)
    proxy.setFilterRole(AppListModel.NameRole)
    proxy.setFilterCaseSensitivity(Qt.CaseSensitivity(False))
    proxy.setDynamicSortFilter(True)

    engine.rootContext().setContextProperty("searchModel", proxy)

    app_tile_qml = QUrl.fromLocalFile(
        str(Path(__file__).parent / "qml" / "tiles" / "AppTile.qml")
    )
    pinned_tiles = [
        {
            "type": "app",
            "name": a["name"],
            "colSpan": 1,
            "rowSpan": 1,
            "payload": {"exec": a["exec"], "icon": a["icon"]},
            "qmlSource": app_tile_qml,
        }
        for a in apps[:6]
    ]
    pinned_model = TileListModel(pinned_tiles)

    engine.rootContext().setContextProperty("pinnedTiles", pinned_model)


    qml_path = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(str(qml_path))

    window = cast(QWindow, engine.rootObjects()[0])
    engine.rootContext().setContextProperty("mainWindow", window)
    if not engine.rootObjects():
        sys.exit(-1)

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
