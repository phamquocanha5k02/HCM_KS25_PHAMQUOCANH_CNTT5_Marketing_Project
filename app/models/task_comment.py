from sqlalchemy import Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped
from sqlalchemy.sql import func
from app.db.base import Base

class TaskComment(Base):
    __tablename__ = "task_comments"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    task_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaign_tasks.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    task = relationship("CampaignTask", back_populates="comments")
    user = relationship("User")
    
    # su dung on delete cascade de dong bo du lieu neu xoa task thi xoa cac comment lien quan
    