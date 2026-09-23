import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtQuick import QQuickImageProvider

DEFAULT_THEME = "Catppuccin-Mocha"

def detect_icon_theme():
    if os.environ.get("GNOME_DESKTOP_SESSION_ID") or os.environ.get("XDG_CURRENT_DESKTOP") in ("GNOME", "Cinnamon", "MATE"):
        return None
    if os.environ.get("KDE_FULL_SESSION") == "true":
        return None
    if os.environ.get("DESKTOP_SESSION") == "xfce":
        return None
    return DEFAULT_THEME

class IconProvider(QQuickImageProvider):
    def __init__(self) -> None:
        theme = detect_icon_theme()
        if theme:
            QIcon.setThemeName(theme)

        super().__init__(QQuickImageProvider.ImageType.Pixmap)

    def requestPixmap(self, icon_name: str, size: QSize, requestedSize: QSize, /) -> QPixmap:
        icon = QIcon.fromTheme(icon_name)

        w = requestedSize.width() if requestedSize.width() > 0 else 64
        h = requestedSize.height() if requestedSize.height() > 0 else 64

        pixmap = icon.pixmap(w, h)

        if size:
            size.setWidth(pixmap.width())
            size.setHeight(pixmap.height())

        return pixmap
