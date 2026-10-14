-- Set up a Tiger Cloud service and create your first Hypertable
-- 30 days of simulated morning walks, partitioned into 1-day chunks.

CREATE TABLE walks (
  ts         TIMESTAMPTZ NOT NULL,
  walker     TEXT        NOT NULL,
  steps      INTEGER     NOT NULL,
  minutes    INTEGER     NOT NULL,
  place      TEXT
);

SELECT create_hypertable('walks', by_range('ts', INTERVAL '1 day'));

INSERT INTO walks (ts, walker, steps, minutes, place)
SELECT
  date_trunc('day', now()) - (d || ' days')::interval + interval '6 hours' + (random() * interval '2 hours'),
  'nana',
  (2000 + random() * 4000)::int,
  (20 + random() * 40)::int,
  (ARRAY['park','temple','market','pandal','river ghat'])[1 + floor(random() * 5)::int]
FROM generate_series(0, 29) AS d;

-- Weekly rollup
SELECT time_bucket('7 days', ts) AS week,
       count(*)              AS walks,
       sum(steps)            AS total_steps,
       round(avg(minutes))   AS avg_minutes
FROM walks
GROUP BY week
ORDER BY week;

-- Chunks created by time partitioning
SELECT chunk_name, range_start, range_end
FROM timescaledb_information.chunks
WHERE hypertable_name = 'walks'
ORDER BY range_start DESC
LIMIT 5;
