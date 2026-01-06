# Why #1: OPEX G&A Above Benchmark

**Question**: Why is OPEX G&A above benchmark (11.7% vs 9.0%), even if the absolute gap appears modest?

**Date**: 2026-01-06

---

## Summary Answer

The data shows that G&A OPEX at 11.7% of revenue ($9,258,384) exceeds the combined benchmark of 9.0% ($7,127,504) by 2.7 percentage points, representing an absolute variance of $2,130,881.

A contributing factor appears to be the composition of G&A expenses. The net G&A figure reflects $17,688,177 in gross positive entries, offset by $8,429,793 in negative adjustments. Without negative adjustments, G&A would represent 22.3% of revenue.

The G&A expense base is concentrated in a small number of expense categories, with Outsourced Services alone comprising 49.6% of the net G&A total.

---

## Evidence

### G&A Expense Summary

| Metric | Value |
|--------|-------|
| Total Revenue | $79,194,483.50 |
| G&A Benchmark (Shared Services 4.5% + Executive 4.5%) | 9.0% |
| G&A Benchmark Amount | $7,127,503.51 |
| **Actual G&A (Net)** | **$9,258,384.30** |
| **Actual G&A % of Revenue** | **11.69%** |
| Variance to Benchmark | +$2,130,880.79 (+2.69pp) |

### Gross vs Net Composition

| Component | Amount | Notes |
|-----------|--------|-------|
| Positive entries | $17,688,177.40 | Gross expense before adjustments |
| Negative entries | -$8,429,793.10 | Credits/adjustments |
| **Net G&A** | **$9,258,384.30** | Reported figure |

This is evidenced by: `OPEX - NEmpl.` sheet, `function_l2 = "G&A"`, `2018_total` column.

---

### G&A Breakdown by Expense Category

| Expense Category | Amount | % of G&A | % of Revenue |
|------------------|--------|----------|--------------|
| Outsourced Services | $4,593,361.70 | 49.6% | 5.8% |
| Hosting | $1,336,947.90 | 14.4% | 1.7% |
| T&E/Other | $1,152,754.90 | 12.5% | 1.5% |
| Personnel | $982,013.30 | 10.6% | 1.2% |
| External Contractors | $683,553.90 | 7.4% | 0.9% |
| Occupancy | $348,049.10 | 3.8% | 0.4% |
| Other (Bonus, Marketing, Commissions) | $161,703.50 | 1.7% | 0.2% |
| **Total** | **$9,258,384.30** | **100.0%** | **11.7%** |

This is evidenced by: `OPEX - NEmpl.` sheet, `expense_category` column, aggregated by `function_l2 = "G&A"`.

---

### G&A Breakdown by Department

| Department | Amount | % of G&A |
|------------|--------|----------|
| Corporate | $2,634,716.60 | 28.5% |
| Finance & Accounting | $2,371,403.80 | 25.6% |
| GMs & Office Admins | $939,473.60 | 10.1% |
| Legal | $803,779.90 | 8.7% |
| Enterprise Systems | $731,954.50 | 7.9% |
| Human Resources | $615,258.20 | 6.6% |
| Business Operations | $538,380.30 | 5.8% |
| Corporate Technology | $323,439.90 | 3.5% |
| Other departments | $300,062.10 | 3.2% |

This is evidenced by: `OPEX - NEmpl.` sheet, `department` column, aggregated by `function_l2 = "G&A"`.

---

### Top Spend Combinations (Department × Expense Category)

| Department | Expense Category | Amount | % of G&A |
|------------|------------------|--------|----------|
| Corporate | Outsourced Services | $1,979,795.10 | 21.4% |
| Finance & Accounting | Outsourced Services | $1,426,247.90 | 15.4% |
| Legal | Outsourced Services | $729,129.80 | 7.9% |
| Occupancy | T&E/Other | $684,550.30 | 7.4% |
| Finance & Accounting | External Contractors | $529,469.10 | 5.7% |

This is evidenced by: `OPEX - NEmpl.` sheet, cross-tabulation of `department` × `expense_category` for `function_l2 = "G&A"`.

---

### Negative Adjustment Concentration within G&A

| Area | Negative Sum | Count |
|------|--------------|-------|
| **By Department** | | |
| Occupancy | -$3,903,486.30 | 13 |
| Benefits | -$3,102,883.60 | 219 |
| Finance & Accounting | -$771,693.00 | 22 |
| **By Expense Category** | | |
| Occupancy | -$3,909,864.20 | 18 |
| Personnel | -$3,524,873.10 | 225 |
| T&E/Other | -$944,836.30 | 25 |

This is evidenced by: `OPEX - NEmpl.` sheet, `2018_total < 0` filtered by `function_l2 = "G&A"`.

---

## Observations (Descriptive Only)

1. The data shows that Outsourced Services represents nearly half (49.6%) of net G&A expense.

2. The data shows that Corporate and Finance & Accounting departments together account for 54.1% of G&A spend.

3. The data shows that significant negative adjustments ($8.4M) reduce what would otherwise be a 22.3% G&A expense ratio down to 11.7%.

4. The data shows that negative adjustments are concentrated in Occupancy (-$3.9M) and Personnel (-$3.5M) expense categories within G&A.

---

## Data Source Reference

- Sheet: `OPEX - NEmpl.`
- Filter: `function_l2 = "G&A"`
- Value Column: `2018_total`
- Row Count (G&A only): 1,071 entries

---

**Why #1 answered. Awaiting next SVP Why.**
