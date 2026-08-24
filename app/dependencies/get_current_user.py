from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.db.get_db import get_db
from app.models.users import User
import jwt

oauth2_schema = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(
    token : str = Depends(oauth2_schema), # tu lay token tu header Authorization:Bearer
    db: Session = Depends(get_db),
) -> User:
    cred_exc = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Khong the xac thuc thong tin dang nhap",
        headers={"WWW-Authenticate":"Bearer"},
    )
    try:
        payload = decode_token(token) #-> sai/exp -> PyJWTError
        if payload.get("type") != "access":
            raise cred_exc
        user_id  = int(payload.get("sub"))
    except (jwt.PyJWTError, ValueError, TypeError):
        raise cred_exc
    user = db.get(User, user_id)
    if user is None:
        raise cred_exc
    if not user.is_active: # tai khoang bi khoa
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tai khoang cua ban hien tai khong hoat dong"
        )
    return user

    #Luồng lá chắn: lấy token → giải mã (kiểm tra con dấu + hạn + type=access) → tìm user trong DB → kiểm tra `is_active` → trả user. **Sai bất kỳ bước nào → 401** (trừ bị khoá → 403).
    
    