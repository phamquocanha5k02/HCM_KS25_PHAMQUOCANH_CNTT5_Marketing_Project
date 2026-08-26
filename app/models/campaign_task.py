from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func

from app.db.base import Base


class CampaignTask(Base):
    __tablename__ = "campaign_tasks"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    campaign_id: Mapped[int] = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    assignee_id: Mapped[int | None] = Column(Integer, ForeignKey("users.id"), nullable=True)
    title: Mapped[str] = Column(String(200), nullable=False)
    description: Mapped[str] = Column(Text, nullable=True)
    status: Mapped[str] = Column(String(20), nullable=False, default="TODO")  # TODO / IN_PROGRESS / DONE
    priority: Mapped[str] = Column(String(20), nullable=False, default="MEDIUM")  # LOW / MEDIUM / HIGH
    due_date: Mapped[DateTime] = Column(DateTime, nullable=True)  # hạn xử lý (DATETIME theo bảng chuẩn)
    created_at: Mapped[DateTime] = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationship với Campaign
    campaign = relationship("Campaign", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys="CampaignTask.assignee_id")
    comments = relationship("TaskComment", back_populates="task", cascade="all, delete-orphan")
    # Quyền sửa/xoá task dựa vào: OWNER của campaign (campaigns.owner_id) hoặc assignee của task
