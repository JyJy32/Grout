from pathlib import Path
from xdg.DesktopEntry import DesktopEntry
from xdg.BaseDirectory import xdg_data_dirs


def get_desktop_entries() -> list[dict[str, str]]:
    apps = []
    seen = set()
    search_dirs = [Path(d) / "applications" for d in xdg_data_dirs]
    search_dirs.append(Path.home() / ".local/share/applications")

    for dir in search_dirs:
        if not dir.is_dir():
            continue
        for d_file in dir.glob("*.desktop"):
            if d_file.name in seen:
                continue
            seen.add(d_file.name)
            try:
                entry = DesktopEntry(str(d_file))
            except Exception:
                continue

            if entry.getNoDisplay() or entry.getHidden():
                continue
            if entry.getType() != "Application":
                continue
            apps.append({
                "name": entry.getName(),
                "exec": entry.getExec(),
                "icon": entry.getIcon(),
                "comment": entry.getComment(),
            })
    apps.sort(key=lambda a: a["name"].lower())
    return apps
