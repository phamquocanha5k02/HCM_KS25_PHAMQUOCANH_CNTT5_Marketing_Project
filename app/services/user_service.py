from typing import Optional

from sqlalchemy.orm import Session

from app.models.users import User


def list_users(
    db: Session,
    search: Optional[str] = None,
    is_active: Optional[bool] = None,
) -> list[User]:
    """Danh sách user — logic nghiệp vụ nằm ở service, router chỉ gọi."""
    query = db.query(User)
    if search:
        query = query.filter(
            User.email.contains(search) | User.full_name.contains(search)
        )
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()
