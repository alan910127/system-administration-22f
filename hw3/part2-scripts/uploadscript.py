#!/usr/bin/env python3

import os
import socket
import sys
from datetime import datetime
from pathlib import Path
from typing import Sequence

HOME_DIR = Path("/") / "home" / "ftp"
HIDDEN_DIR = HOME_DIR / "hidden"
VIOFILE_DIR = HIDDEN_DIR / ".exe"
LOG_FILE = HOME_DIR / "public" / "pureftpd.viofile"


def main(args: Sequence[str]):
    filename = args[1]
    file = Path(filename)

    if file.suffix != ".exe":
        return

    timestamp = f"{datetime.now():%b %d %H:%M:%S}"
    hostname = socket.gethostname()
    author = os.getenv("UPLOAD_VUSER", "")

    with LOG_FILE.open("a+") as log_file:
        print(
            f"{timestamp} {hostname} ftpuscr[{os.getpid()}]: "
            f"{filename} violate file detected. Uploaded by {author}.",
            file=log_file,
        )

    file.rename(VIOFILE_DIR / file.name)


if __name__ == "__main__":
    main(sys.argv)
