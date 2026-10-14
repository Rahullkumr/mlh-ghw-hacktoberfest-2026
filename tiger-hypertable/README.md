# Set up a Tiger Cloud service and create your first Hypertable

`walks` hypertable: 30 days of simulated morning walks, split into **1-day chunks**.
Queries that filter by time only touch the chunks in range instead of scanning the whole table.

- SQL: [hypertable.sql](hypertable.sql)
- Service: `touchgrass` (see [tiger-mcp-integration](../tiger-mcp-integration/))

Sample weekly rollup:

| week       | walks | total_steps | avg_minutes |
|------------|------:|------------:|------------:|
| 2026-09-14 | 7     | 28656       | 45          |
| 2026-09-21 | 7     | 32355       | 41          |
| 2026-09-28 | 7     | 25342       | 31          |
| 2026-10-05 | 7     | 25014       | 41          |
