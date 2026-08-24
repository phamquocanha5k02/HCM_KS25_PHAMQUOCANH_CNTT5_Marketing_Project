import jwt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.users import User
from app.schemas.user import UserRegister
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
    )

def register(db: Session, payload: UserRegister) -> User:
    exist = db.query(User).filter(User.email == payload.email).first()
    if exist:
        raise HTTPException(
            status_code=409,
            detail="Email da duoc dang ki"
        )
    user = User(
        email = payload.email,
        password_hash = hash_password(payload.password),
        full_name = payload.full_name,
        role = "USER" # role mac dinh la user khong cho tu chon la admin
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login(db: Session, email: str, password: str) -> dict:
    user = db.query(User).filter(User.email == email).first()
    
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail = "Email hoac mat khau khong dung" #-> su dung thong bao chung cho sai email hoac mk de tranh do email exists
        )
    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail = "Tai khoan khong hoat dong"
        )
    token = create_access_token({
        "sub": str(user.id),
        "role": str(user.role)
    })
    refresh = create_refresh_token(user.id)
    
    return {
        "access_token": token,
        "refresh_token": refresh,
        "token_type": "bearer"
        }
    
def refresh_access_token(db: Session, refresh_token : str) -> dict:
    # nhận refresh token hợp lệ → trả access token mới
    try:
        payload = decode_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Token khong hop le"
            )
        user_id = int(payload.get("sub"))
    except (jwt.PyJWTError, ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Refresh token sai hoac da het han"
        )
    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Tai khoang khong hoat dong"
            )
    new_access = create_access_token(
            {
            "sub": str(user.id),
            "role": user.role
            }
        )
    return {
        "access_token": new_access,
        "token_type": "bearer"
    }
    #đăng ký role luôn `"USER"` — KHÔNG lấy role từ request. Người dùng tự gửi `{"role": "ADMIN"}` cũng vô dụng vì service ghi đè.