from datetime import datetime, timezone
from typing import Any


def build_response(
    status_code: int,
    message: str,
    data: Any = None,
    error: Any = None,
    path: str = "",
) -> dict:
    """Response chuẩn thống nhất cho mọi endpoint (thành công + lỗi)."""
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": error,
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "path": path,
    }
