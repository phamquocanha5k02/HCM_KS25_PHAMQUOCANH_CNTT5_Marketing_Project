from os import path

from fastapi import APIRouter, Depends, HTTPException, Request, Body
from fastapi.routing import APIRoute
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.schemas.user import UserRegister, UserOut
from app.services import auth_service
from app.db.session import get_db
from app.core.response import build_response

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", status_code=201, summary="Dang ky tai khoang")
def register(payload: UserRegister, request: Request, db : Session = Depends(get_db)):
    user = auth_service.register(db, payload)
    return build_response(
        201,
        "Dang ky thanh cong",
        UserOut.model_validate,
        path=request.url.path
        )
@router.post("/login", summary="Dang nhap va nhan JWT")
def login(
    form : OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db)
    ):
    data =  auth_service.login(db,form.username, form.password)
    
    return build_response(200, "Dang nhap thanh cong", data, path = request.url.path)

@router.post("/refresh", summary="Cap lai access token ")
def refresh(request: Request = None, payload: dict = Body(...), db: Session = Depends(get_db)):
    data = auth_service.refresh_access_token(db, payload.get("refresh_token", ""))
    return build_response(200, "Cap token moi thanh cong", data, path=request.url.path)