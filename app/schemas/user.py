from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr
    full_name: str = Field(min_length=2, max_length=100)


class UserRegister(UserBase):
    password: str = Field(min_length=6, max_length=72)  # 72 = giới hạn bcrypt
    # KHÔNG có role/is_active → role mặc định "USER", chống leo thang đặc quyền


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, min_length=2, max_length=100)
    password: str | None = Field(default=None, min_length=6, max_length=72)


class UserOut(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    role: str
    is_active: bool
    created_at: datetime
    # KHÔNG có password_hash → không bao giờ lộ ra response
