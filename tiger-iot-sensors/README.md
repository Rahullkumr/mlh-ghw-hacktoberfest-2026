# Simulate an IoT sensor dataset with Tiger Cloud

4 sensors (`sensors` table, relational metadata) and a `sensor_data` hypertable with
**1,156 readings**: one every 5 minutes for 24 hours, in 1-hour chunks.

- SQL: [iot_sensors.sql](iot_sensors.sql)

Per-sensor summary:

| type | location | avg_temp | peak_cpu |
|------|----------|---------:|---------:|
| a    | ceiling  | 48.50    | 0.999    |
| a    | floor    | 49.01    | 0.997    |
| b    | ceiling  | 49.98    | 0.994    |
| b    | floor    | 51.27    | 0.997    |
