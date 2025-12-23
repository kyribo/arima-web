-- Password is: Admin123!
INSERT INTO auth.users (
    email, 
    username, 
    hashed_password, 
    first_name, 
    last_name, 
    role, 
    is_active, 
    is_2fa_enabled,
    bio,
    location
) VALUES (
    'admin@arima.com', 
    'superadmin', 
    '$2b$12$L7Wc.6QxX2/UvB/lRjQ.u.Y/v/k/k/k/k/k/k/k/k/k/k/k/k/k/k', -- Hash for: Admin123!
    'Super', 
    'Admin', 
    'Superadmin', 
    TRUE, 
    FALSE,
    'System Administrator',
    'Earth'
) ON CONFLICT (email) DO NOTHING;
