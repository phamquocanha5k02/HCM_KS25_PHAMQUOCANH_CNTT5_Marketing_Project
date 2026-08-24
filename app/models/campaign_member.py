# BẢNG TRUNG GIAN CỦA CAMPAIGN VÀ USERS (quan hệ N-N)

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class CampaignMember(Base):
    __tablename__ = "campaign_members"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaigns.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="MEMBER")  # OWNER / MEMBER (trong campaign)
    joined_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    # Quan hệ với bảng User và Campaign
    campaign = relationship("Campaign", back_populates="members")
    user = relationship("User", back_populates="memberships")

    # Khóa chính là cặp (campaign_id, user_id) → DB tự chặn thêm trùng member (IntegrityError)
