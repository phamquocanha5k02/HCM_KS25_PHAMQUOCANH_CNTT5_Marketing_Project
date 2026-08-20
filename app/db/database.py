from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy_utils import create_database, database_exists

from app.core.config import settings


BASE_URL = settings.DATABASE_URL # lay du lieu tu file .env tranh hardcode

engine = create_engine(BASE_URL)

SessionLocal = sessionmaker(
    bind = engine,
    autoflush=False,
    autocommit = False,
    expire_on_commit=False
    )
##Mặc định expire_on_commit=True: sau commit(),
# mọi thuộc tính của object bị "expire", 
# truy cập sau đó sẽ phát sinh query mới 
# → lỗi DetachedInstanceError trong nhiều endpoint.
class Base(DeclarativeBase):
    pass
