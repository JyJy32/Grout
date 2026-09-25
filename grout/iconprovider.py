import os

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon, QImage, QPixmap
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


# icon color
def resolve_icon_image(icon_name: str, size: int = 32) -> QImage | None:
    if not icon_name:
        return None
    icon = QIcon.fromTheme(icon_name)
    if icon.isNull():
        return None
    pixmap = icon.pixmap(size, size)
    if pixmap.isNull():
        return None
    return pixmap.toImage()

def average_color(image: QImage) -> tuple[int, int, int] | None:
    image = image.convertToFormat(QImage.Format.Format_RGBA8888)
    r_total = g_total = b_total = count = 0
    for y in range(image.height()):
        for x in range (image.width()):
            pixel = image.pixelColor(x, y)
            if pixel.alpha() < 32:
                continue
            r_total += pixel.red()
            g_total += pixel.green()
            b_total += pixel.blue()
            count += 1
    if count == 0:
        return None
    return (r_total // count, g_total // count, b_total // count)

def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))

def closest_theme_color(rgb: tuple[int, int, int], colors: dict[str, str]) -> str | None:
    best_hex, best_dist = None, None
    for hex_value in colors.values():
        cr, cg, cb = hex_to_rgb(hex_value)
        dist = (rgb[0] - cr) ** 2 + (rgb[1] - cg) ** 2 + (rgb[2] - cb) ** 2
        if best_dist is None or dist < best_dist:
            best_dist, best_hex = dist, hex_value
    return best_hex

def compute_tile_color(icon_name: str, colors: dict[str, str], fallback: str | None = None) -> str | None:
    image = resolve_icon_image(icon_name)
    if image is None:
        return fallback
    rgb = average_color(image)
    if rgb is None:
        return fallback
    return closest_theme_color(rgb, colors) or fallback
