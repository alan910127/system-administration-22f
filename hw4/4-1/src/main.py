from pathlib import Path

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import FileResponse, PlainTextResponse

from . import auth, utils
from .model import UserLogin

app = FastAPI()


@app.get("/public/{filename}", response_class=FileResponse)
async def read_public_file(filename: str):
    realpath = Path.home() / "hw4" / "4-1" / "data" / "static" / "public" / filename

    print(f"{realpath=}")

    if not realpath.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return realpath


@app.get("/{directory}/{filename}", response_class=FileResponse)
async def read_file(
    directory: str, filename: str, username: str = Depends(auth.get_current_user)
):
    realpath = Path.home() / "hw4" / "4-1" / "data" / "static" / directory / filename

    print(f"{realpath=}")

    if directory != username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    if not realpath.exists():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return realpath


@app.post("/login", response_class=PlainTextResponse)
async def login(req: Request):
    content_type = req.headers.get("Content-Type", "")
    if content_type.startswith("application/json"):
        user = UserLogin(**await req.json())
    elif content_type.startswith("application/x-www-form-urlencoded"):
        user = UserLogin(**await req.form())  # type: ignore
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    db_user = utils.get_user(user.username)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if not auth.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return auth.jwt_encode(user.username)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
