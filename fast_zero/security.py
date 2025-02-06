from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from pwdlib import PasswordHash
from jwt import encode as jwt_encode

pwd_context = PasswordHash.recommended()

SECRET_KEY = "f9e3b1b3f1d2f3e"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt_encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
