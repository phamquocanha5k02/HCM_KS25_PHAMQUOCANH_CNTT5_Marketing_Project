
# Campaign — Checklist Kịch Bản Test Chi Tiết

> Checklist test thủ công cho toàn bộ API — chi tiết hơn bản Excel `CHECKLIST_TEST.xlsx` (37 kịch bản). Mỗi kịch bản có: điều kiện tiên quyết, input, expected output, các bước thực hiện và checkbox kết quả.
>
> ⭐ = kịch bản regression cho các bug đã sửa.

## 🧭 Hướng dẫn sử dụng

1. Chạy server: `uvicorn main:app --reload` → mở `http://127.0.0.1:8000/docs`
2. Bấm **Authorize** → `username` + `password` (không cần client_secret) → khóa 🔓
3. Với mỗi kịch bản: làm theo **Các bước** → đối chiếu **Expected** → đánh dấu kết quả
4. Nếu Fail → ghi rõ lỗi vào **Tại sao fail**

> [!warning] Tài khoản test nhanh
> Seed tạo sẵn: `owner@example.com` / `Owner123!` (ADMIN) · `member@example.com` / `Member123!` (USER)
> Access token hết hạn sau **30 phút** — hết hạn thì Authorize lại.

---

## 📊 Mục 1 — Bảng tổng hợp 37 kịch bản

| Mã | Nhóm | Mô tả | API | Expected |
|---|---|---|---|---|
| TC-001 | Health | Server sống | GET /health | 200 |
| TC-002 | Auth | Đăng ký thành công | POST /api/auth/register | 201 |
| TC-003 | Auth | Đăng ký trùng email | POST /api/auth/register | 409 |
| TC-004 | Auth | Password ngắn | POST /api/auth/register | 422 |
| TC-005 | Auth | Thiếu field | POST /api/auth/register | 422 |
| TC-006 | Auth | ⭐ Login chuẩn OAuth2 | POST /api/auth/login | 200, access_token cấp cao nhất |
| TC-007 | Auth | Login sai mật khẩu | POST /api/auth/login | 401 |
| TC-008 | Auth | Login email lạ | POST /api/auth/login | 401 |
| TC-009 | Auth | Refresh hợp lệ | POST /api/auth/refresh | 200 |
| TC-010 | Auth | Refresh token rác | POST /api/auth/refresh | 401 |
| TC-011 | Users | /me không token | GET /api/users/me | 401 |
| TC-012 | Users | /me có token | GET /api/users/me | 200 |
| TC-013 | Users | /users user thường | GET /api/users | 403 |
| TC-014 | Users | /users admin + search | GET /api/users?search= | 200 |
| TC-015 | Campaign | Tạo campaign → OWNER | POST /api/campaigns | 201 |
| TC-016 | Campaign | Tạo không token | POST /api/campaigns | 401 |
| TC-017 | Campaign | Cô lập dữ liệu | GET /api/campaigns | 200, data=[] |
| TC-018 | Campaign | Xem không phải member | GET /api/campaigns/{id} | 403 |
| TC-019 | Campaign | Sửa không phải OWNER | PATCH /api/campaigns/{id} | 403 |
| TC-020 | Member | Thêm member trùng | POST /api/campaigns/{id}/members | 400 |
| TC-021 | Member | Xóa OWNER | DELETE /api/campaigns/{id}/members/{uid} | 400 |
| TC-022 | Campaign | Xóa campaign cascade | DELETE /api/campaigns/{id} | 200 |
| TC-023 | Task | Tạo task mặc định | POST /api/campaigns/{id}/campaign-tasks | 201 |
| TC-024 | Task | Enum sai | POST task | 422 |
| TC-025 | Task | Assignee ngoài campaign | POST task | 400 |
| TC-026 | Task | ⭐ Update bởi OWNER | PATCH /api/campaign-tasks/{id} | 200 |
| TC-027 | Task | Update bởi member | PATCH task | 403 |
| TC-028 | Task | ⭐ Sort sai | GET task?sort=xyz | 400 |
| TC-029 | Task | Filter status | GET task?status=TODO | 200 |
| TC-030 | Task | Assignee xóa task mình | DELETE task | 200 |
| TC-031 | Comment | Thêm comment | POST .../comments | 201 |
| TC-032 | Comment | ⭐ List comments | GET .../comments | 200 |
| TC-033 | Comment | Comment không phải member | POST comments | 403 |
| TC-034 | Comment | Xóa task → cascade comment | DELETE task | 200 |
| TC-035 | Attachment | Upload sai loại | POST .../attachments | 400 |
| TC-036 | Attachment | ⭐ Upload .png | POST .../attachments | 201 |
| TC-037 | Attachment | Upload không phải member | POST .../attachments | 403 |

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

## ✅ Checklist tổng cuối buổi

### Health & Auth
- [ ] TC-001 Server sống
- [ ] TC-002 Đăng ký OK
- [ ] TC-003 Trùng email 409
- [ ] TC-004/005 Validation 422
- [ ] TC-006 ⭐ Login chuẩn OAuth2
- [ ] TC-007/008 Sai thông tin 401
- [ ] TC-009/010 Refresh

### Users
- [ ] TC-011/012 /me 401 & 200
- [ ] TC-013/014 /users 403 & 200 + search

### Campaigns & Members
- [ ] TC-015/016 Tạo campaign + không token
- [ ] TC-017/018 Cô lập + 403
- [ ] TC-019 Sửa không phải owner 403
- [ ] TC-020/021 Member trùng + xóa owner
- [ ] TC-022 Cascade

### Tasks
- [ ] TC-023/024 Tạo + enum 422
- [ ] TC-025 Assignee ngoài 400
- [ ] TC-026 ⭐ Update owner 200
- [ ] TC-027 Update member 403
- [ ] TC-028 ⭐ Sort sai 400
- [ ] TC-029/030 Filter + assignee xóa

### Comments & Attachments
- [ ] TC-031/032 ⭐ Thêm + list comments
- [ ] TC-033/034 403 + cascade
- [ ] TC-035/036 ⭐ Upload sai loại + png
- [ ] TC-037 Upload 403

> [!success] Khi hoàn thành
> 37/37 pass = project sẵn sàng demo & vấn đáp. Ghi nhớ kể 4 câu chuyện bug ⭐ khi được hỏi "em gặp lỗi gì khi làm dự án?"
