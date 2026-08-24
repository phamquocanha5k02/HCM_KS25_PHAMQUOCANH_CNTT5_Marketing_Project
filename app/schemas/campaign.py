from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class CampaignBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class CampaignCreate(CampaignBase):
    # KHÔNG có owner_id — khi tạo campaign, service tự gán owner_id = user đang đăng nhập
    pass


class CampaignUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None
    # Tất cả optional → partial update (PATCH): chỉ ghi đè trường gửi lên
    # KHÔNG cho sửa owner_id


class CampaignOut(CampaignBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    owner_id: int  # trả kèm để client biết ai là owner
    created_at: datetime
