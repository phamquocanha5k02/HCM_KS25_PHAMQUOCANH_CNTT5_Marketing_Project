
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.campaign_member import CampaignMember
from app.models.campaign import Campaign

def get_membership(db: Session, campaign_id : int, user_id: int) -> CampaignMember | None:
    # Trả dòng member (có role) hoặc None nếu user không thuộc campaign
    return db.get(CampaignMember, (campaign_id, user_id))

def require_member(db: Session, campaign_id: int, user_id: int) -> CampaignMember:
    # User phai la thanh vien neu ko thi tra ve 403
    member = get_membership(db, campaign_id, user_id)
    if member is None:
        raise HTTPException(
            status_code=403,
            detail="Ban khong thuoc chien dich nay"
        )
    return member

def require_owner(db: Session, campaign_id: int, user_id: int) -> CampaignMember:
    # User phai la owner
    require_member(db, campaign_id, user_id) # phai la thanh vien cua chien dich
    if Campaign.owner_id != user_id:
        raise HTTPException(
            403,
            detail= "Chi owner moi duoc thuc hien"
        )
    return get_membership(db, Campaign.id, user_id)