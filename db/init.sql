-- OpenClaw Production Database Initialization
-- PostgreSQL 15

-- Create extensions
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS btree_gin;
CREATE EXTENSION IF NOT EXISTS btree_gist;

-- Create schema
CREATE SCHEMA IF NOT EXISTS openclaw;

-- Tables for sessions
CREATE TABLE IF NOT EXISTS openclaw.sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    agent_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB DEFAULT '{}'::jsonb,
    status VARCHAR(50) DEFAULT 'active'
);

-- Table for messages
CREATE TABLE IF NOT EXISTS openclaw.messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES openclaw.sessions(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL, -- 'user' or 'assistant'
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table for agents
CREATE TABLE IF NOT EXISTS openclaw.agents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    config JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table for workflows
CREATE TABLE IF NOT EXISTS openclaw.workflows (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    config JSONB NOT NULL,
    created_by VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table for audit logs
CREATE TABLE IF NOT EXISTS openclaw.audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    action VARCHAR(255) NOT NULL,
    entity_type VARCHAR(50),
    entity_id UUID,
    user_id VARCHAR(255),
    details JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_sessions_user_id ON openclaw.sessions(user_id);
CREATE INDEX idx_sessions_agent_name ON openclaw.sessions(agent_name);
CREATE INDEX idx_sessions_created_at ON openclaw.sessions(created_at);
CREATE INDEX idx_messages_session_id ON openclaw.messages(session_id);
CREATE INDEX idx_messages_created_at ON openclaw.messages(created_at);
CREATE INDEX idx_agents_name ON openclaw.agents(name);
CREATE INDEX idx_agents_status ON openclaw.agents(status);
CREATE INDEX idx_workflows_status ON openclaw.workflows(status);
CREATE INDEX idx_audit_logs_created_at ON openclaw.audit_logs(created_at);
CREATE INDEX idx_audit_logs_user_id ON openclaw.audit_logs(user_id);

-- Insert default agents
INSERT INTO openclaw.agents (name, type, status, config) VALUES
    ('main', 'gemini_chat', 'active', '{"model": "gemini-1.5-pro", "provider": "pickaxe"}'),
    ('video', 'video_processor', 'active', '{"service": "video_agent"}'),
    ('marketing', 'marketing_generator', 'active', '{"service": "marketing_generator"}'),
    ('shopify', 'shopify_integration', 'active', '{"service": "shopify_integration"}')
ON CONFLICT DO NOTHING;

-- Grants
GRANT ALL PRIVILEGES ON SCHEMA openclaw TO openclaw_admin;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA openclaw TO openclaw_admin;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA openclaw TO openclaw_admin;
