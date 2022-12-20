import subprocess
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI()


def get_disk_free_ratio() -> float:
    disk_info = subprocess.check_output(["df"], encoding="ascii").splitlines()
    root_info = [info for info in disk_info if info.startswith("zroot/ROOT/default")][0]
    zroot_capacity = root_info.split()[4].removesuffix("%")
    return int(zroot_capacity) / 100


@app.get("/")
async def health_check():
    return {
        "disk": get_disk_free_ratio(),
        "uptime": int(time.monotonic()),
        "time": int(time.time()),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
