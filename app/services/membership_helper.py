from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campaign_member import CampaignMember
from app.models.campaign import Campaign

def get_membership(db: Session, campaign_id: int, user_id: int) -> CampaignMember | None:
    """Trả dòng member (có role) hoặc None nếu user không thuộc campaign."""
    # ⭐ PK của campaign_members là CẶP (user_id, campaign_id).
    # Truyền dict theo TÊN cột → không bị nhầm thứ tự tuple.
    return db.get(CampaignMember, {"campaign_id": campaign_id, "user_id": user_id})

def require_member(db: Session, campaign_id: int, user_id: int) -> CampaignMember:
    """User phải là thành viên, nếu không → 403."""
    member = get_membership(db, campaign_id, user_id)
    if member is None:
        raise HTTPException(
            status_code=403,
            detail="Ban khong thuoc chien dich nay"
        )
    return member

def require_owner(db: Session, campaign: Campaign, user_id: int) -> CampaignMember:
    """User phải là OWNER (theo campaigns.owner_id), nếu không → 403."""
    require_member(db, campaign.id, user_id)      # câu 1: phải là thành viên
    if campaign.owner_id != user_id:              # câu 2: phải là owner ⭐ (dùng instance)
        raise HTTPException(
            status_code=403,
            detail="Chi owner moi duoc thuc hien"
        )
    return get_membership(db, campaign.id, user_id)
