#!/usr/bin/env python
import sys
from pathlib import Path
from typing import cast
from PySide6.QtCore import QSortFilterProxyModel, QUrl, Qt
from PySide6.QtGui import QGuiApplication, QWindow
from PySide6.QtQml import QQmlApplicationEngine

from grout import launcher
from grout.apps import get_desktop_entries
from grout.config import load_tiles, save_tiles
from grout.daemon import ToggleServer
from grout.models import AppListModel, TileListModel
from grout.launcher import Launcher
from grout.widgets import discover_widgets

# TODO: 
# -[] widget discovery
# -[] xdg themes


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

    add_tile_proxy = QSortFilterProxyModel()
    add_tile_proxy.setSourceModel(app_model)
    add_tile_proxy.setFilterRole(AppListModel.NameRole)
    add_tile_proxy.setFilterCaseSensitivity(Qt.CaseSensitivity(False))
    add_tile_proxy.setDynamicSortFilter(True)
    engine.rootContext().setContextProperty("addTileSearchModel", add_tile_proxy)

    widgets_registry = discover_widgets()

    app_tile_qml = QUrl.fromLocalFile(
        str(Path(__file__).parent / "qml" / "tiles" / "AppTile.qml")
    )
    default_tiles = [
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
    weather_widget_qml = QUrl.fromLocalFile(
        str(Path(__file__).parent.parent / "widgets" / "weather" / "Widget.qml"))
    weather_tile = {
        "type": "widget",
        "name": "Weather",
        "colSpan": 1,
        "rowSpan": 1,
        "payload": {"latitude": 51.2194, "longitude": 4.4025},
        "qmlSource": weather_widget_qml
    }

    default_tiles.append(weather_tile)
    pinned_tiles = load_tiles(default_tiles)
    pinned_model = TileListModel(pinned_tiles, app_tile_qml=app_tile_qml, widgets_registry=widgets_registry, on_change=save_tiles)

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
