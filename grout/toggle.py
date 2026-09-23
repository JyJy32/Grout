#!/usr/bin/env python
import os
import socket
import sys
from pathlib import Path

def main():
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR", "/tmp")
    socket_path = Path(runtime_dir) / "grout.sock"

    if not socket_path.exists():
        print("grout daemon is not running", file=sys.stderr)
        sys.exit(1)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(str(socket_path))
    sock.send(b"toggle")
    sock.close()

if __name__ == "__main__":
    main()
