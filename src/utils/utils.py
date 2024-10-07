# контекст для хеширования паролей
from datetime import datetime, timedelta, timezone
from fastapi import Request, HTTPException, status
import jwt
from passlib.context import CryptContext

from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# получение хешированного пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# проверка хешированного пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        payload=to_encode,
        key=settings.get_auth_data()["secret_key"],
        algorithm=settings.get_auth_data()["algorithm"],
    )
    return encoded_jwt


def get_token_from_cookies(request: Request) -> str:
    token = request.cookies.get("users_access_token")
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен не найден"
        )
    return token


def decode_token(
    token: str | bytes,
):
    decoded_jwt = jwt.decode(
        token,
        key=settings.get_auth_data()["secret_key"],
        algorithms=settings.get_auth_data()["algorithm"],
    )
    return decoded_jwt
