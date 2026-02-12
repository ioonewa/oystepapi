-- feed_item
--  ├─ feed_item_content      (текст, краткое описание)
--  ├─ feed_item_media        (1..N медиа)
--  ├─ feed_item_button       (0..1)
--  ├─ feed_item_type_ext     (1..1, по типу)
--  └─ selection_ext
--      ├─ properties (map)
--      └─ related selections

CREATE TYPE media_type AS ENUM (
    'image',
    'video'
);

CREATE TYPE selection_type AS ENUM (
    'single',
    'multi'
);

-- Храним отдельно контент, чтобы отдавать их отдельно для фильтрации
CREATE TABLE feed_item_types (
    id SERIAL PRIMARY KEY,
    code TEXT UNIQUE NOT NULL,   -- 'oyreels', 'oynews', 'selection'
    title TEXT NOT NULL          -- отображаемое название
);

-- Основа
-- Основа
CREATE TABLE feed_items (
    id BIGSERIAL PRIMARY KEY,

    type TEXT not null REFERENCES feed_item_types(code),
    status TEXT NOT NULL DEFAULT 'published',

    published_at TIMESTAMPTZ DEFAULT now(),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_feed_items_published
    ON feed_items (published_at DESC);

CREATE INDEX idx_feed_items_type
    ON feed_items (type);


CREATE TABLE media_items (
    id BIGSERIAL PRIMARY KEY,

    type media_type NOT NULL,

    url TEXT NOT NULL,
    preview_url TEXT,          -- превью для видео

    width INT,
    height INT,
    duration_seconds INT,

    created_at TIMESTAMPTZ DEFAULT now()
);

-- Контент
CREATE TABLE feed_item_content (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE,

    preview_media_id BIGINT NOT NULL REFERENCES media_items(id),
    title TEXT NOT NULL,
    short_description TEXT,
    body TEXT
);

CREATE TABLE feed_item_media (
    feed_item_id BIGINT
        REFERENCES feed_items(id) ON DELETE CASCADE,

    media_item_id BIGINT
        REFERENCES media_items(id),

    position INT DEFAULT 0,

    PRIMARY KEY (feed_item_id, media_item_id)
);

CREATE TABLE feed_item_buttons (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE,

    text TEXT NOT NULL,
    link TEXT NOT NULL
);

CREATE TABLE reel_posts (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE
);
CREATE TABLE news_posts (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE,

    source TEXT,
    original_url TEXT
);
CREATE TABLE selection_posts (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE,

    selection_type selection_type NOT NULL DEFAULT 'single'
);

CREATE TABLE selection_properties (
    feed_item_id BIGINT
        REFERENCES selection_posts(feed_item_id) ON DELETE CASCADE,

    property_id INT
        REFERENCES properties(id) ON DELETE CASCADE,

    position INT,

    PRIMARY KEY (feed_item_id, property_id)
);


CREATE TABLE related_selections (
    parent_feed_item_id BIGINT
        REFERENCES selection_posts(feed_item_id) ON DELETE CASCADE,

    related_feed_item_id BIGINT
        REFERENCES selection_posts(feed_item_id) ON DELETE CASCADE,

    position INT,

    PRIMARY KEY (parent_feed_item_id, related_feed_item_id),
    CHECK (parent_feed_item_id <> related_feed_item_id)
);

CREATE TABLE user_favourites (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    feed_item_id BIGINT REFERENCES feed_items(id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ DEFAULT now(),
    PRIMARY KEY (user_id, feed_item_id)
);

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


-- feed_item (course)
--  ├─ feed_item_content
--  ├─ course_posts
--  ├─ course_authors
--  └─ lessons
--      ├─ lesson_media
--      └─ lesson_authors

CREATE TABLE course_posts (
    feed_item_id BIGINT PRIMARY KEY
        REFERENCES feed_items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS authors (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    bio TEXT,
    avatar_media_id BIGINT REFERENCES media_items(id),
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE course_authors (
    feed_item_id BIGINT
        REFERENCES course_posts(feed_item_id) ON DELETE CASCADE,

    author_id INT
        REFERENCES authors(id) ON DELETE CASCADE,

    PRIMARY KEY (feed_item_id, author_id)
);

CREATE TABLE lessons (
    id BIGSERIAL PRIMARY KEY,

    course_feed_item_id BIGINT
        REFERENCES course_posts(feed_item_id) ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT,

    position INT NOT NULL,

    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ
);


-- Медиа для отдельных уроков
CREATE TABLE lesson_media (
    lesson_id BIGINT
        REFERENCES lessons(id) ON DELETE CASCADE,

    media_item_id BIGINT
        REFERENCES media_items(id),

    position INT DEFAULT 0,

    PRIMARY KEY (lesson_id, media_item_id)
);
