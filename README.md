# 📢 Marketing Campaign Management API

API quản lý chiến dịch marketing: user, chiến dịch, thành viên, đầu việc (task), comment và file đính kèm.

Xây dựng với **FastAPI + SQLAlchemy 2.0 + MySQL**, theo kiến trúc **3 lớp** (Router → Service → Model).

---

## 🧰 Công nghệ

| Thành phần | Phiên bản |
|---|---|
| Python | 3.10+ (khuyến nghị 3.12/3.14) |
| FastAPI | ≥ 0.115 |
| SQLAlchemy | ≥ 2.0 |
| MySQL | 8.x |
| Auth | JWT (PyJWT) + bcrypt |

## ✅ Tính năng chính

- Đăng ký / Đăng nhập / Refresh token (JWT)
- Phân quyền 2 tầng: **ADMIN/USER** (hệ thống) + **OWNER/MEMBER** (trong campaign)
- CRUD chiến dịch, quản lý thành viên (chống trùng, chống xóa owner)
- CRUD đầu việc: workflow `TODO/IN_PROGRESS/DONE`, priority `LOW/MEDIUM/HIGH`, giao việc chỉ cho member
- Filter / search / sort / phân trang (limit, offset)
- Comment trên đầu việc (chỉ member của campaign)
- Upload file đính kèm (kiểm tra loại + kích thước, chống path traversal)
- Response chuẩn hóa + global exception handler

---

## 🚀 Cài đặt & chạy

### Bước 1 — Tạo database MySQL

```sql
CREATE DATABASE campaign_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Bước 2 — Tạo môi trường ảo và cài dependencies

```bash
cd campaign_management
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Bước 3 — Cấu hình `.env`

```bash
cp .env.example .env
```

Sửa file `.env` cho khớp MySQL của bạn:

```env
# Database
DATABASE_URL=mysql+pymysql://root:mat_khau_cua_ban@localhost:3306/campaign_management_db

# Security
SECRET_KEY=day_la_secret_key_cua_ban
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### Bước 4 — (Tùy chọn) Nạp dữ liệu mẫu

```bash
python scripts/seed.py
```

Tạo 2 tài khoản demo:

| Tài khoản | Mật khẩu | Role |
|---|---|---|
| `owner@example.com` | `Owner123!` | ADMIN |
| `member@example.com` | `Member123!` | USER |

(Kèm 1 campaign mẫu + 2 task mẫu)

### Bước 5 — Chạy server

```bash
uvicorn main:app --reload
```

- Swagger UI: **http://127.0.0.1:8000/docs**
- Health check: **http://127.0.0.1:8000/health**

> ⚠️ Nếu lỗi `address already in use` → đổi port: `uvicorn main:app --port 8000 --reload`

---

## 🔐 Cách dùng Swagger (quan trọng!)

Project dùng `OAuth2PasswordBearer` (OAuth2 **password flow**) — vì vậy:

1. **Không có ô dán token** — đây là bình thường!
2. Bấm nút **Authorize** (góc phải trên) → nhập:
   - `username`: email (ví dụ `owner@example.com`)
   - `password`: mật khẩu
   - `client_secret`: **để TRỐNG**
3. Bấm **Authorize** → khóa 🔒 chuyển thành 🔓
4. Gọi các endpoint bảo vệ → không còn 401

> 💡 Token hết hạn sau **30 phút** — hết hạn chỉ cần Authorize lại (không cần đăng nhập lại).
> 💡 `POST /api/auth/login` trả **đúng chuẩn OAuth2** (`access_token` ở cấp cao nhất) — đừng đổi sang build_response kẻo Authorize hỏng!

---

## 📚 Danh sách endpoint

### Auth
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| POST | `/api/auth/register` | Public | Đăng ký `{email, full_name, password}` |
| POST | `/api/auth/login` | Public | Form `username` + `password` → token |
| POST | `/api/auth/refresh` | Public | Cấp lại access token `{refresh_token}` |

### Users
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| GET | `/api/users/me` | Đăng nhập | Thông tin cá nhân (không lộ password_hash) |
| GET | `/api/users` | **ADMIN** | Danh sách user, `?search=&is_active=` |

### Campaigns
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| POST | `/api/campaigns` | Đăng nhập | Tạo campaign (tự thành OWNER) |
| GET | `/api/campaigns` | Đăng nhập | Campaign của tôi, `?search=` |
| GET | `/api/campaigns/{id}` | Member | Chi tiết campaign |
| PATCH | `/api/campaigns/{id}` | **OWNER** | Sửa campaign |
| DELETE | `/api/campaigns/{id}` | **OWNER** | Xóa (cascade xóa member + task) |

### Campaign Members
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| POST | `/api/campaigns/{id}/members` | **OWNER** | Thêm member `{user_id}` |
| GET | `/api/campaigns/{id}/members` | Member | Danh sách thành viên + role |
| DELETE | `/api/campaigns/{id}/members/{user_id}` | **OWNER** | Xóa member (không xóa được owner) |

### Campaign Tasks
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| POST | `/api/campaigns/{id}/campaign-tasks` | Member | Tạo task |
| GET | `/api/campaigns/{id}/campaign-tasks` | Member | List + filter/search/sort/paginate |
| GET | `/api/campaign-tasks/{id}` | Member | Chi tiết task |
| PATCH | `/api/campaign-tasks/{id}` | **OWNER / assignee** | Sửa task |
| DELETE | `/api/campaign-tasks/{id}` | **OWNER / assignee** | Xóa task (xóa luôn comment) |

### Comments & Attachments
| Method | URL | Quyền | Mô tả |
|---|---|---|---|
| POST | `/api/campaign-tasks/{id}/comments` | Member | Thêm comment `{content}` |
| GET | `/api/campaign-tasks/{id}/comments` | Member | Danh sách comment |
| POST | `/api/campaign-tasks/{id}/attachments` | Member | Upload file (PNG/JPEG/PDF ≤ 5MB) |

**Filter/Sort/Paginate task:**
```
/api/campaigns/{id}/campaign-tasks?search=abc&status=TODO&priority=HIGH&assignee_id=1&sort=-created_at&limit=10&offset=0
```
- `sort`: `created_at`, `due_date`, `title`, `priority`, `status` (thêm `-` = giảm dần)

---

## 📁 Cấu trúc thư mục

```
campaign_management/
├── main.py                  # Khởi động app + exception handlers + create_all
├── requirements.txt
├── .env / .env.example
├── app/
│   ├── routers/             # Đón request, gọi service, trả response
│   │   ├── auth.py  users.py  campaigns.py  campaign_tasks.py
│   ├── services/            # Logic nghiệp vụ + phân quyền
│   │   ├── auth_service.py  user_service.py
│   │   ├── campaign_service.py  task_service.py
│   │   └── membership_helper.py   # require_member / require_owner ⭐
│   ├── models/              # SQLAlchemy models (users, campaigns, ...)
│   ├── schemas/             # Pydantic: Base/Create/Update/Response
│   ├── dependencies/        # get_current_user, require_admin
│   ├── core/                # config, security (bcrypt + JWT), response, exceptions
│   └── db/                  # session.py, get_db.py, base.py
├── scripts/
│   └── seed.py              # Nạp dữ liệu mẫu
└── docs/                    # Tài liệu luồng hoạt động + lý thuyết vấn đáp
```

---

## ⚠️ Lỗi thường gặp

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `"Not authenticated"` (401) | Chưa Authorize trên Swagger hoặc token hết hạn | Bấm Authorize → nhập username/password |
| `"Khong the xac thuc..."` (401) | Token cũ/hỏng lưu trong trình duyệt | Authorize → logout → authorize lại |
| `python-multipart` lỗi | Thiếu package cho upload file | `pip install python-multipart` |
| `address already in use` | Port bị chiếm | Đổi port bằng `--port 8000` |
| Bảng không được tạo khi thêm model mới | Quên import model vào `app/models/__init__.py` | Thêm vào `__init__.py` rồi khởi động lại |
| `create_all` không sửa bảng cũ | Thay đổi cột không tự migrate | Drop bảng cũ hoặc dùng Alembic |

---

## 🧪 Test nhanh (không cần Swagger)

```bash
# 1. Login lấy token
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/auth/login \
  -d "username=owner@example.com&password=Owner123!" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

# 2. Gọi endpoint bảo vệ
curl -s http://127.0.0.1:8000/api/users/me -H "Authorization: Bearer $TOKEN"
```

---

## 📚 Tài liệu thêm

- `docs/luong_hoat_dong.md` — luồng hoạt động chi tiết từng phần
- `docs/ly_thuyet_van_dap.md` — lý thuyết ôn vấn đáp
