from datetime import datetime, timedelta, timezone
from typing import Optional
import bcrypt
import jwt

from app.core.config import settings

# ---- bcrypt (hash mật khẩu) ----
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# ---- JWT (tạo + giải mã token) ----
def create_access_token(data: dict) -> str:
    payload = data.copy()
    payload["type"] = "access"
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

# ----- Token sống lâu hơn, dùng để cấp lại access token khi hết hạn -------
def create_refresh_token(user_id : int) -> str:
    payload = {"sub": str(user_id), "type": "refresh"}
    payload["exp"] = datetime.now(timezone.utc) + timedelta(
        days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


# Sai chu ky hoac het han tu raise jwt.PyJWTError
def decode_token(token: str) -> dict:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


