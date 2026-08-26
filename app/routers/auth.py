from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserOut
from app.services import auth_service
from app.db.get_db import get_db
from app.core.response import build_response

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=201, summary="Đăng ký tài khoản",
             description="Tạo tài khoản mới. Role luôn mặc định USER (không cho client tự chọn ADMIN). Password từ 6-72 ký tự.")
def register(payload: UserRegister, request: Request, db : Session = Depends(get_db)):
    user = auth_service.register(db, payload)
    return build_response(
        201,
        "Đăng ký thành công",
        UserOut.model_validate(user),
        path=request.url.path
        )
@router.post("/login", summary="Đăng nhập để nhận JWT token",
             description="Xác thực username (email) + password → trả access_token + refresh_token theo chuẩn OAuth2. Endpoint này là tokenUrl của nút Authorize trong Swagger.")
def login(
    form : OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):
    data =  auth_service.login(db,form.username, form.password)

    # ⚠️ KHÔNG bọc build_response: /login là tokenUrl chuẩn OAuth2.
    # Swagger Authorize đòi access_token ở CẤP CAO NHẤT của JSON.
    return data

@router.post("/refresh", summary="Cấp lại access token",
             description="Dùng refresh_token để nhận access_token mới khi access token cũ hết hạn (không cần đăng nhập lại).")
def refresh(request: Request, payload: dict = Body(...), db: Session = Depends(get_db)):
    data = auth_service.refresh_access_token(db, payload.get("refresh_token", ""))
    return build_response(200, "Cấp access token mới thành công", data, path=request.url.path)