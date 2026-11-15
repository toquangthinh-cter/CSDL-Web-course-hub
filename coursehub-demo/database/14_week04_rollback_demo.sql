-- Chạy từng khối. Khối 2 sẽ lỗi: đó là điều mong đợi.
-- Khối 1: dọn dữ liệu
DELETE FROM enrollments WHERE class_section_id = 'RACE-01';
DELETE FROM enrollment_events WHERE class_section_id = 'RACE-01' AND dataset = 'demo';

-- Khối 2: transaction cố ý lỗi
BEGIN;
INSERT INTO enrollments (student_id, class_section_id)
VALUES ('22000004', 'RACE-01');
INSERT INTO enrollment_events (student_id, class_section_id, event_type, source, dataset)
VALUES ('22000004', 'RACE-01', 'INVALID', 'api', 'demo');
COMMIT;

-- Khối 3: nếu khối 2 báo lỗi, chạy ngay lệnh này trên cùng tab
ROLLBACK;

-- Khối 4: kiểm tra, cả hai phải bằng 0
SELECT COUNT(*) AS enrollments_race FROM enrollments WHERE class_section_id = 'RACE-01';
SELECT COUNT(*) AS events_race FROM enrollment_events
WHERE class_section_id = 'RACE-01' AND dataset = 'demo';