-- Script SQL para migrar dados para Railway PostgreSQL
-- Execute este script no Railway PostgreSQL Query Editor

-- 1. Criar tabela obrigacoes_com_data
CREATE TABLE IF NOT EXISTS obrigacoes_com_data (
    obligation_id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    notes TEXT,
    date DATE,
    jurisdiction_level VARCHAR(50),
    jurisdiction VARCHAR(200),
    state VARCHAR(10),
    county VARCHAR(100),
    city VARCHAR(100),
    category VARCHAR(100),
    frequency VARCHAR(50),
    sources JSONB
);

-- 2. Criar tabela obrigacoes_sem_data
CREATE TABLE IF NOT EXISTS obrigacoes_sem_data (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500),
    notes TEXT
);

-- 3. Inserir dados de exemplo (você pode adicionar mais dados aqui)
INSERT INTO obrigacoes_com_data (title, notes, date, jurisdiction_level, jurisdiction, state, county, city, category, frequency, sources) VALUES
('IRS Form 941 - Employer''s Quarterly Federal Tax Return (Q1)', 'Quarterly federal tax return for employers', '2025-04-30', 'federal', 'Internal Revenue Service', NULL, NULL, NULL, 'Tax Return', 'Quarterly', '[]'),
('IRS Form 1040-ES - Estimated Tax (Q1 installment)', 'First quarter estimated tax payment', '2025-04-15', 'federal', 'Internal Revenue Service', NULL, NULL, NULL, 'Tax Payment', 'Quarterly', '[]'),
('Florida Income Tax Withholding', 'Monthly state income tax withholding', '2025-04-30', 'state', 'Florida Department of Revenue', 'FL', NULL, NULL, 'Withholding', 'Monthly', '[]'),
('Florida Corporate Income Tax Return', 'Annual corporate income tax return', '2025-04-15', 'state', 'Florida Department of Revenue', 'FL', NULL, NULL, 'Tax Return', 'Annual', '[]'),
('Orange County Property Tax Assessment', 'Annual property tax assessment', '2025-04-30', 'county', 'Orange County Tax Assessor', 'FL', 'Orange', NULL, 'Property Tax', 'Annual', '[]'),
('Orlando Business License Renewal', 'Annual business license renewal', '2025-04-30', 'municipal', 'City of Orlando', 'FL', 'Orange', 'Orlando', 'Business License', 'Annual', '[]');

INSERT INTO obrigacoes_sem_data (title, notes) VALUES
('Federal Tax Compliance', 'Ensure compliance with all federal tax obligations'),
('State Tax Compliance', 'Ensure compliance with all state tax obligations'),
('County Tax Compliance', 'Ensure compliance with all county tax obligations'),
('Municipal Tax Compliance', 'Ensure compliance with all municipal tax obligations');

-- 4. Verificar se os dados foram inseridos
SELECT 'obrigacoes_com_data' as tabela, COUNT(*) as total FROM obrigacoes_com_data
UNION ALL
SELECT 'obrigacoes_sem_data' as tabela, COUNT(*) as total FROM obrigacoes_sem_data;
