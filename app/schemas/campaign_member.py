from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CampaignMemberBase(BaseModel):
    user_id: int
    campaign_id: int
    role: str = Field(default="MEMBER", max_length=50)  # OWNER / MEMBER (trong campaign)


class CampaignMemberCreate(CampaignMemberBase):
    pass


class CampaignMemberUpdate(BaseModel):
    role: str | None = Field(default=None, max_length=50)


class CampaignMemberResponse(CampaignMemberBase):
    model_config = ConfigDict(from_attributes=True)

    joined_at: datetime
