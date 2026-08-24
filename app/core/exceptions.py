from fastapi import HTTPException


def not_found(detail: str = "Không tìm thấy") -> HTTPException:
    return HTTPException(status_code=404, detail=detail)


def bad_request(detail: str = "Yêu cầu không hợp lệ") -> HTTPException:
    return HTTPException(status_code=400, detail=detail)


def forbidden(detail: str = "Bạn không có quyền") -> HTTPException:
    return HTTPException(status_code=403, detail=detail)


def unauthorized(detail: str = "Chưa đăng nhập") -> HTTPException:
    return HTTPException(status_code=401, detail=detail)


def conflict(detail: str = "Dữ liệu đã tồn tại") -> HTTPException:
    return HTTPException(status_code=409, detail=detail)
