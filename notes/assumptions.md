# Phase 1 Ingestion Assumptions

Generated: 2026-01-05T21:16:08.485534

## Header Detection Assumptions

- [Input P&L][OPEX - NEmpl.] Rows 0-0 treated as metadata/non-data rows
- [Input P&L][COGS - NEmpl.] Rows 0-0 treated as metadata/non-data rows
- [Input P&L][Empl.] Rows 0-1 treated as metadata/non-data rows
- [Input P&L][RecurringRevenue] Rows 0-1 treated as metadata/non-data rows
- [Input P&L][PSORevenue] Rows 0-1 treated as metadata/non-data rows
- [Input P&L][PerpetualRevenue] Rows 0-1 treated as metadata/non-data rows

## General Assumptions

- Column names with special characters, spaces, or parentheses were normalized to snake_case
- Duplicate column names within a sheet were made unique by appending numeric suffixes
- Empty/NaN column headers were renamed to "unnamed" (with suffixes for duplicates)
- No rows were filtered based on data content; only structural non-data rows were excluded
- Original data files were NOT modified

## Data Integrity Notes

- All numeric values preserved as-is (no rounding or transformation applied)
- All string values preserved as-is (no trimming or case conversion on data)
- Null values preserved as pandas NaN

## QC Artifacts Generated

1. `outputs/qc/01_sheet_ingestion_summary.csv` - Per-sheet row counts and header detection
2. `outputs/qc/02_column_name_mapping.csv` - Original to normalized column name mapping
3. `outputs/qc/03_null_rate_summary.csv` - Null rate per column per sheet
4. `outputs/qc/04_data_type_summary.csv` - Data types detected per column
