-- Truy vấn thống kê: 1 lớp, 1 loại sự kiện, 1 tuần
EXPLAIN (ANALYZE, BUFFERS)
SELECT class_section_id, event_type, COUNT(*) AS total
FROM enrollment_events
WHERE dataset = 'performance'
  AND class_section_id = 'WEB-01'
  AND event_type = 'CREATED'
  AND occurred_at >= TIMESTAMP '2025-06-01 00:00:00'
  AND occurred_at <  TIMESTAMP '2025-06-08 00:00:00'
GROUP BY class_section_id, event_type;