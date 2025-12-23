CREATE TABLE IF NOT EXISTS auth.user_secrets (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    totp_secret VARCHAR(255),
    backup_codes JSONB,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
