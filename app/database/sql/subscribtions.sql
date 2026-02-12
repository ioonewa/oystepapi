CREATE TYPE currency AS ENUM (
    'RUB'
);
CREATE TABLE subscription_plans (
    code TEXT PRIMARY KEY,              -- free / trial / pro / lifetime
    name TEXT NOT NULL,
    description TEXT,

    price INT,                    -- NULL = бесплатно
    currency currency DEFAULT 'RUB',

    duration_days INT,                  -- NULL = lifetime
    downloads_limit INT,

    is_active BOOLEAN DEFAULT true
);


CREATE TYPE subscription_status AS ENUM (
    'active',
    'expired',
    'cancelled' -- Вмешательство из вне (Например нарушение правил)
);

CREATE TABLE subscriptions (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),

    plan_code TEXT NOT NULL REFERENCES subscription_plans(code),
    status subscription_status NOT NULL DEFAULT 'active',

    starts_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    ends_at TIMESTAMPTZ,                 -- NULL = lifetime

    auto_renew BOOLEAN NOT NULL DEFAULT TRUE,
    cancelled_at TIMESTAMPTZ,

    -- снапшот условий на момент покупки
    price INT,
    currency currency DEFAULT 'RUB',
    duration_days INT,
    downloads_limit INT,

    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX uniq_active_subscription_per_user
ON subscriptions (user_id)
WHERE status = 'active';


CREATE INDEX idx_subscriptions_user_active
    ON subscriptions (user_id)
    WHERE status = 'active';


CREATE TYPE payment_provider AS ENUM (
    'tochka_bank',
);

CREATE TYPE payment_status AS ENUM (
    'pending',
    'paid',
    'failed',
    'refunded'
);

CREATE TABLE payments (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    subscription_id BIGINT NOT NULL REFERENCES subscriptions(id),

    provider payment_provider NOT NULL,
    provider_payment_id TEXT,            -- invoice_id / charge_id

    amount INT NOT NULL,
    currency currency NOT NULL DEFAULT 'RUB',

    status payment_status NOT NULL DEFAULT 'pending',

    created_at TIMESTAMPTZ DEFAULT now(),
    paid_at TIMESTAMPTZ
);

CREATE INDEX idx_subscriptions_autorenew_due
ON subscriptions (ends_at)
WHERE status = 'active'
  AND auto_renew = true
  AND ends_at IS NOT NULL;


CREATE TABLE referral_links (
    id BIGSERIAL PRIMARY KEY,

    code TEXT UNIQUE NOT NULL,              -- ref_752021281 или promo_webinar_2026
    owner_id BIGINT REFERENCES users(id),   -- NULL = системная ссылка (вебинар)

    -- демо-подписка
    demo_plan_code TEXT REFERENCES subscription_plans(code),
    demo_duration_days INT,
    demo_downloads_limit INT,

    -- скидка на первую оплату
    discount_percent INT,                   -- 20 = -20%
    discount_duration_days INT,              -- обычно 30
    discount_once BOOLEAN DEFAULT true,

    max_uses INT,                            -- NULL = без лимита
    used_count INT NOT NULL DEFAULT 0,

    expires_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true,

    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE user_referrals (
    id BIGSERIAL PRIMARY KEY,

    referral_link_id BIGINT NOT NULL REFERENCES referral_links(id),
    sender_id BIGINT REFERENCES users(id),       -- NULL для системных ссылок
    recipient_id BIGINT UNIQUE NOT NULL REFERENCES users(id),

    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE user_discounts (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),

    referral_link_id BIGINT REFERENCES referral_links(id),

    percent INT NOT NULL,
    expires_at TIMESTAMPTZ,
    is_used BOOLEAN DEFAULT false,

    created_at TIMESTAMPTZ DEFAULT now()
);
