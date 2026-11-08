# CourseHub - Buoi 4

- Migration 001: enrollment_events.
- Demo class: RACE-01, capacity = 1.
- POST /enrollments: lock class_sections bang FOR UPDATE.
- Concurrency test: 1 request 201, 1 request 409.
- Performance data: 100000 rows, dataset=performance.
- Index: idx_enrollment_events_dataset_student_time.
- Ghi lai scan type va Execution Time truoc/sau o day.
Limit  (cost=2914.77..2914.90 rows=50 width=39) (actual time=10.807..10.814 rows=50.00 loops=1)
  Buffers: shared hit=1137
  ->  Sort  (cost=2914.77..2916.86 rows=835 width=39) (actual time=10.805..10.808 rows=50.00 loops=1)
        Sort Key: occurred_at DESC
        Sort Method: top-N heapsort  Memory: 31kB
        Buffers: shared hit=1137
        ->  Seq Scan on enrollment_events  (cost=0.00..2887.03 rows=835 width=39) (actual time=0.098..10.516 rows=820.00 loops=1)
              Filter: ((occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone) AND ((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text))
              Rows Removed by Filter: 99182
              Buffers: shared hit=1137
Planning:
  Buffers: shared hit=44 read=1 dirtied=1
Planning Time: 4.784 ms
Execution Time: 10.854 ms
# Sau khi tạo index
Limit  (cost=0.42..67.71 rows=50 width=39) (actual time=0.148..0.248 rows=50.00 loops=1)
  Buffers: shared hit=50 read=3
  ->  Index Scan using idx_enrollment_events_dataset_student_time on enrollment_events  (cost=0.42..1110.79 rows=825 width=39) (actual time=0.146..0.239 rows=50.00 loops=1)
        Index Cond: (((dataset)::text = 'performance'::text) AND ((student_id)::text = '22000001'::text) AND (occurred_at >= '2025-12-20 00:00:00'::timestamp without time zone))
        Index Searches: 1
        Buffers: shared hit=50 read=3
Planning:
  Buffers: shared hit=39 read=1
Planning Time: 2.995 ms
Execution Time: 0.293 ms
## Bài 2 - rollback
- Ca lỗi: POST /demo/rollback-test -> 409; enrollments RACE-01 = 0, events = 0.
- Đối chứng: POST /enrollments -> 201; enrollments = 1, events = 1.
- Kết luận: INSERT enrollments bị hoàn tác khi INSERT enrollment_events lỗi (Atomicity).
## Bài 3 - index thứ hai

Truy vấn: thống kê số sự kiện CREATED của lớp WEB-01 trong tuần 01/06/2025 - 08/06/2025
(dataset = performance). Kết quả trả về 411 dòng được đếm.

| | Scan type | Rows Removed by Filter | Execution Time | Buffers |
|---|---|---|---|---|
| Trước (chỉ có idx_..._dataset_student_time) | Bitmap Heap Scan + Bitmap Index Scan | 1507 | 10.951 ms | shared hit=309 read=27 |
| Sau (có idx_..._dataset_section_type_time) | Index Only Scan | 0 (không xuất hiện, mọi điều kiện nằm trong Index Cond) | 0.493 ms | shared hit=1 read=6 |

Nhận xét:
- Execution Time giảm từ 10.951 ms xuống 0.493 ms (khoảng 22 lần).
- Số buffer truy cập giảm từ 336 (309 + 27) xuống 7 (1 + 6).
- Trước khi có index mới, PostgreSQL chỉ lọc được theo dataset và occurred_at bằng
  index cũ nên đọc 1918 dòng từ bảng, loại 1507 dòng không phải WEB-01 hoặc CREATED,
  giữ lại 411 dòng.
- Index mới có dataset, class_section_id, event_type (điều kiện bằng) đứng trước
  và occurred_at (điều kiện khoảng) đứng cuối, nên toàn bộ điều kiện nằm trong
  Index Cond. Truy vấn chỉ dùng 4 cột này nên PostgreSQL dùng Index Only Scan với
  Heap Fetches = 0, không phải đọc bảng.

Ca phạm vi rộng: Seq Scan vì điều kiện occurred_at >= '2025-01-01' và
dataset = 'performance' khớp gần như toàn bộ bảng (Rows Removed by Filter chỉ là 2).
Khi phải lấy gần hết dòng, đọc tuần tự bảng (1137 buffers, 32.170 ms) rẻ hơn đi qua
index rồi quay lại bảng, nên planner không dùng index.

Lưu ý:
- Planning Time tăng nhẹ (1.077 ms -> 3.450 ms) do có thêm index để cân nhắc, không đáng kể
  so với thời gian thực thi giảm.
- Các số liệu lấy từ một lần chạy; read > 0 cho thấy một phần dữ liệu chưa nằm trong cache.