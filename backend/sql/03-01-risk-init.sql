-- Create Schema
CREATE SCHEMA IF NOT EXISTS riske;

-- Create Risk Events Table
CREATE TABLE IF NOT EXISTS riske.risk_events (
    id VARCHAR PRIMARY KEY,
    report_title VARCHAR NOT NULL,
    client_code VARCHAR NOT NULL,
    risk_description TEXT NOT NULL,
    severity VARCHAR NOT NULL,
    impact TEXT,
    action_taken TEXT,
    follow_up_plan TEXT,
    additional_notes TEXT,
    images JSONB DEFAULT '[]',
    status VARCHAR NOT NULL,
    date VARCHAR NOT NULL,
    time VARCHAR,
    
    maker VARCHAR,
    approver VARCHAR,
    
    created_by_id UUID REFERENCES auth.users(id),
    approved_by_id UUID REFERENCES auth.users(id),
    
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now(),
    resolved_at TIMESTAMPTZ
);

-- Create Risk Approvals Table
CREATE TABLE IF NOT EXISTS riske.risk_approvals (
    id VARCHAR PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT now(),
    action VARCHAR NOT NULL,
    status VARCHAR DEFAULT 'pending',
    payload JSONB DEFAULT '{}',
    target_incident_id VARCHAR,
    
    requested_by_id UUID REFERENCES auth.users(id),
    assessed_by_id UUID REFERENCES auth.users(id),
    
    note TEXT
);
