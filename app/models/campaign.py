from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)  # nguồn sự thật OWNER
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="owned_campaigns")  # 1 campaign có 1 owner
    members = relationship(
        "CampaignMember",
        back_populates="campaign",
        cascade="all, delete-orphan",
    )  # xóa campaign → xóa luôn member trong bảng trung gian
    tasks = relationship("CampaignTask", back_populates="campaign")  # 1 campaign có nhiều task
