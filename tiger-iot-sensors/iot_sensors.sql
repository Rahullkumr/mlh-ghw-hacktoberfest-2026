-- Simulate an IoT sensor dataset for testing and development with Tiger Cloud
-- 4 sensors, one reading every 5 minutes for 24 hours.

CREATE TABLE sensors (
  id       SERIAL PRIMARY KEY,
  type     VARCHAR(50),
  location VARCHAR(50)
);

CREATE TABLE sensor_data (
  time        TIMESTAMPTZ NOT NULL,
  sensor_id   INTEGER REFERENCES sensors(id),
  temperature DOUBLE PRECISION,
  cpu         DOUBLE PRECISION
);

SELECT create_hypertable('sensor_data', by_range('time', INTERVAL '1 hour'));

INSERT INTO sensors (type, location) VALUES
  ('a', 'floor'), ('a', 'ceiling'), ('b', 'floor'), ('b', 'ceiling');

INSERT INTO sensor_data (time, sensor_id, cpu, temperature)
SELECT time, sensor_id, random() AS cpu, random() * 100 AS temperature
FROM generate_series(now() - INTERVAL '24 hours', now(), INTERVAL '5 minutes') AS g1(time),
     generate_series(1, 4, 1) AS g2(sensor_id);

-- Row count and time range
SELECT count(*) AS readings, min(time) AS first, max(time) AS last
FROM sensor_data;

-- 30-minute averages
SELECT time_bucket('30 minutes', time) AS period,
       avg(temperature)                AS avg_temp,
       avg(cpu)                        AS avg_cpu
FROM sensor_data
GROUP BY period
ORDER BY period DESC
LIMIT 10;

-- Per-sensor summary joined with metadata
SELECT s.type, s.location,
       round(avg(d.temperature)::numeric, 2) AS avg_temp,
       round(max(d.cpu)::numeric, 3)         AS peak_cpu,
       last(d.temperature, d.time)           AS latest_temp
FROM sensor_data d
JOIN sensors s ON s.id = d.sensor_id
GROUP BY s.type, s.location
ORDER BY s.type, s.location;
