-- Mất toàn bộ nội dung cột note; các cột khác và số dòng giữ nguyên.
BEGIN;

ALTER TABLE enrollment_events DROP COLUMN note;
DELETE FROM schema_migrations WHERE version = '002';

COMMIT;