CREATE EXTENSION postgis;

CREATE TYPE selection_type AS ENUM (
    'single',
    'multi'
);

CREATE TYPE city AS ENUM (
    'Moscow'
)

CREATE TABLE IF NOT EXISTS properties (
    id SERIAL PRIMARY KEY,

    name TEXT,
    location GEOGRAPHY(Point, 4326) NOT NULL,

    site_url TEXT,
    city city,
    address TEXT,
    completion_year SMALLINT,

    extra_info TEXT,

    created_at TIMESTAMPTZ DEFAULT now()
)