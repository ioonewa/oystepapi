CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    bio TEXT,
    avatar_url TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    preview_url TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS course_authors (
    course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,
    author_id INT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,

    PRIMARY KEY (course_id, author_id)
);


CREATE TABLE IF NOT EXISTS lessons (
    id SERIAL PRIMARY KEY,
    course_id INT NOT NULL REFERENCES courses(id) ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT,

    video_url TEXT,
    preview_url TEXT,

    duration_seconds INT,

    position INT NOT NULL,        -- порядок в курсе

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS lesson_authors (
    lesson_id INT NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    author_id INT NOT NULL REFERENCES authors(id) ON DELETE CASCADE,

    PRIMARY KEY (lesson_id, author_id)
);


CREATE INDEX IF NOT EXISTS lessons_course_position_idx
ON lessons(course_id, position);