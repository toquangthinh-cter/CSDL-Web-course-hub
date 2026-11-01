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