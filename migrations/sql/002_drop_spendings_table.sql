-- Migration: Drop spendings table
-- Description: Drops the spendings table (use with caution - this will delete all data)
-- Created: 2025-11-29

-- Drop indexes first
DROP INDEX IF EXISTS idx_spendings_date;
DROP INDEX IF EXISTS idx_spendings_category;
DROP INDEX IF EXISTS idx_spendings_id;

-- Drop the table
DROP TABLE IF EXISTS spendings;

