# Phase 1b: Type Normalization Proposal

Generated: 2026-01-05

**Status: PROPOSAL ONLY — Awaiting SVP Approval**

---

## Executive Summary

This document proposes explicit normalization rules for converting ingested data to appropriate types before financial analysis. All transformations are designed to be reversible and preserve data integrity.

**Key Finding**: The data is cleaner than anticipated. No complex parsing is required (no parentheses negatives, currency symbols, or text-encoded numbers). The primary normalization needs are:
1. Convert `object` dtype columns to `float64`
2. Apply optional rounding to address floating point precision artifacts
3. Optionally rename ambiguous columns for clarity

---

## Proposed Normalization Rules

### Rule 1: Numeric Type Conversion

**Scope**: All columns containing financial values

| Sheet | Column | Current dtype | Proposed dtype | Transformation |
|-------|--------|---------------|----------------|----------------|
| Benchmarks | benchmark | object | float64 | `pd.to_numeric()` |
| P&L Summary | 2018_total | object | float64 | `pd.to_numeric()` |
| OPEX - NEmpl. | 2018_total | object | float64 | `pd.to_numeric()` |
| COGS - NEmpl. | 2018_total | object | float64 | `pd.to_numeric()` |
| Empl. | 2018_total | object | float64 | `pd.to_numeric()` |
| RecurringRevenue | 2018_total | object | float64 | `pd.to_numeric()` |
| PSORevenue | 2018_total | object | float64 | `pd.to_numeric()` |
| PerpetualRevenue | 2018_total | object | float64 | `pd.to_numeric()` |
| Finance Roles | hourly_rate_usd | object | float64 | `pd.to_numeric()` |
| Finance Roles | annual_salary_usd | object | float64 | `pd.to_numeric()` |

**Implementation**:
```python
df['column'] = pd.to_numeric(df['column'], errors='coerce')
```

**Expected Impact**:
- Enables arithmetic operations (sum, mean, etc.)
- Enables aggregation by category
- No value changes expected (all values already parseable)

**Risk**: `errors='coerce'` will convert unparseable values to NaN. QC check required to verify no new NaNs introduced.

---

### Rule 2: Floating Point Precision Rounding (OPTIONAL)

**Scope**: Financial amount columns with precision artifacts

**Proposal**: Round to 2 decimal places for currency values

| Before | After |
|--------|-------|
| `15400.000000000002` | `15400.00` |
| `89138.09999999999` | `89138.10` |
| `922.4999999999999` | `922.50` |

**Implementation**:
```python
df['2018_total'] = df['2018_total'].round(2)
```

**Expected Impact**:
- Cleaner display values
- Potential minor rounding differences in totals (< $0.01 per row)
- Cumulative rounding impact on sheet totals: estimated < $1.00

**Risk**: Rounding introduces small discrepancies. Must validate that:
- Sheet-level totals remain within acceptable tolerance (±$1.00)
- P&L Summary totals can be reconciled

**Recommendation**: Apply rounding ONLY if explicitly approved. Financial analysis can proceed without rounding.

---

### Rule 3: Near-Zero Check Value Handling (OPTIONAL)

**Scope**: P&L Summary sheet only

**Observation**: Two rows contain near-zero values that appear to be spreadsheet validation formulas:
- `Expense Check`: -5.96e-08
- `NHC Check`: -6.71e-08

**Proposal Options**:

| Option | Description | Implementation |
|--------|-------------|----------------|
| A | Keep as-is | No change |
| B | Convert to exactly 0.00 | `df.loc[df['p_l_summary'].str.contains('Check'), '2018_total'] = 0.0` |
| C | Exclude from totals | Filter during aggregation |

**Recommendation**: Option A (keep as-is) for Phase 2 initial analysis. These values have no material impact on totals.

---

### Rule 4: Column Renaming for Clarity (OPTIONAL)

**Scope**: Duplicate column disambiguation

**Current State**:
- `dept` = Department/Team name
- `dept_1` = Expense sub-category

**Proposal**:

| Current | Proposed | Rationale |
|---------|----------|-----------|
| `dept` | `department` | Clearer semantic meaning |
| `dept_1` | `expense_category` | Describes actual content |

**Implementation**:
```python
df.rename(columns={'dept': 'department', 'dept_1': 'expense_category'}, inplace=True)
```

**Expected Impact**:
- Improved code readability
- Self-documenting column names
- No data value changes

**Recommendation**: Apply renaming if downstream analysis will reference these columns frequently.

---

### Rule 5: Preserve String Columns As-Is

**Scope**: All non-numeric columns

The following columns should remain as `object` (string) dtype:

| Column | Sheets | Reason |
|--------|--------|--------|
| category | Benchmarks, Empl. | Categorical label |
| p_l_summary | P&L Summary | Row descriptor |
| function_l1 | OPEX, COGS, Empl. | Hierarchical category |
| function_l2 | OPEX, COGS, Empl. | Hierarchical category |
| dept / department | OPEX, COGS | Department name |
| dept_1 / expense_category | OPEX, COGS | Expense type |
| vendor | OPEX, COGS | Vendor name (currently all null) |
| tier | Empl., Revenue sheets | Tier classification |
| type | Revenue sheets | Revenue type |
| customer_name | Revenue sheets | Customer identifier (currently all null) |
| name | Empl. | Employee name (currently all null) |
| title | Finance Roles | Role title |
| description | Finance Roles | Role description |

**No transformation required** for these columns.

---

## Columns Intentionally NOT Normalized

The following columns contain 100% null values and require no transformation:

| Sheet | Column | Notes |
|-------|--------|-------|
| OPEX - NEmpl. | vendor | Preserved for structural completeness |
| COGS - NEmpl. | vendor | Preserved for structural completeness |
| Empl. | name | Preserved for structural completeness |
| RecurringRevenue | customer_name | Preserved for structural completeness |
| PSORevenue | customer_name | Preserved for structural completeness |
| PerpetualRevenue | customer_name | Preserved for structural completeness |

---

## QC Expectations After Normalization

### Invariants (Must NOT Change)

| Check | Description | Validation Method |
|-------|-------------|-------------------|
| Row Counts | Total rows per sheet must remain identical | Compare `len(df)` before/after |
| Column Counts | Total columns per sheet must remain identical | Compare `len(df.columns)` before/after |
| Null Counts | NaN count per column must remain identical (for numeric conversion) | Compare `df.isnull().sum()` before/after |
| Value Preservation | No non-null values should become NaN | Check `new_nulls = after_nulls - before_nulls == 0` |

### Expected Changes

| Check | Description | Expected Outcome |
|-------|-------------|------------------|
| dtype | Numeric columns change from `object` to `float64` | 10 columns across all sheets |
| Sum Totals | Sheet-level sums should match (within floating point tolerance) | Difference < 1e-6 |

### Totals to Validate

Pre- and post-normalization sums for each sheet's `2018_total` column:

| Sheet | Pre-Normalization Sum | Post-Normalization Sum | Tolerance |
|-------|----------------------|------------------------|-----------|
| OPEX - NEmpl. | TBD | Must match | ±$0.01 |
| COGS - NEmpl. | TBD | Must match | ±$0.01 |
| Empl. | TBD | Must match | ±$0.01 |
| RecurringRevenue | TBD | Must match | ±$0.01 |
| PSORevenue | TBD | Must match | ±$0.01 |
| PerpetualRevenue | TBD | Must match | ±$0.01 |

### Reconciliation Against P&L Summary

After normalization, the following cross-sheet validations should be performed:

| P&L Summary Row | Computed From | Expected Match |
|-----------------|---------------|----------------|
| Revenue (Recurring) | `RecurringRevenue['2018_total'].sum()` | 68,584,167 |
| Revenue (PSO) | `PSORevenue['2018_total'].sum()` | 9,307,488.2 |
| Revenue (Perpetual) | `PerpetualRevenue['2018_total'].sum()` | 1,302,828.3 |
| Total Revenue | Sum of above | 79,194,483.5 |
| HC Expense (W2) | `Empl['2018_total'].sum()` | 30,544,905.6 |
| Non HC Expense (OPEX) | `OPEX['2018_total'].sum()` | 27,170,629.5 |
| Non HC Expense (COGS) | `COGS['2018_total'].sum()` | 14,461,557.9 |

---

## Proposed Implementation Sequence

1. **Create backup of ingested DataFrames** (in-memory copy)
2. **Apply Rule 1**: Convert numeric columns to float64
3. **Validate Invariants**: Row counts, null counts unchanged
4. **Validate Sums**: Pre/post sum comparison within tolerance
5. **Optional**: Apply Rule 2 (rounding) if approved
6. **Optional**: Apply Rule 4 (renaming) if approved
7. **Cross-validate**: Reconcile against P&L Summary values
8. **Generate QC Report**: Document all transformations and validation results

---

## Summary Table: Proposed Transformations

| Rule | Mandatory | Transformation | Impact |
|------|-----------|----------------|--------|
| 1 | **Yes** | Convert object → float64 | Enables numeric operations |
| 2 | No | Round to 2 decimals | Cleaner values, minor rounding |
| 3 | No | Handle check values | Cosmetic |
| 4 | No | Rename ambiguous columns | Clarity |
| 5 | **Yes** | Preserve string columns | No change |

---

## Approval Request

The following normalization actions require SVP approval:

- [ ] **Rule 1** (Mandatory): Convert numeric columns to float64
- [ ] **Rule 2** (Optional): Apply 2-decimal rounding
- [ ] **Rule 3** (Optional): Handle P&L Summary check values
- [ ] **Rule 4** (Optional): Rename duplicate columns for clarity

---

**Phase 1b analysis complete. Awaiting SVP approval to execute normalization rules.**
