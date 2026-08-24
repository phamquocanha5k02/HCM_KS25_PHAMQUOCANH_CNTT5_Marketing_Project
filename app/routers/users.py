from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.user import UserOut
from app.models.users import User
from app.db.get_db import get_db
from app.core.response import build_response
from app.dependencies.get_current_user import get_current_user
from app.dependencies.require_admin import require_admin

router = APIRouter(prefix="/api/users", tags=["users"])

@router.get("/me", summary="Xem hồ sơ cá nhân")
def get_me(request: Request = None,
    current_user: User = Depends(get_current_user)):
    return build_response(
        200,
        "Thông tin người dùng",
        UserOut.model_validate(current_user),
        path=request.url.path
        )

@router.get("", summary="Danh sách người dùng (chỉ Admin)")
def list_users(
    request: Request = None,
    search: Optional[str] = None,     # tìm theo tên/email
    is_active: Optional[bool] = None, # lọc trạng thái
    db: Session = Depends(get_db),
    _ : User = Depends(require_admin)):  # chỉ ADMIN
    query = db.query(User)
    if search:
        query = query.filter( User.email.contains(search) | User.full_name.contains(search))
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    users = [UserOut.model_validate(u) for u in query.all()]
    return build_response(
        200,
        "Danh sách người dùng",
        users,
        path=request.url.path
        )