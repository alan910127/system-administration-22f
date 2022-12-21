from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBasic, OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from . import utils

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
basic_auth_scheme = HTTPBasic()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(password: str, hash: str) -> bool:
    return pwd_ctx.verify(password, hash)


def jwt_encode(username: str):
    return jwt.encode({"user": username}, key=utils.get_secret(), algorithm="HS256")


def jwt_decode(token: str):
    try:
        payload = jwt.decode(token, key=utils.get_secret(), algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return payload


async def get_current_user(req: Request):
    authorization = req.headers.get("Authorization", "")
    if authorization.lower().startswith("basic"):
        credential = await basic_auth_scheme(req)
        print(f"{credential=}")
        if not credential:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

        username = credential.username
        password = credential.password

        user = utils.get_user(username)

        if user is None or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    elif authorization.lower().startswith("bearer"):
        token = await oauth2_scheme(req)

        if token is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

        credential = jwt_decode(token)
        username = credential["user"]
    else:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

    return username
