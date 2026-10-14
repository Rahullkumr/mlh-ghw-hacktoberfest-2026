-- Accelerate Dashboards with Continuous Aggregates
-- Daily per-walker metrics on the `walks` hypertable (see ../tiger-hypertable).
-- Run each statement on its own: CAGG creation and refresh can't run inside a transaction block.

CREATE MATERIALIZED VIEW walks_daily
WITH (timescaledb.continuous) AS
SELECT
  time_bucket('1 day', ts) AS day,
  walker,
  count(*)     AS walks,
  sum(steps)   AS total_steps,
  sum(minutes) AS total_minutes,
  max(steps)   AS best_walk_steps
FROM walks
GROUP BY day, walker
WITH DATA;

-- Refresh the last 30 days every hour, leaving the newest hour to real-time aggregation
SELECT add_continuous_aggregate_policy('walks_daily',
  start_offset      => INTERVAL '30 days',
  end_offset        => INTERVAL '1 hour',
  schedule_interval => INTERVAL '1 hour');

-- Real-time mode: merge not-yet-materialized rows at query time
ALTER MATERIALIZED VIEW walks_daily SET (timescaledb.materialized_only = false);

-- Late write into an already-materialized bucket needs an explicit refresh
INSERT INTO walks (ts, walker, steps, minutes, place)
VALUES (now() - interval '5 minutes', 'nana', 4321, 35, 'pandal');

CALL refresh_continuous_aggregate('walks_daily', now() - INTERVAL '3 days', NULL);

-- Dashboard query
SELECT day::date, walks, total_steps, total_minutes, best_walk_steps
FROM walks_daily
ORDER BY day DESC
LIMIT 7;

-- Weekly rollup served from the aggregate instead of raw rows
SELECT time_bucket('7 days', day) AS week,
       sum(walks)                 AS walks,
       sum(total_steps)           AS steps,
       round(avg(total_minutes))  AS avg_daily_minutes
FROM walks_daily
GROUP BY week
ORDER BY week;
