-- Add access column regarding User Management Implementation
ALTER TABLE auth.users ADD COLUMN IF NOT EXISTS access JSONB DEFAULT '[]'::jsonb;
