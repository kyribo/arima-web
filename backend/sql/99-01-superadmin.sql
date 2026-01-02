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
    'superadmin_new@arima.com', 
    'superadmin_new', 
    '$2b$12$Qsf1auq/VaazXbO6WFcRTOfDJF4q9IVg8ENgQcVW4Hvav.q6gKXxi', -- Hash for: Admin123!
    'Super', 
    'Admin New', 
    'Superadmin', 
    TRUE, 
    FALSE,
    'System Administrator (Secondary)',
    'Earth'
) ON CONFLICT (email) DO NOTHING;
