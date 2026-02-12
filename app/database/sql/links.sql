CREATE TYPE IF NOT EXISTS chat_tag AS ENUM (
    'project',
    'partner'
);

CREATE TYPE IF NOT EXISTS chat_type AS ENUM (
    'group',
    'channel',
    'bot'
);

CREATE TABLE IF NOT EXISTS chats (
    id SERIAL PRIMARY KEY,

    name TEXT NOT NULL,
    telegram_username TEXT,
    link TEXT NOT NULL,
    type chat_type NOT NULL
    tag chat_tag NOT NULL DEFAULT 'project',
    
    preview TEXT, --путь до файла
    main_color TEXT,
    border_color TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    position INTEGER,

    UNIQUE(link)
)

-- если нужно ограничивать доступ к разным чатам
CREATE TABLE user_chats (
    user_id INT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chat_id INT NOT NULL REFERENCES chats(id) ON DELETE CASCADE,

    PRIMARY KEY (user_id, chat_id)
);
