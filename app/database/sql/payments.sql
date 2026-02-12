
CREATE TYPE provider_type AS ENUM (
    'tochka_bank',
);

CREATE TYPE payment_status AS ENUM (
    'pending',
    'paid',
    'failed'
);

CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) NOT NULL,

    amount_rub NUMERIC(12,2) NOT NULL,
    subscription_id INT REFERENCES subscriptions(id) NOT NULL,
    status payment_status NOT NULL DEFAULT 'pending',
    
    provider provider_type DEFAULT 'tochka_bank',
    created_at TIMESTAMPTZ DEFAULT now()
)

CREATE INDEX idx_payments_user_id ON payments(user_id);
CREATE INDEX idx_payments_subscription_id ON payments(subscription_id);
CREATE INDEX idx_payments_created_at ON payments(created_at);