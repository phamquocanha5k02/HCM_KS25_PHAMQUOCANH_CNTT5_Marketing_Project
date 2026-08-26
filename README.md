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

---

## 📊 Checklist Tổng Hợp — 37 Kịch Bản (Tick được)

> 📋 Bản Excel tương đương: `CHECKLIST_TEST.xlsx` (có dropdown Pass/Fail).
> ⭐ = kịch bản regression cho các bug đã sửa.

### 🩺 Health
- [ ] **TC-001** Server sống → `200`

### 🔐 Auth
- [ ] **TC-002** Đăng ký thành công → `201`
- [ ] **TC-003** Đăng ký trùng email → `409`
- [ ] **TC-004** Password quá ngắn → `422`
- [ ] **TC-005** Thiếu field bắt buộc → `422`
- [ ] **TC-006** ⭐ Login chuẩn OAuth2 (access_token cấp cao nhất) → `200`
- [ ] **TC-007** Login sai mật khẩu → `401`
- [ ] **TC-008** Login email không tồn tại → `401`
- [ ] **TC-009** Refresh token hợp lệ → `200`
- [ ] **TC-010** Refresh token rác → `401`

### 👤 Users
- [ ] **TC-011** /users/me không token → `401`
- [ ] **TC-012** /users/me có token → `200`
- [ ] **TC-013** /users với user thường → `403`
- [ ] **TC-014** /users admin + search → `200`

### 📢 Campaigns & Members
- [ ] **TC-015** Tạo campaign → tự thành OWNER → `201`
- [ ] **TC-016** Tạo campaign không token → `401`
- [ ] **TC-017** Cô lập dữ liệu (user B không thấy campaign A) → `200 data=[]`
- [ ] **TC-018** Xem campaign không phải member → `403`
- [ ] **TC-019** Sửa campaign không phải OWNER → `403`
- [ ] **TC-020** Thêm member trùng → `400`
- [ ] **TC-021** Xóa OWNER khỏi campaign → `400`
- [ ] **TC-022** Xóa campaign → cascade member + task → `200`

### 📝 Tasks
- [ ] **TC-023** Tạo task mặc định (TODO/MEDIUM) → `201`
- [ ] **TC-024** Gửi enum không hợp lệ → `422`
- [ ] **TC-025** Gán assignee NGOÀI campaign → `400`
- [ ] **TC-026** ⭐ Update task bởi OWNER → `200`
- [ ] **TC-027** Update task bởi member thường → `403`
- [ ] **TC-028** ⭐ Sort không hợp lệ → `400`
- [ ] **TC-029** Filter theo status → `200`
- [ ] **TC-030** Assignee xóa task của mình → `200`

### 💬 Comments
- [ ] **TC-031** Thêm comment → `201`
- [ ] **TC-032** ⭐ List comments → `200`
- [ ] **TC-033** Comment khi không phải member → `403`
- [ ] **TC-034** Xóa task → cascade comment → `200`

### 📎 Attachments
- [ ] **TC-035** Upload file sai loại (.txt) → `400`
- [ ] **TC-036** ⭐ Upload .png hợp lệ → `201`
- [ ] **TC-037** Upload khi không phải member → `403`

---

## 🩺 Nhóm 1 — Health

### TC-001 — Kiểm tra server còn sống
- **API:** `GET /health`
- **Điều kiện tiên quyết:** Server đang chạy
- **Input:** Không cần
- **Expected:**
  - Status: `200`
  - Body: `{"status": "ok"}`
- **Các bước:**
  1. Mở Swagger
  2. Gọi `GET /health` → Execute
- **Kết quả:** - [ ] Chưa test
- **Tại sao fail:** 

---

## 🔐 Nhóm 2 — Auth

### TC-002 — Đăng ký tài khoản thành công
- **API:** `POST /api/auth/register`
- **Điều kiện tiên quyết:** DB không có email này
- **Input:**
  ```json
  { "email": "user1@test.com", "full_name": "Nguyễn Văn A", "password": "secret123" }
  ```
- **Expected:**
  - Status: `201`
  - `data.email` = user1@test.com · `data.role` = "USER" · **KHÔNG có `password_hash`**
- **Các bước:** Swagger → `POST /api/auth/register` → Try it out → dán JSON trên → Execute
- **Kết quả:** - [ ] Chưa test
- **Tại sao fail:**

### TC-003 — Đăng ký trùng email
- **API:** `POST /api/auth/register`
- **Điều kiện tiên quyết:** Email đã đăng ký ở TC-002
- **Input:** Cùng JSON TC-002 (cùng email)
- **Expected:** Status `409` — "Email da duoc dang ki"
- **Các bước:** Gọi lại register với email cũ
- **Kết quả:** - [ ] Chưa test
- **Tại sao fail:**

### TC-004 — Password quá ngắn
- **API:** `POST /api/auth/register`
- **Input:** `{"email": "x@test.com", "full_name": "X", "password": "123"}`
- **Expected:** Status `422` (Pydantic chặn `min_length=6`)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-005 — Thiếu field bắt buộc
- **API:** `POST /api/auth/register`
- **Input:** `{"email": "x@test.com"}` (thiếu full_name, password)
- **Expected:** Status `422` — liệt kê đúng field thiếu
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-006 — ⭐ Login đúng — access_token ở CẤP CAO NHẤT (chuẩn OAuth2)
- **API:** `POST /api/auth/login`
- **Điều kiện tiên quyết:** Đã đăng ký user
- **Input:** form-data: `username` = email · `password`
- **Expected:**
  - Status `200`
  - Body: `access_token` **ở cấp cao nhất** (cùng hàng với `token_type`), KHÔNG nằm trong `data`
  - Đây là điều kiện để nút **Authorize** của Swagger hoạt động!
- **Các bước:**
  1. Gọi login → copy access_token
  2. Vào nút **Authorize** → nhập username/password → khóa phải mở 🔓
  3. Gọi 1 endpoint bảo vệ → 200
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-007 — Login sai mật khẩu
- **API:** `POST /api/auth/login`
- **Input:** username đúng + password sai
- **Expected:** `401` — "Email hoac mat khau khong dung" (thông báo chung)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-008 — Login email không tồn tại
- **API:** `POST /api/auth/login`
- **Input:** email lạ
- **Expected:** `401` — **cùng thông báo** với TC-007 (không lộ email nào sai — chống dò email)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-009 — Refresh token hợp lệ
- **API:** `POST /api/auth/refresh`
- **Input:** `{"refresh_token": "<refresh token từ login>"}`
- **Expected:** `200` — `data.access_token` mới
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-010 — Refresh token rác
- **API:** `POST /api/auth/refresh`
- **Input:** `{"refresh_token": "token-rac"}`
- **Expected:** `401`
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

## 👤 Nhóm 3 — Users

### TC-011 — /users/me không có token
- **API:** `GET /api/users/me`
- **Input:** Không gửi Authorization header
- **Expected:** `401` — "Not authenticated"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-012 — /users/me có token
- **API:** `GET /api/users/me`
- **Điều kiện tiên quyết:** Đã Authorize
- **Input:** Header `Authorization: Bearer <access_token>`
- **Expected:** `200` — `data.email` đúng, **không có `password_hash`**
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-013 — /users với user thường
- **API:** `GET /api/users`
- **Điều kiện tiên quyết:** Token của user role=USER (không phải admin)
- **Expected:** `403` — "Ban khong co quyen quan tri vien"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-014 — /users với admin + search
- **API:** `GET /api/users?search=Bob`
- **Điều kiện tiên quyết:** Token ADMIN (seed: `owner@example.com`)
- **Expected:** `200` — chỉ trả user khớp tên/email "Bob"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

## 📢 Nhóm 4 — Campaigns & Members

### TC-015 — Tạo campaign → tự thành OWNER
- **API:** `POST /api/campaigns`
- **Input:** `{"name": "Camp Test"}`
- **Expected:** `201` — `data.owner_id` = id user đang đăng nhập (KHÔNG cần gửi owner_id)
- **Các bước:**
  1. Login user A → Authorize
  2. Tạo campaign → kiểm tra owner_id
  3. (Nâng cao) Vào MySQL: `SELECT * FROM campaign_members WHERE campaign_id=...` → thấy dòng role=OWNER
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-016 — Tạo campaign không có token
- **API:** `POST /api/campaigns`
- **Input:** `{"name": "X"}` (không Authorize)
- **Expected:** `401`
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-017 — Cô lập dữ liệu
- **API:** `GET /api/campaigns`
- **Điều kiện tiên quyết:** User A có campaign; dùng token user B
- **Expected:** `200` — `data = []` (B không thấy campaign của A)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-018 — Xem campaign không phải member
- **API:** `GET /api/campaigns/{id}`
- **Điều kiện tiên quyết:** User lạ (không trong campaign)
- **Expected:** `403` — "Ban khong thuoc chien dich nay"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-019 — Sửa campaign không phải OWNER
- **API:** `PATCH /api/campaigns/{id}`
- **Điều kiện tiên quyết:** Token member (không phải owner)
- **Input:** `{"name": "Hack"}`
- **Expected:** `403` — "Chi owner moi duoc thuc hien"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-020 — Thêm member trùng
- **API:** `POST /api/campaigns/{id}/members`
- **Điều kiện tiên quyết:** User đã là member
- **Input:** `{"user_id": <đã có>}`
- **Expected:** `400` — "Thanh vien da co trong chien dich"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-021 — Xóa OWNER khỏi campaign
- **API:** `DELETE /api/campaigns/{id}/members/{owner_id}`
- **Input:** owner_id chính mình
- **Expected:** `400` — "Khong the xoa owner cua chien dich" (chống campaign mồ côi)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-022 — Xóa campaign → cascade
- **API:** `DELETE /api/campaigns/{id}`
- **Điều kiện tiên quyết:** Campaign có member + task
- **Expected:**
  - Status `200`
  - Sau đó `GET /api/campaigns/{id}` → `404`
  - (Nâng cao) MySQL: member + task của campaign đó đã biến mất
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

## 📝 Nhóm 5 — Tasks

### TC-023 — Tạo task với giá trị mặc định
- **API:** `POST /api/campaigns/{id}/campaign-tasks`
- **Input:** `{"title": "Task 1"}`
- **Expected:** `201` — `status="TODO"`, `priority="MEDIUM"`, `campaign_id` đúng
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-024 — Gửi enum không hợp lệ
- **API:** `POST /api/campaigns/{id}/campaign-tasks`
- **Input:** `{"title": "X", "status": "DONE_X", "priority": "SUPER"}`
- **Expected:** `422` — enum chặn ngay (không cần if-check tay)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-025 — Gán assignee NGOÀI campaign
- **API:** `POST /api/campaigns/{id}/campaign-tasks`
- **Điều kiện tiên quyết:** User Z không trong campaign
- **Input:** `{"title": "X", "assignee_id": <id user Z>}`
- **Expected:** `400` — "Nguoi duoc giao viec khong thuoc chien dich"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-026 — ⭐ Update task bởi OWNER (regression bug `_can_management_task`)
- **API:** `PATCH /api/campaign-tasks/{id}`
- **Điều kiện tiên quyết:** Token OWNER của campaign
- **Input:** `{"title": "Đã sửa", "status": "IN_PROGRESS"}`
- **Expected:** `200` — title + status đổi đúng
  > [!bug] Trước đây: truyền `task.campaign_id` (int) thay vì `task` (object) → AttributeError → **500**. Đã sửa dòng 78 `task_service.py`.
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-027 — Update task bởi member thường
- **API:** `PATCH /api/campaign-tasks/{id}`
- **Điều kiện tiên quyết:** Member (không owner, không assignee)
- **Input:** `{"title": "Hack"}`
- **Expected:** `403` — "Ban khong co quyen cap nhat dau viec nay"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-028 — ⭐ Sort không hợp lệ (regression bug sort)
- **API:** `GET /api/campaigns/{id}/campaign-tasks?sort=xyz`
- **Expected:** `400` — "Truong sort khong hop le"
  > [!bug] Trước đây: `getattr(CampaignTask, "xyz")` → AttributeError → **500**. Đã thêm whitelist cột sort trong `task_service.py`.
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-029 — Filter theo status
- **API:** `GET /api/campaigns/{id}/campaign-tasks?status=TODO`
- **Điều kiện tiên quyết:** Có 2 task khác status
- **Expected:** `200` — chỉ trả task status=TODO
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-030 — Assignee xóa task của mình
- **API:** `DELETE /api/campaign-tasks/{id}`
- **Điều kiện tiên quyết:** Token của assignee được giao task đó
- **Expected:** `200`
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

## 💬 Nhóm 6 — Comments

### TC-031 — Thêm comment
- **API:** `POST /api/campaign-tasks/{id}/comments`
- **Input:** `{"content": "Comment 1"}`
- **Expected:** `201` — `data.comment_id > 0`
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-032 — ⭐ List comments (regression: từng bị 405)
- **API:** `GET /api/campaign-tasks/{id}/comments`
- **Điều kiện tiên quyết:** Task có ít nhất 1 comment
- **Expected:** `200` — danh sách comment, có content + user_id + created_at
  > [!bug] Trước đây: service có hàm `list_comment` nhưng router **thiếu endpoint** → 405. Đã thêm route GET.
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-033 — Comment khi không phải member
- **API:** `POST /api/campaign-tasks/{id}/comments`
- **Điều kiện tiên quyết:** User lạ
- **Input:** `{"content": "X"}`
- **Expected:** `403` — "Ban khong thuoc chien dich nay"
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-034 — Xóa task → comment mất theo (cascade)
- **API:** `DELETE /api/campaign-tasks/{id}`
- **Điều kiện tiên quyết:** Task có comment
- **Expected:** `200`; sau đó `GET .../comments` → `404` (task đã xóa, comment cũng mất)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

## 📎 Nhóm 7 — Attachments

### TC-035 — Upload file sai loại (.txt)
- **API:** `POST /api/campaign-tasks/{id}/attachments`
- **Input:** multipart `file` = file .txt (text/plain)
- **Expected:** `400` — "Loại file không được phép" (kiểm tra cả content_type + đuôi file)
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-036 — ⭐ Upload .png hợp lệ (regression bug Path import)
- **API:** `POST /api/campaign-tasks/{id}/attachments`
- **Input:** multipart `file` = file .png (image/png)
- **Expected:** `201` — `data.path` bắt đầu `uploads/` và kết thúc `.png`
  > [!bug] Trước đây: `from fastapi import Path` che mất `pathlib.Path` → AssertionError → **500**. Đã sửa import dòng 4 `campaign_tasks.py`.
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

### TC-037 — Upload khi không phải member
- **API:** `POST /api/campaign-tasks/{id}/attachments`
- **Điều kiện tiên quyết:** User lạ
- **Input:** multipart .png + token user lạ
- **Expected:** `403`
- **Kết quả:** - [ ] Chưa test · **Tại sao fail:**

---

> [!success] Khi hoàn thành
> 37/37 pass = project sẵn sàng demo & vấn đáp. Ghi nhớ kể 4 câu chuyện bug ⭐ khi được hỏi "em gặp lỗi gì khi làm dự án?"
