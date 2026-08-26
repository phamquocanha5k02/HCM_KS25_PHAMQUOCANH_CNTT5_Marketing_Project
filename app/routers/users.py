from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.user import UserOut
from app.models.users import User
from app.db.get_db import get_db
from app.core.response import build_response
from app.dependencies.get_current_user import get_current_user
from app.dependencies.require_admin import require_admin
from app.services import user_service

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", summary="Xem hồ sơ cá nhân",
            description="Trả thông tin user đang đăng nhập (lấy từ JWT). KHÔNG bao giờ lộ password_hash trong response.")
def get_me(request: Request,
    current_user: User = Depends(get_current_user)):
    return build_response(
        200,
        "Thông tin người dùng",
        UserOut.model_validate(current_user),
        path=request.url.path
        )

@router.get("", summary="Danh sách người dùng (chỉ Admin)",
            description="Chỉ ADMIN mới gọi được. Hỗ trợ search theo tên/email (?search=) và lọc trạng thái (?is_active=true/false).")
def list_users(
    request: Request,
    search: Optional[str] = None,     # tìm theo tên/email
    is_active: Optional[bool] = None, # lọc trạng thái
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin)):  # chỉ ADMIN
    users = user_service.list_users(db, search, is_active)  # logic ở service
    data = [UserOut.model_validate(u) for u in users]
    return build_response(
        200,
        "Danh sách người dùng",
        data,
        path=request.url.path
        )