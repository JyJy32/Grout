import os
import subprocess
from PySide6.QtCore import QObject, Slot

class SystemActions(QObject):
    @Slot()
    def logout(self):
        session_id = os.environ.get("XDG_SESSION_ID")
        try:
            if session_id:
                subprocess.Popen(["loginctl", "terminate-session", session_id])
            else:
                subprocess.Popen(["openbox", "--exit"])
        except FileNotFoundError:
            print("grout: logout failed - loginctl not found")

    @Slot()
    def shutdown(self):
        try:
            subprocess.Popen(["systemctl", "poweroff"])
        except FileNotFoundError:
            print("grout: shutdown failed - systemctl not found")
