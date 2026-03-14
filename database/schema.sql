-- Anti-Gravity Bug Bounty Platform - Database Schema
-- Database: PostgreSQL (Supabase)
-- Version: 1.0.0

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- USERS & AUTHENTICATION
-- =====================================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    wallet_address VARCHAR(42) UNIQUE NOT NULL,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(255),
    role VARCHAR(20) NOT NULL DEFAULT 'researcher', -- researcher, project_owner, validator
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    profile_metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_users_wallet ON users(wallet_address);
CREATE INDEX idx_users_role ON users(role);

-- =====================================================
-- REPUTATION SYSTEM
-- =====================================================

CREATE TABLE reputation_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    wallet_address VARCHAR(42) NOT NULL,
    trust_score DECIMAL(5,2) DEFAULT 50.00 CHECK (trust_score >= 0 AND trust_score <= 100),
    total_submissions INTEGER DEFAULT 0,
    validated_bugs INTEGER DEFAULT 0,
    rejected_bugs INTEGER DEFAULT 0,
    spam_reports INTEGER DEFAULT 0,
    total_earnings DECIMAL(20,8) DEFAULT 0,
    success_rate DECIMAL(5,2) GENERATED ALWAYS AS (
        CASE 
            WHEN total_submissions > 0 
            THEN (validated_bugs::DECIMAL / total_submissions::DECIMAL * 100)
            ELSE 0 
        END
    ) STORED,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id)
);

CREATE INDEX idx_reputation_wallet ON reputation_scores(wallet_address);
CREATE INDEX idx_reputation_trust_score ON reputation_scores(trust_score DESC);

-- =====================================================
-- PROJECTS & BOUNTY PROGRAMS
-- =====================================================

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    owner_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    website_url VARCHAR(500),
    github_url VARCHAR(500),
    contract_address VARCHAR(42), -- Smart contract vault address
    total_bounty_pool DECIMAL(20,8) DEFAULT 0,
    available_bounty DECIMAL(20,8) DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_active ON projects(is_active);

-- Bounty tiers for different severity levels
CREATE TABLE bounty_tiers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    severity VARCHAR(20) NOT NULL, -- critical, high, medium, low, info
    min_payout DECIMAL(20,8) NOT NULL,
    max_payout DECIMAL(20,8) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, severity)
);

-- =====================================================
-- BUG REPORTS
-- =====================================================

CREATE TABLE bug_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    researcher_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Report Details
    title VARCHAR(500) NOT NULL,
    description TEXT NOT NULL,
    steps_to_reproduce TEXT,
    impact_analysis TEXT,
    
    -- AI Classification
    owasp_category VARCHAR(100), -- A01:2021-Broken Access Control, etc.
    cvss_score DECIMAL(3,1) CHECK (cvss_score >= 0 AND cvss_score <= 10),
    cvss_vector VARCHAR(200),
    severity VARCHAR(20), -- critical, high, medium, low, info
    ai_confidence DECIMAL(5,2), -- AI model confidence (0-100)
    is_spam BOOLEAN DEFAULT FALSE,
    spam_score DECIMAL(5,2), -- Spam detection score (0-100)
    
    -- Status & Workflow
    status VARCHAR(50) DEFAULT 'pending_triage', 
    -- pending_triage, ai_validated, human_review, accepted, rejected, duplicate, fixed, paid
    
    -- Evidence & Proof
    ipfs_hash VARCHAR(100), -- IPFS CID for evidence files
    proof_of_concept_url VARCHAR(500),
    
    -- Validation & Payment
    validator_id UUID REFERENCES users(id),
    validated_at TIMESTAMP WITH TIME ZONE,
    bounty_amount DECIMAL(20,8),
    transaction_hash VARCHAR(66), -- Blockchain transaction hash
    paid_at TIMESTAMP WITH TIME ZONE,
    
    -- Timestamps
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_bugs_project ON bug_reports(project_id);
CREATE INDEX idx_bugs_researcher ON bug_reports(researcher_id);
CREATE INDEX idx_bugs_status ON bug_reports(status);
CREATE INDEX idx_bugs_severity ON bug_reports(severity);
CREATE INDEX idx_bugs_submitted ON bug_reports(submitted_at DESC);

-- =====================================================
-- AI PROCESSING LOGS
-- =====================================================

CREATE TABLE ai_processing_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bug_report_id UUID NOT NULL REFERENCES bug_reports(id) ON DELETE CASCADE,
    model_version VARCHAR(50) NOT NULL,
    processing_time_ms INTEGER,
    
    -- Classification Results
    owasp_predictions JSONB, -- Array of predictions with confidence scores
    cvss_breakdown JSONB, -- Detailed CVSS metrics
    spam_analysis JSONB, -- Spam detection details
    
    -- Model Outputs
    raw_model_output JSONB,
    
    processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_ai_logs_bug ON ai_processing_logs(bug_report_id);

-- =====================================================
-- BLOCKCHAIN TRANSACTIONS
-- =====================================================

CREATE TABLE bounty_transactions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    bug_report_id UUID NOT NULL REFERENCES bug_reports(id) ON DELETE CASCADE,
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    researcher_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Transaction Details
    transaction_hash VARCHAR(66) UNIQUE NOT NULL,
    from_address VARCHAR(42) NOT NULL, -- Smart contract address
    to_address VARCHAR(42) NOT NULL, -- Researcher wallet
    amount DECIMAL(20,8) NOT NULL,
    token_symbol VARCHAR(10) DEFAULT 'MATIC',
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, confirmed, failed
    block_number BIGINT,
    gas_used BIGINT,
    
    -- Timestamps
    initiated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    confirmed_at TIMESTAMP WITH TIME ZONE,
    
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_transactions_bug ON bounty_transactions(bug_report_id);
CREATE INDEX idx_transactions_researcher ON bounty_transactions(researcher_id);
CREATE INDEX idx_transactions_hash ON bounty_transactions(transaction_hash);

-- =====================================================
-- REPUTATION HISTORY (Audit Trail)
-- =====================================================

CREATE TABLE reputation_events (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    bug_report_id UUID REFERENCES bug_reports(id) ON DELETE SET NULL,
    
    event_type VARCHAR(50) NOT NULL, -- bug_validated, bug_rejected, spam_detected, etc.
    score_delta DECIMAL(5,2) NOT NULL, -- Change in trust score
    previous_score DECIMAL(5,2),
    new_score DECIMAL(5,2),
    
    reason TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_reputation_events_user ON reputation_events(user_id);
CREATE INDEX idx_reputation_events_created ON reputation_events(created_at DESC);

-- =====================================================
-- NOTIFICATIONS
-- =====================================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    type VARCHAR(50) NOT NULL, -- bug_validated, payment_sent, status_update, etc.
    title VARCHAR(255) NOT NULL,
    message TEXT,
    
    related_bug_id UUID REFERENCES bug_reports(id) ON DELETE SET NULL,
    related_project_id UUID REFERENCES projects(id) ON DELETE SET NULL,
    
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read) WHERE is_read = FALSE;

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_bug_reports_updated_at BEFORE UPDATE ON bug_reports
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- VIEWS FOR ANALYTICS
-- =====================================================

-- Researcher leaderboard
CREATE VIEW researcher_leaderboard AS
SELECT 
    u.id,
    u.wallet_address,
    u.username,
    r.trust_score,
    r.validated_bugs,
    r.total_submissions,
    r.success_rate,
    r.total_earnings,
    RANK() OVER (ORDER BY r.trust_score DESC, r.validated_bugs DESC) as rank
FROM users u
JOIN reputation_scores r ON u.id = r.user_id
WHERE u.role = 'researcher' AND u.is_active = TRUE
ORDER BY r.trust_score DESC, r.validated_bugs DESC;

-- Project statistics
CREATE VIEW project_statistics AS
SELECT 
    p.id,
    p.name,
    COUNT(DISTINCT b.id) as total_reports,
    COUNT(DISTINCT CASE WHEN b.status = 'accepted' THEN b.id END) as accepted_reports,
    COUNT(DISTINCT b.researcher_id) as unique_researchers,
    SUM(CASE WHEN b.status = 'paid' THEN b.bounty_amount ELSE 0 END) as total_paid,
    p.available_bounty,
    AVG(CASE WHEN b.cvss_score IS NOT NULL THEN b.cvss_score END) as avg_severity
FROM projects p
LEFT JOIN bug_reports b ON p.id = b.project_id
GROUP BY p.id, p.name, p.available_bounty;

-- =====================================================
-- SAMPLE DATA (Optional - for testing)
-- =====================================================

-- Insert sample OWASP categories for reference
CREATE TABLE owasp_categories (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    year INTEGER DEFAULT 2021
);

INSERT INTO owasp_categories (code, name, description) VALUES
('A01:2021', 'Broken Access Control', 'Restrictions on what authenticated users are allowed to do are often not properly enforced'),
('A02:2021', 'Cryptographic Failures', 'Failures related to cryptography which often lead to exposure of sensitive data'),
('A03:2021', 'Injection', 'User-supplied data is not validated, filtered, or sanitized by the application'),
('A04:2021', 'Insecure Design', 'Missing or ineffective control design'),
('A05:2021', 'Security Misconfiguration', 'Missing appropriate security hardening or improperly configured permissions'),
('A06:2021', 'Vulnerable and Outdated Components', 'Using components with known vulnerabilities'),
('A07:2021', 'Identification and Authentication Failures', 'Confirmation of the user identity, authentication, and session management'),
('A08:2021', 'Software and Data Integrity Failures', 'Code and infrastructure that does not protect against integrity violations'),
('A09:2021', 'Security Logging and Monitoring Failures', 'Insufficient logging and monitoring'),
('A10:2021', 'Server-Side Request Forgery (SSRF)', 'Fetching a remote resource without validating the user-supplied URL');

-- =====================================================
-- ROW LEVEL SECURITY (RLS) - For Supabase
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE reputation_scores ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE bug_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

-- Example policies (customize based on your auth setup)
-- Users can read their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid()::text = id::text);

-- Researchers can view their own bug reports
CREATE POLICY "Researchers can view own reports" ON bug_reports
    FOR SELECT USING (auth.uid()::text = researcher_id::text);

-- Project owners can view reports for their projects
CREATE POLICY "Owners can view project reports" ON bug_reports
    FOR SELECT USING (
        EXISTS (
            SELECT 1 FROM projects 
            WHERE projects.id = bug_reports.project_id 
            AND projects.owner_id::text = auth.uid()::text
        )
    );
