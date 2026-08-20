from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql import func
from app.db.database import Base

class CampaignTask(Base):
    __tablename__ = "campaign_tasks"
    
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    campaign_id: Mapped[int] = Column(Integer, ForeignKey("campaigns.id"), nullable=False)
    title: Mapped[str] = Column(String(255), nullable=False)
    description: Mapped[str] = Column(Text, nullable=True)
    status: Mapped[str] = Column(String(50), nullable=False, default="pending")  # pending, in_progress, completed
    created_at: Mapped[DateTime] = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationship with Campaign
    campaign = relationship("Campaign", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks", foreign_keys="CampaignTask.assignee_id")  # Relationship with User (assignee)
    #KHÔNG có cột `created_by`** — bảng chuẩn không có. 
    # Quyền sửa/xoá task dựa vào: **OWNER của campaign** (`campaigns.owner_id`) hoặcassignee của task