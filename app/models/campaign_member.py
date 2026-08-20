#BANG TRUNG GIANG CUA CAMPAIGN VA USERS

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class CampaignMember(Base):
    __tablename__ = "campaign_members"
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), primary_key=True)
    campaign_id: Mapped[int] = mapped_column(Integer, ForeignKey("campaigns.id"), primary_key=True)
    role: Mapped[str] = mapped_column(String(50), nullable=False, default="member") # vai tro cua user trong campaign owner/member 
    joined_at: Mapped[DateTime] = mapped_column(DateTime , server_default=func.now(), nullable=False)
    
    # Quan he voi bang User va Campaign
    campaign = relationship("Campaign", back_populates="members") # 1 campaign có nhiều member
    user = relationship("User", back_populates="memberships") # 1 user có nhieu campaign
    
    #Khóa chính là cặp (campaign_id, user_id)** → DB tự chặn thêm trùng member (IntegrityError