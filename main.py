from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import models  # import để model được "đăng ký" vào Base trước khi create_all
from app.core.response import build_response
from app.db.base import Base
from app.db.session import engine
from app.models.task_comment import TaskComment

app = FastAPI(title="Campaign Management API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    if hasattr(exc, "status_code"):
        return JSONResponse(
            status_code=exc.status_code,
            content=build_response(
                exc.status_code, str(exc.detail), error=str(exc.detail), path=request.url.path
            ),
            headers=getattr(exc, "headers", None),   # giữ WWW-Authenticate
        )
    return JSONResponse(
        status_code=500,
        content=build_response(500, "Lỗi máy chủ nội bộ", error="Internal Server Error", path=request.url.path),
    )

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=build_response(422, "Dữ liệu không hợp lệ", error=exc.errors(), path=request.url.path),
    )


Base.metadata.create_all(bind=engine)
from app.routers import auth, users, campaigns, campaign_tasks
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(campaigns.router)
app.include_router(campaign_tasks.router)
