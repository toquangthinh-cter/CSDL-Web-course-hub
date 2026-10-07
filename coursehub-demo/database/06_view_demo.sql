-- 3. Quan sát view khi có một đăng ký mới
BEGIN;

INSERT INTO enrollments (student_id, class_section_id)
VALUES('22000004', 'WEB-01');
-- 3.1. Xem kết quả rồi hoàn tác
SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';

ROLLBACK;

SELECT class_id, capacity, enrolled, remaining
FROM v_section_summary
WHERE class_id = 'WEB-01';