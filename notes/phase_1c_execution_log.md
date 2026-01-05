# Phase 1c Execution Log

Generated: 2026-01-05T22:51:44.068441

## Approved Rules Applied

- ✓ Rule 1: Convert numeric columns to float64
- ✓ Rule 4: Rename dept → department, dept_1 → expense_category
- ✓ Rule 5: Preserve string columns as-is

## Not Applied (Not Approved)

- ✗ Rule 2: Rounding
- ✗ Rule 3: Check-value handling

## Execution Log

```
[2026-01-05 22:51:43] [INFO] ======================================================================
[2026-01-05 22:51:43] [INFO] PHASE 1c: EXECUTE APPROVED NORMALIZATION RULES
[2026-01-05 22:51:43] [INFO] ======================================================================
[2026-01-05 22:51:43] [INFO] 
[2026-01-05 22:51:43] [INFO] APPROVED RULES:
[2026-01-05 22:51:43] [INFO]   ✓ Rule 1: Convert numeric columns to float64
[2026-01-05 22:51:43] [INFO]   ✓ Rule 4: Rename dept → department, dept_1 → expense_category
[2026-01-05 22:51:43] [INFO]   ✓ Rule 5: Preserve string columns as-is
[2026-01-05 22:51:43] [INFO] 
[2026-01-05 22:51:43] [INFO] NOT APPROVED (NOT APPLIED):
[2026-01-05 22:51:43] [INFO]   ✗ Rule 2: Rounding
[2026-01-05 22:51:43] [INFO]   ✗ Rule 3: Check-value handling
[2026-01-05 22:51:43] [INFO] 
[2026-01-05 22:51:43] [INFO] --------------------------------------------------
[2026-01-05 22:51:43] [INFO] Processing: Input P&L File
[2026-01-05 22:51:43] [INFO] --------------------------------------------------
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: Benchmarks
[2026-01-05 22:51:43] [INFO] [Benchmarks] Rule 1: benchmark dtype object → float64
[2026-01-05 22:51:43] [INFO] [Benchmarks] Rule 5: Preserved 1 string columns as-is: ['category']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: P&L Summary
[2026-01-05 22:51:43] [INFO] [P&L Summary] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [P&L Summary] Rule 5: Preserved 1 string columns as-is: ['p_l_summary']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: OPEX - NEmpl.
[2026-01-05 22:51:43] [INFO] [OPEX - NEmpl.] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [OPEX - NEmpl.] Rule 4: Renamed 'dept' → 'department'
[2026-01-05 22:51:43] [INFO] [OPEX - NEmpl.] Rule 4: Renamed 'dept_1' → 'expense_category'
[2026-01-05 22:51:43] [INFO] [OPEX - NEmpl.] Rule 5: Preserved 5 string columns as-is: ['function_l1', 'function_l2', 'department', 'expense_category', 'vendor']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: COGS - NEmpl.
[2026-01-05 22:51:43] [INFO] [COGS - NEmpl.] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [COGS - NEmpl.] Rule 4: Renamed 'dept' → 'department'
[2026-01-05 22:51:43] [INFO] [COGS - NEmpl.] Rule 4: Renamed 'dept_1' → 'expense_category'
[2026-01-05 22:51:43] [INFO] [COGS - NEmpl.] Rule 5: Preserved 5 string columns as-is: ['function_l1', 'function_l2', 'department', 'expense_category', 'vendor']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: Empl.
[2026-01-05 22:51:43] [INFO] [Empl.] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [Empl.] Rule 4: Renamed 'dept' → 'department'
[2026-01-05 22:51:43] [INFO] [Empl.] Rule 5: Preserved 6 string columns as-is: ['tier', 'category', 'function_l1', 'function_l2', 'department', 'name']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: RecurringRevenue
[2026-01-05 22:51:43] [INFO] [RecurringRevenue] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [RecurringRevenue] Rule 5: Preserved 3 string columns as-is: ['tier', 'type', 'customer_name']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: PSORevenue
[2026-01-05 22:51:43] [INFO] [PSORevenue] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:43] [INFO] [PSORevenue] Rule 5: Preserved 3 string columns as-is: ['tier', 'type', 'customer_name']
[2026-01-05 22:51:43] [INFO] 
>>> Sheet: PerpetualRevenue
[2026-01-05 22:51:44] [INFO] [PerpetualRevenue] Rule 1: 2018_total dtype object → float64
[2026-01-05 22:51:44] [INFO] [PerpetualRevenue] Rule 5: Preserved 3 string columns as-is: ['tier', 'type', 'customer_name']
[2026-01-05 22:51:44] [INFO] 
--------------------------------------------------
[2026-01-05 22:51:44] [INFO] Processing: Central Finance Roles File
[2026-01-05 22:51:44] [INFO] --------------------------------------------------
[2026-01-05 22:51:44] [INFO] 
>>> Sheet: Finance Roles
[2026-01-05 22:51:44] [INFO] [Finance Roles] Rule 1: hourly_rate_usd dtype object → int64
[2026-01-05 22:51:44] [INFO] [Finance Roles] Rule 1: annual_salary_usd dtype object → int64
[2026-01-05 22:51:44] [INFO] [Finance Roles] Rule 5: Preserved 2 string columns as-is: ['title', 'description']
[2026-01-05 22:51:44] [INFO] 
======================================================================
[2026-01-05 22:51:44] [INFO] GENERATING QC OUTPUTS
[2026-01-05 22:51:44] [INFO] ======================================================================
[2026-01-05 22:51:44] [INFO] 
Saved: outputs/qc/08_post_normalization_dtype_summary.csv
[2026-01-05 22:51:44] [INFO] 
Columns with dtype changes: 10
[2026-01-05 22:51:44] [INFO] 
Saved: outputs/qc/09_pre_post_sum_reconciliation.csv
[2026-01-05 22:51:44] [INFO] 
Sum Reconciliation Results:
[2026-01-05 22:51:44] [INFO] 
Saved: outputs/qc/10_invariant_checks.csv
[2026-01-05 22:51:44] [INFO] 
======================================================================
[2026-01-05 22:51:44] [INFO] QC SUMMARY
[2026-01-05 22:51:44] [INFO] ======================================================================
[2026-01-05 22:51:44] [INFO] 
Invariant Checks: 57 total
[2026-01-05 22:51:44] [INFO]   PASS: 57
[2026-01-05 22:51:44] [INFO]   FAIL: 0
[2026-01-05 22:51:44] [INFO] 
Sum Reconciliation Checks: 10 total
[2026-01-05 22:51:44] [INFO]   PASS: 10
[2026-01-05 22:51:44] [INFO]   FAIL: 0
[2026-01-05 22:51:44] [INFO] 
======================================================================
[2026-01-05 22:51:44] [INFO] P&L SUMMARY CROSS-VALIDATION
[2026-01-05 22:51:44] [INFO] ======================================================================
[2026-01-05 22:51:44] [INFO] 
Saved: outputs/qc/11_pnl_cross_validation.csv
[2026-01-05 22:51:44] [INFO] 
P&L Cross-Validation Results:
[2026-01-05 22:51:44] [INFO] 
======================================================================
[2026-01-05 22:51:44] [INFO] PHASE 1c EXECUTION COMPLETE
[2026-01-05 22:51:44] [INFO] ======================================================================
[2026-01-05 22:51:44] [INFO] 
✓ ALL QC CHECKS PASSED
[2026-01-05 22:51:44] [INFO] ✓ Data is normalized and validated
[2026-01-05 22:51:44] [INFO] ✓ Ready for Phase 2
```

## QC Status

**All checks passed: True**
