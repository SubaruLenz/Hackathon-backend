-- Migration: Create spendings table
-- Description: Creates the spendings table for logging budget tracker spendings
-- Created: 2025-11-29

-- Enable UUID extension (if not already enabled)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create spendings table
CREATE TABLE IF NOT EXISTS spendings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    amount FLOAT NOT NULL,
    category VARCHAR NOT NULL,
    description VARCHAR,
    date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_spendings_id ON spendings(id);
CREATE INDEX IF NOT EXISTS idx_spendings_category ON spendings(category);
CREATE INDEX IF NOT EXISTS idx_spendings_date ON spendings(date);

-- Add comments to table and columns for documentation
COMMENT ON TABLE spendings IS 'Table for storing spending entries in the budget tracker';
COMMENT ON COLUMN spendings.id IS 'Unique identifier for the spending entry (UUID)';
COMMENT ON COLUMN spendings.amount IS 'Amount spent (must be positive)';
COMMENT ON COLUMN spendings.category IS 'Category of the spending (e.g., Food, Transport, Entertainment)';
COMMENT ON COLUMN spendings.description IS 'Optional description of the spending';
COMMENT ON COLUMN spendings.date IS 'Date when the spending occurred';
COMMENT ON COLUMN spendings.created_at IS 'Timestamp when the spending record was created';

