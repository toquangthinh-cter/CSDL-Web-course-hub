# Buổi 6 - Docker, Testing, CI

## Môi trường
- OS: Windows
- Docker version: Docker Desktop (Compose v2)
- Python / Node version: Python 3.12 / Node 22.12.0

## Kết quả local
- `pytest backend/tests -q`: 2 passed
- `npm test`: pass (kiểm thử api.js)
- `npm run build`: build thành công thư mục dist
- `docker compose up --build`: backend healthy (port 8000), frontend chạy port 8080

## Một luồng tích hợp đã kiểm tra
- Request: Mở http://127.0.0.1:8080, chọn SV 22000004, đăng ký WEB-01 qua `/api/enrollments` và hủy đăng ký.
- HTTP status: 201 Created khi đăng ký, 204 No Content khi hủy.
- SQL xác nhận: Bảng `enrollments` và `enrollment_events` ghi nhận CREATED/CANCELLED; view `v_section_summary` cập nhật đúng số chỗ.

## Debug / AI
- Lỗi gặp phải:
  1. Workflow CI nằm trong thư mục con `coursehub-demo/.github/workflows` nên GitHub Actions không nhận diện được -> Di chuyển ra thư mục gốc `.github/workflows/ci.yml` và thêm tiền tố `coursehub-demo/`.
  2. File YAML/INI trên Windows dính UTF-8 BOM làm GitHub Actions báo lỗi cú pháp ngay lập tức -> Ghi lại file bằng UTF-8 without BOM.
  3. Job `backend` thiếu biến môi trường `DB_*` khi import `database.py` -> Bổ sung biến `DB_*` giả lập trong bước chạy `pytest` trên CI.
- Bằng chứng đã xem: Log từng step trên GitHub Actions, `git ls-files`, và `docker compose logs`.

## Pull Request / CI
- PR: #9 (nhánh `week06-docker-ci`)
- Reviewer: (Điền tên thành viên review trong nhóm)
- CI run: Pass (cả 3 job `backend`, `frontend`, `docker` đều xanh).