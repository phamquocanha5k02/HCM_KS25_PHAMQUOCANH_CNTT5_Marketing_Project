from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.users import User
from app.schemas.campaign import CampaignCreate, CampaignUpdate
from app.services.membership_helper import require_owner, require_member, get_membership

def create_campaign(db: Session, payload: CampaignCreate, user_id: int) -> Campaign:
    campaign = Campaign(**payload.model_dump(), owner_id = user_id)
    #gan owner
    db.add(campaign)
    db.flush()
    
    db.add(CampaignMember(campaign_id = campaign.id, user_id = user_id, role = "OWNER"))
    db.commit()
    db.refresh(campaign)
    return campaign

def list_campaigns(db: Session, user_id: int, search: Optional[str] = None):
    # Chỉ trả campaign mà user là owner/member (có dòng trong campaign_members)
    query = (
        db.query(Campaign)
        .join(CampaignMember,CampaignMember.campaign_id == Campaign.id)
        .filter(CampaignMember.user_id == user_id)
        )
    if search:
        query = query.filter(Campaign.name.contains(search))
    return query.all()

def get_campaign(db: Session, campaign_id: int, user_id: int ) -> Campaign:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(
            status_code=404,
            detail="Chien dich khong ton tai"
        )
    require_member(db, campaign_id, user_id) # thanh vien cua chien dich moi xem duoc
    return campaign

def update_campaign(db: Session, campaign_id : int, payload: CampaignUpdate, user_id: int) -> Campaign:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(
            status_code= 404,
            detail = "Chien dich khong ton tai"
        )
    require_owner(db, campaign, user_id) #chi owner moi duoc sua
    for key, value in payload.model_dump(exclude=True).items():
        setattr(campaign, key, value) # ghi de truong gui len path
    db.commit()
    db.refresh(campaign)
    return campaign

def delete_campaign(db: Session, campaign_id : int, user_id: int) -> None:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(
            status_code = 404,
            detail="Chien dich khong ton tai"
        )
    require_owner(db, campaign, user_id) # chi owner moi co quyen xoa
    db.delete(campaign) # cascade = "all, delete-orphan" xoa luon ca member == On deletecascade
    db.commit()
    
# -------- MEMBER HELPER ----------
def add_member(db: Session, campaign_id : int, user_id: int, actor_id: int) -> None:
    campaign = db.get(Campaign, campaign_id)
    if campaign is None:
        raise HTTPException(
            status_code=404, 
            detail="Chien dich khong ton tai"
        )
    require_owner(db, campaign, actor_id)
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code = 404, 
            detail = "Nguoi dung khong ton tai"
        )
        
    if get_membership(db, campaign_id, user_id):
        raise HTTPException(
            status_code=400,
            detail = "Thanh vien da co trong chien dich"
        )
    db.add(CampaignMember(campaign_id = campaign_id, user_id = user_id, role = "MEMBER"))
    db.commit()
    
    
