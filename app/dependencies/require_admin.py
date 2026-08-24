from fastapi import Depends, HTTPException
from app.models.users import User
from app.dependencies.get_current_user import get_current_user

def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Ban khong co quyen quan tri vien"
        )
    return current_user