CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS events (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    speaker TEXT,
    location GEOGRAPHY(Point, 4326),
    address TEXT,

    event_at TIMESTAMPTZ NOT NULL,

    description TEXT,
    signup_link TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_events_event_at_id
ON events (event_at DESC, id DESC);
