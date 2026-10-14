-- Implement AI-Powered Vector Search with pgvector
-- Hybrid search: vector similarity + time-range filter on a hypertable, DiskANN index (pgvectorscale).

CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;  -- also installs pgvector

CREATE TABLE walk_notes (
  ts        TIMESTAMPTZ NOT NULL,
  place     TEXT        NOT NULL,
  note      TEXT        NOT NULL,
  -- dims: temple, market, nature, festival, food, social, effort, weather
  embedding VECTOR(8)   NOT NULL
);

SELECT create_hypertable('walk_notes', by_range('ts', INTERVAL '7 days'));

INSERT INTO walk_notes (ts, place, note, embedding) VALUES
 (now() - INTERVAL '27 days', 'temple',     'Morning aarti at the Shiv mandir, sat on the steps after',         '[0.9,0.0,0.2,0.1,0.0,0.3,0.2,0.1]'),
 (now() - INTERVAL '24 days', 'market',     'Bought guavas at the haat, haggled with the sabzi wala',          '[0.0,0.9,0.0,0.1,0.6,0.5,0.3,0.0]'),
 (now() - INTERVAL '21 days', 'river ghat', 'Quiet walk along the river, watched egrets on the sandbank',      '[0.1,0.0,0.9,0.0,0.0,0.1,0.4,0.3]'),
 (now() - INTERVAL '18 days', 'park',       'Laps around the park, rain clouds rolled in, came home early',    '[0.0,0.0,0.7,0.0,0.0,0.1,0.5,0.9]'),
 (now() - INTERVAL '15 days', 'market',     'Chai and samosa at the corner stall with old friends',            '[0.0,0.5,0.0,0.1,0.9,0.8,0.1,0.0]'),
 (now() - INTERVAL '12 days', 'temple',     'Long climb up to the hill temple, knees complained but worth it', '[0.8,0.0,0.4,0.1,0.0,0.1,0.9,0.1]'),
 (now() - INTERVAL '9 days',  'pandal',     'First Durga Puja pandal visit, lights and dhak drums',            '[0.4,0.1,0.0,0.9,0.2,0.6,0.3,0.0]'),
 (now() - INTERVAL '6 days',  'pandal',     'Pandal hopping with grandkids, ate jalebi at the mela',           '[0.3,0.2,0.0,0.9,0.7,0.9,0.5,0.0]'),
 (now() - INTERVAL '3 days',  'river ghat', 'Foggy morning by the river, cool breeze, very peaceful',          '[0.1,0.0,0.8,0.0,0.0,0.0,0.3,0.7]'),
 (now() - INTERVAL '1 day',   'park',       'Walked with the morning group, talked about the Diwali plans',    '[0.0,0.0,0.5,0.4,0.0,0.9,0.4,0.1]');

CREATE INDEX walk_notes_embedding_idx ON walk_notes USING diskann (embedding vector_cosine_ops);

-- 1. "Peaceful nature walk", all time
SELECT ts::date, place, note,
       round((embedding <=> '[0.0,0.0,1.0,0.0,0.0,0.0,0.3,0.4]')::numeric, 3) AS cosine_distance
FROM walk_notes
ORDER BY embedding <=> '[0.0,0.0,1.0,0.0,0.0,0.0,0.3,0.4]'
LIMIT 3;

-- 2. Hybrid: "festival with food and people", last 10 days only
SELECT ts::date, place, note,
       round((embedding <=> '[0.0,0.0,0.0,1.0,0.6,0.8,0.0,0.0]')::numeric, 3) AS cosine_distance
FROM walk_notes
WHERE ts > now() - INTERVAL '10 days'
ORDER BY embedding <=> '[0.0,0.0,0.0,1.0,0.6,0.8,0.0,0.0]'
LIMIT 3;

-- 3. Hybrid: "food with friends", older than 10 days
SELECT ts::date, place, note,
       round((embedding <=> '[0.0,0.3,0.0,0.0,1.0,0.8,0.0,0.0]')::numeric, 3) AS cosine_distance
FROM walk_notes
WHERE ts <= now() - INTERVAL '10 days'
ORDER BY embedding <=> '[0.0,0.3,0.0,0.0,1.0,0.8,0.0,0.0]'
LIMIT 3;
