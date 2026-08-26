# Router cho Campaign Task — Ngày 4: CRUD task, assignee trong chiến dịch, workflow, filter/sort/pagination, permission OWNER/assignee
from typing import Optional
from uuid import uuid4
from pathlib import Path          # ⚠️ pathlib.Path, KHÔNG phải fastapi.Path!
from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File
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
import os
router = APIRouter(tags=["campaign-tasks"])


@router.post("/api/campaigns/{campaign_id}/campaign-tasks", status_code=201,
            summary="Tạo đầu việc chiến dịch",
            description="Thành viên tạo đầu việc cho chiến dịch. Có thể gán assignee (phải là member trong campaign), status, priority, due_date.")
def create_task(campaign_id: int, payload: CampaignTaskCreate, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = task_service.create_task(db, campaign_id, payload, current_user.id)
    return build_response(201, "Tạo đầu việc thành công",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.get("/api/campaigns/{campaign_id}/campaign-tasks",
            summary="Danh sách / lọc / tìm kiếm đầu việc",
            description="Liệt kê đầu việc của chiến dịch (chỉ member). Hỗ trợ lọc theo status/priority/assignee_id, search title, sort (vd sort=-created_at, due_date) và phân trang limit/offset.")
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


@router.get("/api/campaign-tasks/{task_id}", summary="Chi tiết đầu việc",
            description="Xem chi tiết 1 đầu việc. User phải là thành viên của chiến dịch chứa đầu việc đó, nếu không → 403.")
def get_task(task_id: int, request: Request,
            db: Session = Depends(get_db),
            current_user: User = Depends(get_current_user)):
    task = task_service.get_task(db, task_id, current_user.id)
    return build_response(200, "Chi tiết đầu việc",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.patch("/api/campaign-tasks/{task_id}",
            summary="Cập nhật đầu việc (OWNER hoặc assignee)",
            description="Cập nhật title/description/status/priority/due_date/assignee. Chỉ OWNER của campaign hoặc assignee của đầu việc được sửa (PATCH = chỉ ghi đè trường gửi lên).")
def update_task(task_id: int, payload: CampaignTaskUpdate, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task = task_service.update_task(db, task_id, payload, current_user.id)
    return build_response(200, "Cập nhật đầu việc thành công",
                        CampaignTaskResponse.model_validate(task), path=request.url.path)


@router.delete("/api/campaign-tasks/{task_id}",
            summary="Xóa đầu việc (OWNER hoặc assignee)",
            description="Xóa đầu việc. Cascade xóa luôn các comment của đầu việc đó. Chỉ OWNER của campaign hoặc assignee được xóa.")
def delete_task(task_id: int, request: Request,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    task_service.delete_task(db, task_id, current_user.id)
    return build_response(200, "Xoá đầu việc thành công", path=request.url.path)

#---- Comment ----
@router.post("/api/campaign-tasks/{task_id}/comments", status_code=201, summary="Thêm bình luận",
             description="Thêm bình luận cho đầu việc. Chỉ thành viên của chiến dịch mới bình luận được (403 nếu không phải).")
def add_comment(task_id: int,
                payload: CommentCreate,
                request: Request = None,
                db: Session = Depends(get_db),
                current_user : User = Depends(get_current_user)):
    comment = task_service.add_comment(db, task_id, current_user.id, payload.content)
    return build_response(
        201,
        "Them comment thanh cong",
        {"comment_id": comment.id},
        path = request.url.path
    )


@router.get("/api/campaign-tasks/{task_id}/comments", summary="Danh sách bình luận",
            description="Trả danh sách bình luận của đầu việc (mới nhất trước). Chỉ thành viên của chiến dịch xem được.")
def list_comments(task_id: int,
                request: Request = None,
                db: Session = Depends(get_db),
                current_user : User = Depends(get_current_user)):
    comments = task_service.list_comment(db, task_id, current_user.id)
    data = [
        {"id": c.id, "content": c.content, "user_id": c.user_id,
        "created_at": c.created_at.isoformat()}
        for c in comments
    ]
    return build_response(200, "Danh sach comments", data, path=request.url.path)
    
    
# ---- Upload File ----
ALLOWED_TYPES = {"image/png", "image/jpeg", "application/pdf"}
ALLOWED_EXTS = {".png", ".jpg", ".jpeg", ".pdf"}
MAX_SIZE = 5 * 1024 * 1024   # 5 MB

@router.post("/api/campaign-tasks/{task_id}/attachments",
            status_code=201,
            summary="Upload file đính kèm",
            description="Upload file cho đầu việc (PNG/JPEG/PDF, tối đa 5MB). Kiểm tra loại file (content_type + đuôi) và chống path traversal bằng tên file ngẫu nhiên.")
def upload_attachment(task_id: int,
                    request: Request,
                    file: UploadFile = File(...),
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    task = task_service.get_task(db, task_id, current_user.id)   # check member

    # 1 Kiểm tra loại file: content_type (client khai) + đuôi file (thật sự)
    ext = Path(file.filename or "").suffix.lower()
    if file.content_type not in ALLOWED_TYPES or ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=400, detail="Loại file không được phép")

    # 2 Kiểm tra kích thước — đo thật, không tin file.size
    data = file.file.read()
    if len(data) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="File quá 5MB")

    # 3 Lưu file với tên ngẫu nhiên → chống path traversal + trùng tên
    upload_dir = f"uploads/{task.campaign_id}/{task_id}"
    os.makedirs(upload_dir, exist_ok=True)
    path = f"{upload_dir}/{uuid4().hex}{ext}"
    with open(path, "wb") as f:
        f.write(data)

    return build_response(201,
                        "Upload thành công",
                        {"path": path},
                        path=request.url.path)