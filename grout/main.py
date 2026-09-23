#!/usr/bin/env python
import sys
from pathlib import Path
from PySide6.QtCore import QSortFilterProxyModel, Qt
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from grout.apps import get_desktop_entries
from grout.models import AppListModel

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

    qml_path = Path(__file__).parent / "qml" / "Main.qml"
    engine.load(str(qml_path))

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
