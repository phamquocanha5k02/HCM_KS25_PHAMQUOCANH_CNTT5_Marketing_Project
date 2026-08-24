from sqlalchemy import Boolean, Column, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)  # KHÔNG lưu password thật
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="USER")  # USER / ADMIN (toàn hệ thống)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    memberships = relationship("CampaignMember", back_populates="user")  # 1 user có thể tham gia nhiều campaign
    assigned_tasks = relationship("CampaignTask", back_populates="assignee", foreign_keys="CampaignTask.assignee_id")
    owned_campaigns = relationship("Campaign", back_populates="owner", foreign_keys="Campaign.owner_id")
