# Database Migrations

This directory contains SQL migration scripts for the Budget Tracker database.

## Migration Scripts

### 001_create_spendings_table.sql
Creates the `spendings` table with the following structure:
- `id` (UUID, Primary Key) - Unique identifier
- `amount` (FLOAT, NOT NULL) - Amount spent
- `category` (VARCHAR, NOT NULL) - Spending category
- `description` (VARCHAR, NULLABLE) - Optional description
- `date` (TIMESTAMP, NOT NULL) - Date of spending
- `created_at` (TIMESTAMP, NOT NULL) - Record creation timestamp

The script also creates indexes on `id`, `category`, and `date` for better query performance.

### 002_drop_spendings_table.sql
Drops the `spendings` table and its indexes. **Use with caution** - this will delete all data.

## Running Migrations

### Using psql (PostgreSQL command line):
```bash
psql -h localhost -U your_username -d budget_tracker -f migrations/sql/001_create_spendings_table.sql
```

### Using environment variables:
```bash
export PGHOST=localhost
export PGUSER=your_username
export PGDATABASE=budget_tracker
psql -f migrations/sql/001_create_spendings_table.sql
```

### Using connection string:
```bash
psql "postgresql://user:password@localhost:5432/budget_tracker" -f migrations/sql/001_create_spendings_table.sql
```

### 003_insert_mock_spendings.sql
Insert needed data for mock spendings log

## Notes

- The migration scripts use `IF NOT EXISTS` and `IF EXISTS` clauses to make them idempotent
- The UUID extension is automatically enabled if not already present
- Indexes are created to optimize common query patterns (filtering by category and date)

