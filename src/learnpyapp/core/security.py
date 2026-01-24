from datetime import datetime, timedelta
from typing import Any, cast

from jose import jwt
from passlib.context import CryptContext

SECRET_KEY = "super-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    hashed = pwd_context.hash(password)
    return cast(str, hashed)


def verify_password(plain: str, hashed: str) -> bool:
    result = pwd_context.verify(plain, hashed)
    return cast(bool, result)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return cast(str, token)
