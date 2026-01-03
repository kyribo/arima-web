-- Rename risk_event.view to risk_event.read in user access arrays
UPDATE auth.users
SET access = array_replace(access, 'risk_event.view', 'risk_event.read')
WHERE 'risk_event.view' = ANY(access);
