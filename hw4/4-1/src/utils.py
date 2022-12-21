from pathlib import Path

from .model import UserLogin

DATA_DIR = Path.home() / "hw4" / "4-1" / "data"


def get_user(username: str) -> UserLogin | None:
    with (DATA_DIR / "users").open("r") as file:
        for line in file:
            name, password = line.strip().split()
            if name == username:
                return UserLogin(username=name, password=password)

    return None


def get_secret() -> str:
    with (DATA_DIR / "secret").open("r") as file:
        return file.readline().strip()
