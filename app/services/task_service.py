from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from typing import Optional
from app.models.campaign_task import CampaignTask
from app.models.campaign import Campaign
from app.models.campaign_member import CampaignMember
from app.models.task_comment import TaskComment
from app.schemas.campaign_task import CampaignTaskCreate, CampaignTaskUpdate
from app.services.membership_helper import require_member, require_owner

def _get_task(db: Session, task_id: int) -> CampaignTask:
    task = db.get(CampaignTask, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Dau viec khong ton tai")
    return task

def _can_management_task(db: Session, task : CampaignTask, user_id: int) -> bool:
    campaign = db.get(Campaign, task.campaign_id)
    if campaign.owner_id == user_id: #Onwer lam duoc moi thu
        return True
    if task.assignee_id == user_id: # assignee sửa task của mình
        return True
    return False

def create_task(db: Session, campaign_id: int, payload: CampaignTaskCreate, user_id: int) -> CampaignTask:
    require_member(db, campaign_id, user_id)
    if payload.assignee_id is not None:
        _validate_assignee(db, campaign_id, payload.assignee_id)
    task = CampaignTask(campaign_id = campaign_id, **payload.model_dump(exclude_unset=True))
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def _validate_assignee(db: Session, campaign_id: int, assignee_id: int) -> None:
    #Gán việc chỉ cho user TRONG chiến dịch — ngoài → 400
    if db.get(CampaignMember, (assignee_id, campaign_id)) is None:
        raise HTTPException(
            status_code=400,
            detail="Nguoi duoc giao viec khong thuoc chien dich"
        )
        
def list_tasks(db: Session, campaign_id: int, user_id: int,
                search: Optional[str] = None,
                status: Optional[str] = None,
                priority: Optional[str] = None,
                assignee_id: Optional[int] = None,
                limit: int = 10, offset: int = 0,
                sort: str = "-created_at"):
    #Chỉ thành viên mới thấy task của chiến dịch; không lộ task chiến dịch khác
    require_member(db, campaign_id, user_id) # chan tu dau
    query = db.query(CampaignTask).filter(CampaignTask.campaign_id == campaign_id)
    
    if search:
        query = query.filter(CampaignTask.title.contains(search))
    if status:
        query = query.filter(CampaignTask.status == status)
    if priority:
        query = query.filter(CampaignTask.priority == priority)
    if assignee_id:
        query = query.filter(CampaignTask.assignee_id == assignee_id)
    
    # sort: "-created_at" = giảm dần, "due_date" = tăng dần
    # ⚠️ WHITELIST các cột được phép sort — tránh AttributeError -> 500
    ALLOWED_SORT = {"created_at", "due_date", "title", "priority", "status"}
    sort_key = sort.lstrip("-")
    if sort_key not in ALLOWED_SORT:
        raise HTTPException(
            status_code=400,
            detail="Truong sort khong hop le"
        )
    col = getattr(CampaignTask, sort_key)
    query = query.order_by(col.desc() if sort.startswith("-") else col.asc())
    
    return query.offset(offset).limit(limit).all() # phan trang

def get_task(db: Session, task_id, user_id) -> CampaignTask:
    task = _get_task(db, task_id)
    require_member(db, task.campaign_id, user_id)
    return task

def update_task(db: Session, task_id: int, payload: CampaignTaskUpdate, user_id: int) -> CampaignTask:
    task = _get_task(db, task_id)
    require_member(db, task.campaign_id, user_id)
    if not _can_management_task(db, task, user_id):
        raise HTTPException(
            status_code = 403,
            detail = "Ban khong co quyen cap nhat dau viec nay"
            )
    if payload.assignee_id is not None:
        _validate_assignee(db, task.campaign_id, payload.assignee_id)
        
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, user_id: int) -> None:
    task = _get_task(db, task_id)
    require_member(db, task.campaign_id, user_id)
    if not _can_management_task(db, task, user_id):   # OWNER hoặc assignee
        raise HTTPException(status_code=403, detail="Bạn không có quyền xoá đầu việc này")
    db.delete(task)
    db.commit()
    
# ---- Comment ----

def add_comment(db: Session, task_id: int, user_id: int, content: str):
    task = _get_task(db, task_id)
    require_member(db, task.campaign_id, user_id)
    comment = TaskComment(task_id = task_id, user_id = user_id, content = content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

def list_comment(db: Session, task_id: int, user_id: int):
    task = _get_task(db, task_id)
    require_member(db, task.campaign_id, user_id)
    return (
        db.query(TaskComment)
        .filter(TaskComment.task_id == task_id).
        order_by(TaskComment.created_at.desc())
        .all()
        )
