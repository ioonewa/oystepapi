CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    telegram_id BIGINT UNIQUE NOT NULL,
    username VARCHAR(50),
    status TEXT,

    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE IF NOT EXISTS user_profiles (
    user_id INT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    
    name TEXT,           --Содержит Имя и Фамилию
    phone_number TEXT,
    city TEXT,
    email TEXT,   
    telegram_photo_id TEXT, -- Фото хранится в photos/{user_id}/{telegram_photo_id}.png
);

-- Поддержка легаси код, нужно переделать
-- CREATE TABLE IF NOT EXISTS old_user_settings (
--     user_id INT REFERENCES users(id) UNIQUE,
--     notifications_enabled BOOLEAN DEFAULT TRUE,
--     notifications_mode TEXT,
--     notifications_time TEXT,
--     notifications_platforms TEXT[],
--     updated_at TIMESTAMPTZ DEFAULT now()
-- );

-- CREATE TABLE IF NOT EXISTS old_content_rules (
--     post_id INT PRIMARY KEY REFERENCES posts(id),
--     post JSONB NOT NULL,
--     story JSONB NOT NULL
-- );


CREATE TYPE profile_field AS ENUM (
    'name',
    'phone_number',
    'email',
    'photo_tg_code'
);

CREATE TABLE IF NOT EXISTS user_updates (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    field profile_field NOT NULL,
    old_value TEXT,
    new_value TEXT,
    action_time TIMESTAMPTZ DEFAULT now() 
)

CREATE INDEX idx_user_updates_user_id ON user_updates(user_id);
CREATE INDEX idx_user_updates_action_time ON user_updates(action_time);

CREATE TYPE content_type AS ENUM (
    'post',
    'story',
    'video'
);

CREATE TABLE IF NOT EXISTS user_downloads (
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    content content_type NOT NULL,
    selection_id INT REFERENCES selections(id) ON DELETE CASCADE,

    action_time TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_user_downloads_user_id ON user_downloads(user_id);
CREATE INDEX idx_user_downloads_selection_id ON user_downloads(selection_id);
CREATE INDEX idx_user_downloads_user_selection ON user_downloads(user_id, selection_id);