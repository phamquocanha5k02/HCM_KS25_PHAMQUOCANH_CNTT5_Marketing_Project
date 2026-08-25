# Router cho Campaign Task — Ngày 4: CRUD task, assignee trong chiến dịch, workflow, filter/sort/pagination, permission OWNER/assignee
from typing import Optional
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.core.response import build_response
from app.db.get_db import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.users import User
from app.schemas.task_comments import CommentCreate
from app.schemas.campaign_task import (
    CampaignTaskCreate,
    CampaignTaskResponse,
    CampaignTaskUpdate,
)
from app.services import task_service

router = APIRouter(tags=["campaign-tasks"])


@router.post("/api/campaigns/{campaign_id}/campaign-tasks", status_code=201,
            summary="Tạo đầu việc chiến dịch")
def create_task(campaign_id: int, payload: CampaignTaskCreate, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = task_service.create_task(db, campaign_id, payload, current_user.id)
    return build_response(201, "Tạo đầu việc thành công",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.get("/api/campaigns/{campaign_id}/campaign-tasks",
            summary="List/filter/search đầu việc")
def list_tasks(campaign_id: int,
            search: Optional[str] = None,
            status: Optional[str] = None,
            priority: Optional[str] = None,
            assignee_id: Optional[int] = None,
            limit: int = 10, offset: int = 0,
            sort: str = "-created_at",
            request: Request = None,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    tasks = task_service.list_tasks(db, campaign_id, current_user.id,
                                    search, status, priority, assignee_id,
                                    limit, offset, sort)
    return build_response(200, "Danh sách đầu việc",
                        [CampaignTaskResponse.model_validate(task) for task in tasks],
                        path=request.url.path)


@router.get("/api/campaign-tasks/{task_id}", summary="Chi tiết đầu việc")
def get_task(task_id: int, request: Request,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    task = task_service.get_task(db, task_id, current_user.id)
    return build_response(200, "Chi tiết đầu việc",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.patch("/api/campaign-tasks/{task_id}",
            summary="Cập nhật đầu việc (OWNER hoặc assignee)")
def update_task(task_id: int, payload: CampaignTaskUpdate, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = task_service.update_task(db, task_id, payload, current_user.id)
    return build_response(200, "Cập nhật đầu việc thành công",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.delete("/api/campaign-tasks/{task_id}",
            summary="Xóa đầu việc (OWNER hoặc assignee)")
def delete_task(task_id: int, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task_service.delete_task(db, task_id, current_user.id)
    return build_response(200, "Xoá đầu việc thành công", path=request.url.path)

#---- Comment ----
@router.post("/api/campaign-tasks/{task_id}/comments", status_code=201, summary="Them comments")
def add_comment(task_id: int,
                payload: CommentCreate,
                request: Request = None,
                db: Session = Depends(get_db),
                current_user : User = Depends(get_current_user)):
    comment = task_service.add_comment(db, task_id, current_user.id, payload.content)
    return build_response(
        201,
        "Them comment thanh cong",
        path = request.url.path
    )