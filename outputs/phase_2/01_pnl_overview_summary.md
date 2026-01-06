# Phase 2: Financial Overview & Anomaly Flagging

Generated: 2026-01-06T00:14:07.852126

## Constraints Applied

- Diagnostic only
- No data modifications
- No root cause analysis
- No recommendations
- Negative values preserved as legitimate business activity

---

## 1. P&L Overview Summary

### Revenue (2018)

| Revenue Type | Amount | % of Total |
|--------------|--------|------------|
| Recurring | $68,584,167.00 | 86.6% |
| PSO | $9,307,488.20 | 11.8% |
| Perpetual | $1,302,828.30 | 1.6% |
| **TOTAL** | **$79,194,483.50** | **100.0%** |

### Expenses (2018)

| Expense Category | Amount | % of Total |
|------------------|--------|------------|
| HC (W2) | $30,544,905.60 | 42.3% |
| Non-HC OPEX | $27,170,629.50 | 37.6% |
| Non-HC COGS | $14,461,557.90 | 20.0% |
| **TOTAL** | **$72,177,093.00** | **100.0%** |

### Margin Analysis

| Metric | Value |
|--------|-------|
| Gross Margin | $7,017,390.50 |
| Gross Margin % | 8.86% |
| P&L Summary Margin | $7,017,390.50 |
| P&L Summary Margin % | 8.86% |

---

## 2. Reconciliation Checks

| Check | P&L Summary | Computed | Difference | Status |
|-------|-------------|----------|------------|--------|
| Recurring Revenue | $68,584,167.00 | $68,584,167.00 | $0.00 | ✓ RECONCILED |
| PSO Revenue | $9,307,488.20 | $9,307,488.20 | $0.00 | ✓ RECONCILED |
| Perpetual Revenue | $1,302,828.30 | $1,302,828.30 | $0.00 | ✓ RECONCILED |
| Total Revenue | $79,194,483.50 | $79,194,483.50 | $0.00 | ✓ RECONCILED |
| HC Expense (W2) | $30,544,905.60 | $30,544,905.60 | $0.00 | ✓ RECONCILED |
| Non HC Expense (OPEX) | $27,170,629.50 | $27,170,629.50 | $0.00 | ✓ RECONCILED |
| Non HC Expense (COGS) | $14,461,557.90 | $14,461,557.90 | $0.00 | ✓ RECONCILED |

**All reconciliation checks passed.** Computed values from detail sheets match P&L Summary within tolerance.

---

## 3. Negative Value Analysis

### Summary by Sheet

| Sheet | Total Rows | Negative Count | Negative Sum | % of Abs Total | Classification |
|-------|------------|----------------|--------------|----------------|----------------|
| OPEX - NEmpl. | 1890 | 321 | $-11,107,547.60 | 22.49% | Material |
| COGS - NEmpl. | 849 | 34 | $-671,685.80 | 4.25% | Systematic |
| Empl. | 458 | 21 | $-964,277.60 | 2.97% | Systematic |
| RecurringRevenue | 2112 | 6 | $-237,141.00 | 0.34% | Isolated |
| PSORevenue | 323 | 3 | $-165,811.60 | 1.72% | Isolated |
| PerpetualRevenue | 84 | 1 | $-83,406.30 | 5.68% | Isolated |

### Pattern Classification Criteria

- **Isolated**: One-off or immaterial negative values
- **Systematic**: Repeated within a category, function, or department (>10% of category)
- **Material**: Large enough to meaningfully affect margins (>10% of absolute total)

### Notable Concentrations

**OPEX - NEmpl.** (Material)
- Categories with concentrated negatives:
  - G&A: 286 items, $-8,429,793.10 (32.3%)
  - R&D: 6 items, $-1,365,580.30 (12.4%)
  - S&M: 29 items, $-1,312,174.20 (10.7%)
- Departments with concentrated negatives:
  - Occupancy: 13 items, $-3,903,486.30 (49.0%)
  - Benefits: 219 items, $-3,102,883.60 (50.0%)
  - Product Development: 6 items, $-1,365,580.30 (14.9%)
  - Finance & Accounting: 22 items, $-771,693.00 (19.7%)
  - GMs & Office Admins: 8 items, $-333,230.00 (20.7%)

**COGS - NEmpl.** (Systematic)
- Departments with concentrated negatives:
  - Customer Success: 7 items, $-247,959.50 (11.8%)

**Empl.** (Systematic)
- Departments with concentrated negatives:
  - Solution Consultants: 2 items, $-145,886.40 (11.6%)

---

## 4. Out-of-Model Signals

### OPEX - G&A

- **Observation**: G&A expense at 11.7% of revenue
- **Benchmark**: 9.0%
- **Actual**: 11.7%
- **Variance**: +2.7pp
- **Evidence**: OPEX G&A total: $9,258,384

### S&M

- **Observation**: S&M expense at 12.2% of revenue
- **Benchmark**: 6.0%
- **Actual**: 12.2%
- **Variance**: +6.2pp
- **Evidence**: OPEX S&M: $9,650,308

### Expense Mix

- **Observation**: Non-HC expense (57.7%) exceeds HC expense (42.3%)
- **Benchmark**: Typically HC > Non-HC for service businesses
- **Actual**: HC: 42.3%, Non-HC: 57.7%
- **Variance**: Non-HC exceeds HC by $11,087,282
- **Evidence**: HC: $30,544,906, Non-HC: $41,632,187

### Margin

- **Observation**: Gross margin at 8.9%, below benchmark
- **Benchmark**: 70.0%
- **Actual**: 8.9%
- **Variance**: -61.1pp
- **Evidence**: Margin: $7,017,390

### Revenue Mix

- **Observation**: Recurring revenue represents 86.6% of total
- **Benchmark**: N/A - Observation only
- **Actual**: Recurring: 86.6%
- **Variance**: High concentration in single revenue type
- **Evidence**: Recurring: $68,584,167

---

## 5. Flag Register Summary

See `02_flag_register.csv` for complete details.

| Flag ID | Area | Description | Materiality |
|---------|------|-------------|-------------|
| F-01 | OPEX - NEmpl. | Material concentration of negative adjustments (22.5% of abs... | High |
| F-02 | OPEX - NEmpl. - G&A | Systematic negative adjustments in G&A (32.3% of category)... | Medium |
| F-03 | OPEX - NEmpl. - R&D | Systematic negative adjustments in R&D (12.4% of category)... | Medium |
| F-04 | OPEX - NEmpl. - S&M | Systematic negative adjustments in S&M (10.7% of category)... | Medium |
| F-05 | OPEX - NEmpl. - Occupancy | Concentrated negative adjustments in Occupancy department (4... | Medium |
| F-06 | OPEX - NEmpl. - Benefits | Concentrated negative adjustments in Benefits department (50... | Medium |
| F-07 | OPEX - NEmpl. - Product Development | Concentrated negative adjustments in Product Development dep... | Medium |
| F-08 | COGS - NEmpl. | Systematic concentration of negative adjustments (4.2% of ab... | Medium |
| F-09 | COGS - NEmpl. - Customer Success | Concentrated negative adjustments in Customer Success depart... | Medium |
| F-10 | Empl. | Systematic concentration of negative adjustments (3.0% of ab... | Medium |
| F-11 | Empl. - Solution Consultants | Concentrated negative adjustments in Solution Consultants de... | Medium |
| F-12 | OPEX - G&A | G&A expense at 11.7% of revenue... | Medium |
| F-13 | S&M | S&M expense at 12.2% of revenue... | Medium |
| F-14 | Expense Mix | Non-HC expense (57.7%) exceeds HC expense (42.3%)... | High |
| F-15 | Margin | Gross margin at 8.9%, below benchmark... | High |
| F-16 | Revenue Mix | Recurring revenue represents 86.6% of total... | Medium |

**Total Flags: 16**
- High Materiality: 3
- Medium Materiality: 13

---

## 6. QC Confirmation

- ✓ All aggregates derived from normalized Phase 1 data
- ✓ No data values were altered
- ✓ No rows or columns were added or removed
- ✓ All calculations are reproducible from `03_supporting_aggregates.xlsx`

---

## Supporting Artifacts

1. `02_flag_register.csv` - Complete flag register with evidence
2. `03_supporting_aggregates.xlsx` - Detailed breakdowns:
   - Revenue by type
   - Expense by category
   - OPEX by function
   - COGS by function
   - HC by function
   - Negative values by sheet
   - Negative values by category
   - Benchmark reference

---

**Phase 2 complete. Financial overview and anomaly flags prepared. Awaiting SVP direction on which flags to investigate via Why-chain in Phase 3.**
