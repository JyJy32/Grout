import typing

import PySide6.QtCore
from PySide6.QtCore import QAbstractListModel, QByteArray, QModelIndex, Qt, QObject


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
            return app["Icon"]
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
