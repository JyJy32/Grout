import shlex
import subprocess
from PySide6.QtCore import QObject, Slot
_FIELD_CODES = {"%f", "%F", "%u", "%U", "%d", "%D", "%n", "%N", "%i", "%c", "%k", "%v"}

def clean_exec(exec_string: str) -> list[str]:
    try:
        tokens = shlex.split(exec_string)
    except ValueError:
        tokens = exec_string.split()
    return [t for t in tokens if t not in _FIELD_CODES]



class Launcher(QObject):
    @Slot(str, bool)
    def launch(self, exec_string: str, is_terminal: bool = False):
        print(exec_string)
        # TODO: get terminal emulator from config
        if is_terminal:
            exec_string = "alacritty -e " + exec_string
        args = clean_exec(exec_string)
        print(f"grout launching app: {args}")
        if not args:
            return
        try:
            subprocess.Popen(
                args,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            print(f"grout: failed to launch, command not found: {args}")
