# Accelerate Dashboards with Continuous Aggregates

`walks_daily` continuous aggregate on the `walks` hypertable: daily walks, total steps,
total minutes, and best single walk per walker.

- **Refresh policy:** every hour, re-materializes the last 30 days, skipping the newest hour.
- **Real-time mode:** `materialized_only = false`, so rows newer than the last refresh are merged in at query time.
- SQL: [continuous_aggregate.sql](continuous_aggregate.sql)

## Gotcha found while testing

A walk inserted into *today's* bucket didn't show up, even with real-time mode on. The bucket
was already materialized when the view was created, so the watermark sat past it. Real-time
aggregation only covers rows **after** the watermark; late writes into materialized buckets
wait for a refresh. An explicit `refresh_continuous_aggregate` fixed it:

| day        | walks | total_steps | best_walk_steps |
|------------|------:|------------:|----------------:|
| before     | 1     | 2447        | 2447            |
| after      | 2     | 6768        | 4321            |
