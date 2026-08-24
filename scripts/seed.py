"""Nạp dữ liệu mẫu vào MySQL. Chạy: python scripts/seed.py"""

import sys
from pathlib import Path

import bcrypt

# Để import được package `app` khi chạy trực tiếp từ scripts/
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from sqlalchemy import select

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.campaign_task import CampaignTask
from app.models.users import User


USERS = [
    {
        "email": "owner@example.com",
        "full_name": "Campaign Owner",
        "role": "ADMIN",  # USER / ADMIN
        "password": "Owner123!",
    },
    {
        "email": "member@example.com",
        "full_name": "Campaign Member",
        "role": "USER",
        "password": "Member123!",
    },
]


def password_hash(password: str) -> str:
    # bcrypt cần bytes; không bao giờ lưu password thật
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def get_or_create_user(db, data: dict) -> User:
    """Tìm user theo email; chưa có thì tạo mới (chống trùng khi chạy lại)."""
    user = db.scalar(select(User).where(User.email == data["email"]))
    if user is None:
        user = User(
            email=data["email"],
            full_name=data["full_name"],
            role=data["role"],
            password_hash=password_hash(data["password"]),
            is_active=True,
        )
        db.add(user)
        db.flush()  # lấy user.id cho bước sau
    return user


def seed() -> None:
    Base.metadata.create_all(engine)  # tạo bảng nếu chưa có

    with SessionLocal.begin() as db:  # tự commit/rollback
        owner = get_or_create_user(db, USERS[0])
        member = get_or_create_user(db, USERS[1])

        campaign = db.scalar(
            select(Campaign).where(
                Campaign.name == "Sample Marketing Campaign",
                Campaign.owner_id == owner.id,
            )
        )
        if campaign is None:
            campaign = Campaign(
                name="Sample Marketing Campaign",
                description="Campaign created by the seed script.",
                owner_id=owner.id,
            )
            db.add(campaign)
            db.flush()  # lấy campaign.id cho bước dưới

        membership = db.get(
            CampaignMember,
            {"user_id": member.id, "campaign_id": campaign.id},  # PK là cặp (user_id, campaign_id)
        )
        if membership is None:
            db.add(
                CampaignMember(
                    user_id=member.id,
                    campaign_id=campaign.id,
                    role="MEMBER",  # OWNER / MEMBER
                )
            )

        tasks = [
            ("Prepare campaign brief", "TODO", "MEDIUM", owner.id),
            ("Review launch content", "IN_PROGRESS", "HIGH", member.id),
        ]
        for title, status, priority, assignee_id in tasks:
            task_exists = db.scalar(
                select(CampaignTask).where(
                    CampaignTask.campaign_id == campaign.id,
                    CampaignTask.title == title,
                )
            )
            if task_exists is None:
                db.add(
                    CampaignTask(
                        campaign_id=campaign.id,
                        assignee_id=assignee_id,
                        title=title,
                        description=f"Sample task: {title}.",
                        status=status,
                        priority=priority,
                    )
                )

    print("Seed completed successfully.")


if __name__ == "__main__":
    seed()
