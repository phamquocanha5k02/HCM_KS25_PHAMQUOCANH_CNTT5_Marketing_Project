from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Mọi model kế thừa Base này để đăng ký bảng với SQLAlchemy."""
    pass
