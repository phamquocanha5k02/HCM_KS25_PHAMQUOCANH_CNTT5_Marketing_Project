from app.db.database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text, func
from sqlalchemy.orm import relationship, Mapped, mapped_column
class Campaign(Base):
    __tablename__ = "campaigns"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[Text] = mapped_column(Text, nullable=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False) # lay id tu bang users lam khoa ngoai
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    owner = relationship("User", back_populates="owned_campaigns") # 1 campaign có 1 owner
    members = relationship("CampaignMember", back_populates="campaign") # 1 campaign có nhiều member
    tasks = relationship("CampaignTask", back_populates="campaign") # 1 campaign có nhiều task