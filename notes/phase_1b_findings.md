# Phase 1b Findings: Validation, Assumption Justification & Analysis

Generated: 2026-01-05

---

## 1. Header Detection Justification

### Overview

The ingestion script used a heuristic-based approach to detect header rows. The decision logic evaluated each row for:
- Non-null value density (>50% of columns populated)
- String vs numeric content ratio
- Presence of metadata markers (e.g., "IN USD", "Maintenance", "Perpetual")

### Sheet-by-Sheet Justification

#### Sheets with Header at Row 0 (No Metadata Prefix)

| Sheet | Row 0 Content | Justification |
|-------|---------------|---------------|
| Benchmarks | `['Category', 'Benchmark']` | Clear column labels, row 1 contains data (0.7) |
| P&L Summary | `['P&L Summary', '2018 Total']` | Clear column labels, row 1 contains data (Revenue, 79194483.5) |
| Finance Roles | `['Title', 'Description', 'Hourly Rate (USD)', 'Annual Salary (USD)']` | Clear column labels, row 1 contains data |

**Decision Basis**: Row 0 contained recognizable column headers with no metadata prefixes. Row 1 contained actual data values.

#### Sheets with Header at Row 1 (1 Metadata Row)

| Sheet | Row 0 Content | Row 1 Content | Justification |
|-------|---------------|---------------|---------------|
| OPEX - NEmpl. | `['IN USD', NaN, NaN, NaN, NaN, NaN]` | `['Function L1', 'Function L2', 'Dept', 'Dept', 'Vendor', '2018 total']` | Row 0 is currency indicator, not column labels |
| COGS - NEmpl. | `['IN USD', NaN, NaN, NaN, NaN, NaN]` | `['Function L1', 'Function L2', 'Dept', 'Dept', 'Vendor', '2018 total']` | Row 0 is currency indicator, not column labels |

**Decision Basis**: Row 0 contained only "IN USD" with NaN padding - a metadata marker indicating currency denomination. Row 1 contained actual column headers.

#### Sheets with Header at Row 2 (2 Metadata Rows)

| Sheet | Row 0 Content | Row 1 Content | Row 2 Content | Justification |
|-------|---------------|---------------|---------------|---------------|
| Empl. | `[NaN, NaN, NaN, NaN, NaN, NaN, NaN]` | `['IN USD', NaN, NaN, NaN, NaN, NaN, NaN]` | `['Tier', 'Category', 'Function L1', ...]` | Rows 0-1 are empty/metadata |
| RecurringRevenue | `['IN USD', NaN, NaN, NaN]` | `[NaN, NaN, NaN, NaN]` | `['Tier', 'Type', 'Customer Name', '2018 total']` | Rows 0-1 are metadata/empty |
| PSORevenue | `[NaN, 'IN USD', NaN, NaN]` | `[NaN, 'Maintenance', NaN, NaN]` | `['Tier', 'Type', 'Customer Name', '2018 total']` | Rows 0-1 contain sheet-type labels |
| PerpetualRevenue | `[NaN, 'IN USD', NaN, NaN]` | `[NaN, 'Perpetual', NaN, NaN]` | `['Tier', 'Type', 'Customer Name', '2018 total']` | Rows 0-1 contain sheet-type labels |

**Decision Basis**: Rows 0-1 contained metadata markers (empty rows, "IN USD", revenue type labels) that are not column headers. Row 2 contained the actual column headers.

### Rows Dropped Summary

| Sheet | Original Rows | Header Row | Rows Dropped | Drop Reason |
|-------|---------------|------------|--------------|-------------|
| Benchmarks | 11 | 0 | 0 | N/A |
| P&L Summary | 47 | 0 | 0 | N/A |
| OPEX - NEmpl. | 1892 | 1 | 1 | Row 0 (metadata: "IN USD") |
| COGS - NEmpl. | 851 | 1 | 1 | Row 0 (metadata: "IN USD") |
| Empl. | 461 | 2 | 2 | Rows 0-1 (empty + "IN USD") |
| RecurringRevenue | 2115 | 2 | 2 | Rows 0-1 (metadata) |
| PSORevenue | 326 | 2 | 2 | Rows 0-1 (metadata) |
| PerpetualRevenue | 87 | 2 | 2 | Rows 0-1 (metadata) |
| Finance Roles | 6 | 0 | 0 | N/A |

**Total rows dropped: 10 (all metadata/non-data rows)**

---

## 2. Duplicate Column Validation

### Affected Sheets

Two sheets contain duplicate column names:
- **OPEX - NEmpl.**: Column "Dept" appears at indices 2 and 3
- **COGS - NEmpl.**: Column "Dept" appears at indices 2 and 3

### Validation Results

| Sheet | Column Position | Renamed To | Unique Values | Semantic Meaning |
|-------|-----------------|------------|---------------|------------------|
| OPEX - NEmpl. | Index 2 (3rd col) | `dept` | 24 | Department/Team name |
| OPEX - NEmpl. | Index 3 (4th col) | `dept_1` | 11 | Expense sub-category |
| COGS - NEmpl. | Index 2 (3rd col) | `dept` | 8 | Department/Team name |
| COGS - NEmpl. | Index 3 (4th col) | `dept_1` | 9 | Expense sub-category |

### Value Comparison

| Sheet | Rows Where Values Differ | % Different |
|-------|--------------------------|-------------|
| OPEX - NEmpl. | 1,672 of 1,890 | 88.5% |
| COGS - NEmpl. | 849 of 849 | 100% |

### Example Differences

**OPEX - NEmpl.:**
| dept (col 3) | dept_1 (col 4) |
|--------------|----------------|
| Corporate Technology | Hosting |
| Enterprise Systems | T&E/Other |
| Finance & Accounting | Outsourced Services |
| GMs & Office Admins | Commissions |
| Occupancy | Occupancy |

**COGS - NEmpl.:**
| dept (col 3) | dept_1 (col 4) |
|--------------|----------------|
| Cloud Operations | External Contractors |
| Cloud Operations | Hosting |
| Customer Success | Bonus |
| Professional Services | T&E/Other |

### Conclusion

**The duplicate column handling is SAFE.** The two "Dept" columns contain semantically different information:
- **`dept`**: Represents the organizational department or team (e.g., "Finance & Accounting", "Cloud Operations")
- **`dept_1`**: Represents the expense type or sub-category (e.g., "Hosting", "Personnel", "Outsourced Services")

Renaming to `dept` and `dept_1` preserves all information. No data loss occurred.

**Recommendation**: Consider more descriptive names in Phase 2:
- `dept` → `department` or `org_unit`
- `dept_1` → `expense_category` or `cost_type`

---

## 3. Numeric-Like Value Detection

### Summary

All columns expected to contain numeric values (`2018_total`, `benchmark`, `hourly_rate_usd`, `annual_salary_usd`) were scanned for non-numeric patterns.

| Sheet | Column | Current dtype | Non-Numeric Patterns | Notes |
|-------|--------|---------------|---------------------|-------|
| Benchmarks | benchmark | object | None | All values parseable as float |
| P&L Summary | 2018_total | object | None | All values parseable as float |
| OPEX - NEmpl. | 2018_total | object | None | All values parseable as float |
| COGS - NEmpl. | 2018_total | object | None | All values parseable as float |
| Empl. | 2018_total | object | None | All values parseable as float |
| RecurringRevenue | 2018_total | object | None | All values parseable as float |
| PSORevenue | 2018_total | object | None | All values parseable as float |
| PerpetualRevenue | 2018_total | object | None | All values parseable as float |
| Finance Roles | hourly_rate_usd | object | None | All values parseable as float |
| Finance Roles | annual_salary_usd | object | None | All values parseable as float |

**Key Finding**: No problematic non-numeric patterns (parentheses negatives, currency symbols, hyphens, etc.) were detected. All numeric values are already in parseable numeric format.

### Why dtype is `object` Instead of `float64`

The `object` dtype occurs because:
1. Pandas infers dtype during read, and mixed int/float values sometimes result in object dtype
2. Some columns contain both integers and floats (e.g., `79194483.5` vs `68584167`)

This is not an error - it simply requires explicit type conversion.

### Floating Point Precision Issues

Several sheets contain values with floating point precision artifacts:

| Sheet | Example Values | Likely Intended Value |
|-------|----------------|----------------------|
| Empl. | `15400.000000000002` | 15400.00 |
| Empl. | `110000.00000000001` | 110000.00 |
| PerpetualRevenue | `89138.09999999999` | 89138.10 |
| PerpetualRevenue | `922.4999999999999` | 922.50 |
| PSORevenue | `181313.59999999998` | 181313.60 |

**Cause**: Standard IEEE 754 floating point representation limitations in source Excel file or during read.

### Negative Values Analysis

Legitimate negative values exist in the data (credits, reversals, adjustments):

| Sheet | Negative Count | Total Count | Sum of Negatives |
|-------|----------------|-------------|------------------|
| P&L Summary | 2 | 35 | ~0 (rounding check values) |
| OPEX - NEmpl. | 321 | 1,890 | -11,107,547.60 |
| COGS - NEmpl. | 34 | 849 | -671,685.80 |
| Empl. | 21 | 458 | -964,277.60 |
| RecurringRevenue | 6 | 2,112 | -237,141.00 |
| PSORevenue | 3 | 323 | -165,811.60 |
| PerpetualRevenue | 1 | 84 | -83,406.30 |

**These negative values appear intentional** (expense credits, revenue reversals, etc.) and should be preserved.

---

## 4. Data Quality Observations

### Null Columns (100% Null Rate)

| Sheet | Column | Interpretation |
|-------|--------|----------------|
| OPEX - NEmpl. | vendor | No vendor data captured |
| COGS - NEmpl. | vendor | No vendor data captured |
| Empl. | name | Employee names redacted/not captured |
| RecurringRevenue | customer_name | Customer names redacted/not captured |
| PSORevenue | customer_name | Customer names redacted/not captured |
| PerpetualRevenue | customer_name | Customer names redacted/not captured |

**Note**: These columns are structurally present but contain no data. This may be intentional (privacy/redaction) or indicate incomplete source data.

### P&L Summary Check Values

Two rows in P&L Summary contain near-zero values labeled as "checks":
- `Expense Check`: -5.96e-08 (effectively 0)
- `NHC Check`: -6.71e-08 (effectively 0)

These appear to be validation formulas from the source spreadsheet and should be treated as zero or excluded from financial totals.

---

## 5. Assumptions Made (Explicit Log)

1. **Header Detection**: Rows containing only "IN USD" or similar metadata were excluded as non-data rows
2. **Duplicate Columns**: Two columns with identical original names ("Dept") were differentiated by suffix (`_1`)
3. **Negative Values**: All negative values were preserved as-is (assumed intentional)
4. **Floating Point**: No rounding was applied during ingestion; precision artifacts preserved
5. **Null Columns**: 100% null columns were preserved structurally (not dropped)
6. **P&L Check Rows**: Near-zero "check" values were preserved (not filtered)

---

## References

- `outputs/qc/01_sheet_ingestion_summary.csv` - Row count reconciliation
- `outputs/qc/02_column_name_mapping.csv` - Column name transformations
- `outputs/qc/05_duplicate_column_validation.csv` - Duplicate column analysis
- `outputs/qc/06_numeric_pattern_summary.csv` - Numeric pattern scan results
