import shutil
import time

import uvicorn
from fastapi import FastAPI

app = FastAPI()

start_time: float = 0


@app.on_event("startup")
async def handle_startup():
    global start_time
    start_time = time.time()


@app.get("/")
async def health_check():
    total, _, free = shutil.disk_usage("/")
    current_time = time.time()
    return {
        "disk": free / total,
        "uptime": int(current_time - start_time),
        "time": int(current_time),
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
