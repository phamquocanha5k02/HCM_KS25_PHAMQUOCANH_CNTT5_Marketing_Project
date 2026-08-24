from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.models import campaign
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignOut
from app.schemas.user import UserOut
from app.models.users import User
from app.models.campaign_member import CampaignMember
from app.services import campaign_service
from app.services.membership_helper import require_owner, require_member
from app.db.session import get_db
from app.core.response import build_response
from app.dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

class MemberAdd(BaseModel):
    user_id : int
    
@router.post("", status_code=201, summary="Tao chien dich (Tu la Owner)")
def create_campaign(
    payload: CampaignCreate,
    request: Request = None,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)):
    
    campaigns = campaign_service.list_campaigns(db, payload, current_user.id)
    return build_response(
        201,
        "Tao chien dich thanh cong",
        CampaignOut.model_validate(campaign),
        path=request.url.path
        )

@router.get("", summary="Danh sach chien dich cua toi")
def list_campaigns(
    request: Request = None, search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user : User = Depends(get_current_user)
                ):
    
    campaigns = campaign_service.list_campaigns(db, current_user.id, search)
    return build_response(
        200,
        "Chi tiet chien dich",
        [CampaignOut.model_validate(campaign) for campaign in campaigns],
        path = request.url.path
    )

@router.get("/{campaign_id}", summary="Cap nhat chien dich (chi owner)")
def update_campaign(campaign_id: int, payload: CampaignUpdate, request: Request = None,
                    db: Session = Depends(get_db),
                    current_user : User = Depends(get_current_user)):
    campaign = campaign_service.update_campaign(db, campaign_id, payload, current_user.id)
    return build_response(
        200, "Chi tiet chien dich", CampaignOut.model_validate(campaign), path = request.url.path
    )
    
@router.delete("/{campaign_id}", summary="Xóa chiến dịch (chỉ OWNER)")
def delete_campaign(campaign_id: int, request: Request = None,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    campaign_service.delete_campaign(db, campaign_id, current_user.id)
    return build_response(200, "Xoá chiến dịch thành công", path=request.url.path)

# ---- Member ----

@router.post("/{campaign_id}/member", status_code = 201, summary="Them thanh vien (Chi owner)")
def add_member(campaign_id : int, payload: MemberAdd, request : Request = None,
               db: Session = Depends(get_db),
               current_user : User = Depends(get_current_user)):
    campaign_service.add_member(db, campaign_id, payload.user_id, current_user.id)
    return build_response(
        200,
        "Them thanh vien thanh cong",
        path = request.url.path
    )
    
@router.get("{camapign_id}/members", summary="Danh sach thanh vien")
def list_member(campaign_id: int, request: Request = None, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    campaign = campaign_service.get_campaign(db, campaign_id, current_user.id) # check member
    members = (
        db.query(CampaignMember, User)
        .join(User, User.id == CampaignMember.user_id)
        .filter(CampaignMember.campaign_id == campaign_id)
        .all()
        )
    data = [{
        "user": UserOut.model_validate(user).model_dump(),
        "role": member.role,
        "joined_at": member.joined_at.isoformat()
        } for member, user in members]
    return build_response(200, "Danh sach thanh vien", data, path = request.url.path)

@router.delete("/{campaign_id}/members/{user_id}", summary="Xoa thanh vien thanh cong (Chi danh cho Owner)")
def remove_member(campaign_id: int, user_id : int, request: Request = None, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    campaign_service.remove_member(db, campaign_id, user_id, current_user.id)
    return build_response(
        200,
        "Xoa thanh vien thanh cong",
        path = request.url.path
    )
    