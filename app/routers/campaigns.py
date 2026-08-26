from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
from app.schemas.campaign import CampaignCreate, CampaignUpdate, CampaignOut
from app.schemas.user import UserOut
from app.models.users import User
from app.models.campaign_member import CampaignMember
from app.services import campaign_service
from app.db.get_db import get_db
from app.core.response import build_response
from app.dependencies.get_current_user import get_current_user

router = APIRouter(prefix="/api/campaigns", tags=["campaigns"])

class MemberAdd(BaseModel):  # body chuẩn cho thêm member
    user_id: int

@router.post("", status_code=201, summary="Tạo chiến dịch (tự thành OWNER)",
             description="User đăng nhập tạo chiến dịch mới và tự động trở thành OWNER (có dòng trong campaign_members với role=OWNER).")
def create_campaign(
    payload: CampaignCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign = campaign_service.create_campaign(db, payload, current_user.id)
    return build_response(
        201,
        "Tao chien dich thanh cong",
        CampaignOut.model_validate(campaign),
        path=request.url.path
    )

@router.get("", summary="Danh sách chiến dịch của tôi",
            description="Chỉ trả các chiến dịch mà user đang đăng nhập là OWNER hoặc MEMBER. Hỗ trợ ?search= tìm theo tên.")
def list_campaigns(
    request: Request,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaigns = campaign_service.list_campaigns(db, current_user.id, search)
    return build_response(
        200,
        "Danh sach chien dich",
        [CampaignOut.model_validate(c) for c in campaigns],
        path=request.url.path
    )

@router.get("/{campaign_id}", summary="Chi tiết chiến dịch",
            description="Chỉ thành viên (MEMBER/OWNER) của chiến dịch mới xem được chi tiết. Không phải thành viên → 403.")
def get_campaign(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign = campaign_service.get_campaign(db, campaign_id, current_user.id)
    return build_response(
        200,
        "Chi tiet chien dich",
        CampaignOut.model_validate(campaign),
        path=request.url.path
    )

@router.patch("/{campaign_id}", summary="Cập nhật chiến dịch (chỉ OWNER)",
              description="Cập nhật tên/mô tả chiến dịch. Chỉ OWNER mới được sửa (PATCH = chỉ ghi đè trường gửi lên).")
def update_campaign(
    campaign_id: int,
    payload: CampaignUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign = campaign_service.update_campaign(db, campaign_id, payload, current_user.id)
    return build_response(
        200,
        "Cap nhat chien dich thanh cong",
        CampaignOut.model_validate(campaign),
        path=request.url.path
    )

@router.delete("/{campaign_id}", summary="Xóa chiến dịch (chỉ OWNER)",
               description="Xóa chiến dịch. Cascade xóa luôn member + task + comment liên quan (không thể khôi phục).")
def delete_campaign(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign_service.delete_campaign(db, campaign_id, current_user.id)
    return build_response(200, "Xoa chien dich thanh cong", path=request.url.path)

# ---- Member ----

@router.post("/{campaign_id}/members", status_code=201, summary="Thêm thành viên (chỉ OWNER)",
             description="OWNER thêm user vào chiến dịch với role MEMBER. Không cho thêm trùng (chặn ở DB bằng khóa chính kép).")
def add_member(
    campaign_id: int,
    payload: MemberAdd,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign_service.add_member(db, campaign_id, payload.user_id, current_user.id)
    return build_response(
        201,
        "Them thanh vien thanh cong",
        path=request.url.path
    )

@router.get("/{campaign_id}/members", summary="Danh sách thành viên",
            description="Trả danh sách thành viên của chiến dịch kèm role (OWNER/MEMBER) và ngày tham gia. Chỉ thành viên xem được.")
def list_members(
    campaign_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign = campaign_service.get_campaign(db, campaign_id, current_user.id)  # check member
    members = (
        db.query(CampaignMember, User)
        .join(User, User.id == CampaignMember.user_id)
        .filter(CampaignMember.campaign_id == campaign_id)
        .all()
    )
    data = [{
        "user": UserOut.model_validate(u).model_dump(),
        "role": m.role,
        "joined_at": m.joined_at.isoformat()
    } for m, u in members]
    return build_response(200, "Danh sach thanh vien", data, path=request.url.path)

@router.delete("/{campaign_id}/members/{user_id}", summary="Xóa thành viên (chỉ OWNER)",
               description="OWNER xóa member khỏi chiến dịch. KHÔNG được xóa OWNER (chống campaign mồ côi).")
def remove_member(
    campaign_id: int,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    campaign_service.remove_member(db, campaign_id, user_id, current_user.id)
    return build_response(200, "Xoa thanh vien thanh cong", path=request.url.path)
