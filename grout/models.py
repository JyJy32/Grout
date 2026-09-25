from pathlib import Path
import typing

import PySide6.QtCore
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, QUrl, Qt, QObject, Slot

from grout import palette
from grout.iconprovider import compute_tile_color


class AppListModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
    ExecRole = Qt.ItemDataRole.UserRole + 2
    IconRole = Qt.ItemDataRole.UserRole + 3
    CommentRole = Qt.ItemDataRole.UserRole + 4
    def __init__(self, apps, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._apps = apps

    def rowCount(self, /, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._apps)

    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, role: int = 0) -> typing.Any:
        if not index.isValid():
            return None
        app = self._apps[index.row()]
        if role == self.NameRole:
            return app["name"]
        if role == self.ExecRole:
            return app["exec"]
        if role == self.IconRole:
            return app["icon"]
        if role == self.CommentRole:
            return app["comment"]

        return None

    def roleNames(self) -> typing.Dict[int, PySide6.QtCore.QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.ExecRole: QByteArray(b"exec_"),
            self.IconRole: QByteArray(b"icon"),
            self.CommentRole: QByteArray(b"comment"),
        }

class TileListModel(QAbstractListModel):
    TileTypeRole = Qt.ItemDataRole.UserRole + 1
    NameRole = Qt.ItemDataRole.UserRole + 2
    ColSpanRole = Qt.ItemDataRole.UserRole + 3
    RowSpanRole = Qt.ItemDataRole.UserRole + 4
    PayloadRole = Qt.ItemDataRole.UserRole + 5
    QmlSourceRole = Qt.ItemDataRole.UserRole + 6

    # TODO: type hint the params
    def __init__(self, tiles, app_tile_qml, widgets_registry, palette, on_change=None, parent: PySide6.QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._app_tile_qml = app_tile_qml
        self._widgets_registry = widgets_registry  # {widget_name: Path to Widget.qml}
        self._palette = palette
        self._theme_colors = palette["colors"]
        self._on_change = on_change
        self._tiles = [self._resolve(t) for t in tiles]

    def _resolve(self, tile: dict) -> dict:
        """attach a runtime qmlSource to a persisted tile dict."""
        resolved = dict(tile)
        if resolved["type"] == "app":
            # color check for old stuff:
            if not "color" in  resolved["payload"].keys():
                resolved["payload"]["color"] = compute_tile_color(resolved["name"], self._theme_colors, self._palette["surface"])
            resolved["qmlSource"] = self._app_tile_qml
        else:
            widget_path = self._widgets_registry.get(resolved.get("name"))
            if widget_path is None:
                print(f"widget: {resolved.get('name')} no source found")
                resolved["qmlSource"] = QUrl()
            else:
                resolved["qmlSource"] = QUrl.fromLocalFile(str(widget_path))
        return resolved

    def _notify_change(self):
        if self._on_change:
            self._on_change(self.serialize())

    def rowCount(self, /, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._tiles)

    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, /, role: int = 0) -> typing.Any:
        if not index.isValid():
            return None
        tile = self._tiles[index.row()]
        if role == self.TileTypeRole:
            return tile["type"]
        if role == self.NameRole:
            return tile.get("name", "")
        if role == self.ColSpanRole:
            return tile.get("colSpan", 1)
        if role == self.RowSpanRole:
            return tile.get("rowSpan", 1)
        if role == self.PayloadRole:
            return tile.get("payload", {})
        if role == self.QmlSourceRole:
            return tile["qmlSource"]  # absolute file:// path to this tile's QML
        return None

    def roleNames(self):
        return {
            self.TileTypeRole: QByteArray(b"tileType"),
            self.NameRole: QByteArray(b"name"),
            self.ColSpanRole: QByteArray(b"colSpan"),
            self.RowSpanRole: QByteArray(b"rowSpan"),
            self.PayloadRole: QByteArray(b"payload"),
            self.QmlSourceRole: QByteArray(b"qmlSource"),
        }

    def serialize(self):
        """ JSON-safe snapshot, drops the qmlSource field"""
        return [{k: v for k, v in t.items() if k != "qmlSource"} for t in self._tiles]

    @Slot(int, int, int)
    def resizeTile(self, row: int, colSpan: int, rowSpan: int):
        if not (0 <= row < len(self._tiles)):
            return
        self._tiles[row]["colSpan"] = colSpan
        self._tiles[row]["rowSpan"] = rowSpan

        idx = self.index(row, 0)
        self.dataChanged.emit(idx, idx, [self.ColSpanRole, self.RowSpanRole])
        self._notify_change()

    @Slot(int)
    def removeTile(self, row: int):
        if not (0 <= row < len(self._tiles)):
            return
        self.beginRemoveRows(QModelIndex(), row, row)
        del self._tiles[row]
        self.endRemoveRows()
        self._notify_change()

    @Slot("QVariant")
    def addAppTile(self, app):
        if hasattr(app, "toVariant"):
            app = app.toVariant()
        color = compute_tile_color(app.get("icon", ""), self._theme_colors, fallback=self._palette["surface"])
        tile = self._resolve({
            "type": "app",
            "name": app["name"],
            "colSpan": 1,
            "rowSpan": 1,
            "payload": {"exec": app["exec"], "icon": app.get("icon", ""), "color": color},
        })
        row = len(self._tiles)
        self.beginInsertRows(QModelIndex(), row, row)
        self._tiles.append(tile)
        self.endInsertRows()
        self._notify_change()

    @Slot("QVariant")
    def addWidgetTile(self, widget):
        if hasattr(widget, "toVariant"):
            widget = widget.toVariant()
        tile = self._resolve({
            "type": "widget",
            "name": widget["name"],
            "colSpan": 1,
            "rowSpan": 1,
            "payload": {}
        })
        row = len(self._tiles)
        self.beginInsertRows(QModelIndex(), row, row)
        self._tiles.append(tile)
        self.endInsertRows()
        self._notify_change()

class WidgetListModel(QAbstractListModel):
    NameRole = Qt.ItemDataRole.UserRole + 1
    PathRole = Qt.ItemDataRole.UserRole + 2

    def __init__(self, widgets: dict[str, Path], parent: PySide6.QtCore.QObject | None = None) -> None:
        super().__init__(parent)
        self._widgets = [{"name": wk, "path": str(wp)} for (wk, wp) in widgets.items()]

    def rowCount(self, /, parent: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex = QModelIndex()) -> int:
        return len(self._widgets)

    def data(self, index: PySide6.QtCore.QModelIndex | PySide6.QtCore.QPersistentModelIndex, /, role: int = 0) -> typing.Any:
        if not index.isValid():
            return None
        widget = self._widgets[index.row()]
        if role == self.NameRole:
            return widget["name"]
        elif role == self.PathRole:
            return widget["path"]

    def roleNames(self, /) -> typing.Dict[int, PySide6.QtCore.QByteArray]:
        return {
            self.NameRole: QByteArray(b"name"),
            self.PathRole: QByteArray(b"role"),
        }

