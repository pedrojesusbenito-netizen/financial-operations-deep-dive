#!/usr/bin/env python3
"""
Phase 1c: Execute Approved Normalization Rules + QC

SVP AUTHORIZATION:
✓ Rule 1: Convert approved numeric columns from object to float64
✓ Rule 4: Rename columns (dept → department, dept_1 → expense_category)
✓ Rule 5: Preserve all string columns as-is

EXPLICITLY NOT APPROVED:
✗ Rule 2 (rounding) - NOT APPLIED
✗ Rule 3 (check-value handling) - NOT APPLIED

Author: Phase 1c Execution
Date: 2026-01-05
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
from typing import Dict, List, Tuple

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_PL_FILE = "data/Operational Leadership Real Work - Input P&L.xlsx"
CENTRAL_FINANCE_FILE = "data/Central Finance Roles.xlsx"
QC_OUTPUT_DIR = "outputs/qc"

# Header row positions (from Phase 1)
HEADER_ROWS = {
    "Benchmarks": 0,
    "P&L Summary": 0,
    "OPEX - NEmpl.": 1,
    "COGS - NEmpl.": 1,
    "Empl.": 2,
    "RecurringRevenue": 2,
    "PSORevenue": 2,
    "PerpetualRevenue": 2,
    "Finance Roles": 0
}

# Column normalization mapping (from Phase 1)
COLUMN_NORMALIZATIONS = {
    "Benchmarks": ["category", "benchmark"],
    "P&L Summary": ["p_l_summary", "2018_total"],
    "OPEX - NEmpl.": ["function_l1", "function_l2", "dept", "dept_1", "vendor", "2018_total"],
    "COGS - NEmpl.": ["function_l1", "function_l2", "dept", "dept_1", "vendor", "2018_total"],
    "Empl.": ["tier", "category", "function_l1", "function_l2", "dept", "name", "2018_total"],
    "RecurringRevenue": ["tier", "type", "customer_name", "2018_total"],
    "PSORevenue": ["tier", "type", "customer_name", "2018_total"],
    "PerpetualRevenue": ["tier", "type", "customer_name", "2018_total"],
    "Finance Roles": ["title", "description", "hourly_rate_usd", "annual_salary_usd"]
}

# APPROVED: Columns to convert to float64 (Rule 1)
NUMERIC_COLUMNS = {
    "Benchmarks": ["benchmark"],
    "P&L Summary": ["2018_total"],
    "OPEX - NEmpl.": ["2018_total"],
    "COGS - NEmpl.": ["2018_total"],
    "Empl.": ["2018_total"],
    "RecurringRevenue": ["2018_total"],
    "PSORevenue": ["2018_total"],
    "PerpetualRevenue": ["2018_total"],
    "Finance Roles": ["hourly_rate_usd", "annual_salary_usd"]
}

# APPROVED: Column renaming (Rule 4)
COLUMN_RENAMES = {
    "dept": "department",
    "dept_1": "expense_category"
}

# =============================================================================
# EXECUTION LOG
# =============================================================================

execution_log = []

def log(message: str, level: str = "INFO"):
    """Log a message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [{level}] {message}"
    execution_log.append(entry)
    print(entry)

# =============================================================================
# INGESTION (Reuse Phase 1 Logic)
# =============================================================================

def ingest_sheet(xl: pd.ExcelFile, sheet_name: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Ingest a single sheet and return normalized DataFrame with pre-normalization metrics.
    """
    header_row = HEADER_ROWS[sheet_name]
    columns = COLUMN_NORMALIZATIONS[sheet_name]

    # Read raw data
    df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None)

    # Extract data starting after header
    df = df_raw.iloc[header_row + 1:].copy()
    df.columns = columns
    df = df.reset_index(drop=True)

    # Capture pre-normalization metrics
    pre_metrics = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "null_counts": {col: int(df[col].isnull().sum()) for col in df.columns},
        "sums": {}
    }

    # Calculate pre-normalization sums for numeric columns
    for col in NUMERIC_COLUMNS.get(sheet_name, []):
        if col in df.columns:
            numeric_vals = pd.to_numeric(df[col], errors='coerce')
            pre_metrics["sums"][col] = float(numeric_vals.sum())

    return df, pre_metrics

# =============================================================================
# NORMALIZATION (Approved Rules Only)
# =============================================================================

def apply_rule_1(df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
    """
    APPROVED Rule 1: Convert numeric columns from object to float64.
    NO ROUNDING APPLIED (Rule 2 not approved).
    """
    numeric_cols = NUMERIC_COLUMNS.get(sheet_name, [])

    for col in numeric_cols:
        if col in df.columns:
            original_dtype = str(df[col].dtype)
            original_nulls = df[col].isnull().sum()

            # Convert to numeric
            df[col] = pd.to_numeric(df[col], errors='coerce')

            new_dtype = str(df[col].dtype)
            new_nulls = df[col].isnull().sum()

            log(f"[{sheet_name}] Rule 1: {col} dtype {original_dtype} → {new_dtype}")

            # Verify no new nulls introduced
            if new_nulls > original_nulls:
                log(f"[{sheet_name}] WARNING: {new_nulls - original_nulls} new null values in {col}", "WARNING")

    return df


def apply_rule_4(df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
    """
    APPROVED Rule 4: Rename columns for clarity.
    dept → department
    dept_1 → expense_category
    """
    renames_applied = {}

    for old_name, new_name in COLUMN_RENAMES.items():
        if old_name in df.columns:
            df = df.rename(columns={old_name: new_name})
            renames_applied[old_name] = new_name
            log(f"[{sheet_name}] Rule 4: Renamed '{old_name}' → '{new_name}'")

    return df


def apply_rule_5(df: pd.DataFrame, sheet_name: str) -> pd.DataFrame:
    """
    APPROVED Rule 5: Preserve string columns as-is.
    This is a no-op confirmation - we simply don't transform string columns.
    """
    # Identify string columns (non-numeric)
    numeric_cols = NUMERIC_COLUMNS.get(sheet_name, [])
    string_cols = [col for col in df.columns if col not in numeric_cols]

    if string_cols:
        log(f"[{sheet_name}] Rule 5: Preserved {len(string_cols)} string columns as-is: {string_cols}")

    return df

# =============================================================================
# QC FUNCTIONS
# =============================================================================

def generate_post_metrics(df: pd.DataFrame, sheet_name: str) -> Dict:
    """Generate post-normalization metrics."""
    metrics = {
        "row_count": len(df),
        "column_count": len(df.columns),
        "columns": list(df.columns),
        "dtypes": {col: str(df[col].dtype) for col in df.columns},
        "null_counts": {col: int(df[col].isnull().sum()) for col in df.columns},
        "sums": {}
    }

    # Calculate post-normalization sums
    # Map old column names to new names for sum lookup
    numeric_cols_map = {
        "2018_total": "2018_total",
        "benchmark": "benchmark",
        "hourly_rate_usd": "hourly_rate_usd",
        "annual_salary_usd": "annual_salary_usd"
    }

    for col in numeric_cols_map.values():
        if col in df.columns:
            metrics["sums"][col] = float(df[col].sum())

    return metrics


def validate_invariants(pre: Dict, post: Dict, sheet_name: str) -> List[Dict]:
    """Validate that invariants are preserved."""
    results = []

    # Check row count
    row_match = pre["row_count"] == post["row_count"]
    results.append({
        "sheet": sheet_name,
        "check": "row_count",
        "pre_value": pre["row_count"],
        "post_value": post["row_count"],
        "status": "PASS" if row_match else "FAIL"
    })

    # Check column count
    col_match = pre["column_count"] == post["column_count"]
    results.append({
        "sheet": sheet_name,
        "check": "column_count",
        "pre_value": pre["column_count"],
        "post_value": post["column_count"],
        "status": "PASS" if col_match else "FAIL"
    })

    # Check null counts per column (accounting for renames)
    rename_map = {"dept": "department", "dept_1": "expense_category"}

    for pre_col, pre_nulls in pre["null_counts"].items():
        post_col = rename_map.get(pre_col, pre_col)
        if post_col in post["null_counts"]:
            post_nulls = post["null_counts"][post_col]
            null_match = pre_nulls == post_nulls
            results.append({
                "sheet": sheet_name,
                "check": f"null_count_{post_col}",
                "pre_value": pre_nulls,
                "post_value": post_nulls,
                "status": "PASS" if null_match else "FAIL"
            })

    return results


def validate_sums(pre: Dict, post: Dict, sheet_name: str) -> List[Dict]:
    """Validate that sums match within tolerance."""
    results = []
    tolerance = 0.01  # $0.01

    for col, pre_sum in pre["sums"].items():
        if col in post["sums"]:
            post_sum = post["sums"][col]
            diff = abs(post_sum - pre_sum)
            match = diff <= tolerance

            results.append({
                "sheet": sheet_name,
                "column": col,
                "pre_sum": pre_sum,
                "post_sum": post_sum,
                "difference": diff,
                "tolerance": tolerance,
                "status": "PASS" if match else "FAIL"
            })

    return results

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    log("=" * 70)
    log("PHASE 1c: EXECUTE APPROVED NORMALIZATION RULES")
    log("=" * 70)
    log("")
    log("APPROVED RULES:")
    log("  ✓ Rule 1: Convert numeric columns to float64")
    log("  ✓ Rule 4: Rename dept → department, dept_1 → expense_category")
    log("  ✓ Rule 5: Preserve string columns as-is")
    log("")
    log("NOT APPROVED (NOT APPLIED):")
    log("  ✗ Rule 2: Rounding")
    log("  ✗ Rule 3: Check-value handling")
    log("")

    # Ensure output directory exists
    os.makedirs(QC_OUTPUT_DIR, exist_ok=True)

    # Storage for all results
    all_pre_metrics = {}
    all_post_metrics = {}
    all_normalized_dfs = {}
    all_invariant_checks = []
    all_sum_checks = []
    dtype_summary = []

    # ==========================================================================
    # PROCESS INPUT P&L FILE
    # ==========================================================================

    log("-" * 50)
    log("Processing: Input P&L File")
    log("-" * 50)

    xl_pnl = pd.ExcelFile(INPUT_PL_FILE)

    for sheet_name in xl_pnl.sheet_names:
        log(f"\n>>> Sheet: {sheet_name}")

        # Ingest
        df, pre_metrics = ingest_sheet(xl_pnl, sheet_name)
        all_pre_metrics[sheet_name] = pre_metrics

        # Apply approved rules
        df = apply_rule_1(df, sheet_name)
        df = apply_rule_4(df, sheet_name)
        df = apply_rule_5(df, sheet_name)

        # Generate post-metrics
        post_metrics = generate_post_metrics(df, sheet_name)
        all_post_metrics[sheet_name] = post_metrics
        all_normalized_dfs[sheet_name] = df

        # Record dtype changes
        for col in df.columns:
            pre_col = col
            if col == "department":
                pre_col = "dept"
            elif col == "expense_category":
                pre_col = "dept_1"

            pre_dtype = pre_metrics["dtypes"].get(pre_col, "N/A")
            post_dtype = str(df[col].dtype)

            dtype_summary.append({
                "sheet": sheet_name,
                "column": col,
                "pre_dtype": pre_dtype,
                "post_dtype": post_dtype,
                "changed": pre_dtype != post_dtype
            })

        # Validate
        all_invariant_checks.extend(validate_invariants(pre_metrics, post_metrics, sheet_name))
        all_sum_checks.extend(validate_sums(pre_metrics, post_metrics, sheet_name))

    # ==========================================================================
    # PROCESS CENTRAL FINANCE ROLES FILE
    # ==========================================================================

    log("\n" + "-" * 50)
    log("Processing: Central Finance Roles File")
    log("-" * 50)

    xl_cfr = pd.ExcelFile(CENTRAL_FINANCE_FILE)

    for sheet_name in xl_cfr.sheet_names:
        log(f"\n>>> Sheet: {sheet_name}")

        # Ingest
        df, pre_metrics = ingest_sheet(xl_cfr, sheet_name)
        all_pre_metrics[sheet_name] = pre_metrics

        # Apply approved rules
        df = apply_rule_1(df, sheet_name)
        df = apply_rule_4(df, sheet_name)
        df = apply_rule_5(df, sheet_name)

        # Generate post-metrics
        post_metrics = generate_post_metrics(df, sheet_name)
        all_post_metrics[sheet_name] = post_metrics
        all_normalized_dfs[sheet_name] = df

        # Record dtype changes
        for col in df.columns:
            pre_dtype = pre_metrics["dtypes"].get(col, "N/A")
            post_dtype = str(df[col].dtype)

            dtype_summary.append({
                "sheet": sheet_name,
                "column": col,
                "pre_dtype": pre_dtype,
                "post_dtype": post_dtype,
                "changed": pre_dtype != post_dtype
            })

        # Validate
        all_invariant_checks.extend(validate_invariants(pre_metrics, post_metrics, sheet_name))
        all_sum_checks.extend(validate_sums(pre_metrics, post_metrics, sheet_name))

    # ==========================================================================
    # GENERATE QC OUTPUTS
    # ==========================================================================

    log("\n" + "=" * 70)
    log("GENERATING QC OUTPUTS")
    log("=" * 70)

    # 1. Post-normalization dtype summary
    dtype_df = pd.DataFrame(dtype_summary)
    dtype_path = os.path.join(QC_OUTPUT_DIR, "08_post_normalization_dtype_summary.csv")
    dtype_df.to_csv(dtype_path, index=False)
    log(f"\nSaved: {dtype_path}")

    # Show dtype changes
    changed_dtypes = dtype_df[dtype_df["changed"] == True]
    log(f"\nColumns with dtype changes: {len(changed_dtypes)}")
    if not changed_dtypes.empty:
        print(changed_dtypes.to_string(index=False))

    # 2. Pre/post sum reconciliation
    sum_df = pd.DataFrame(all_sum_checks)
    sum_path = os.path.join(QC_OUTPUT_DIR, "09_pre_post_sum_reconciliation.csv")
    sum_df.to_csv(sum_path, index=False)
    log(f"\nSaved: {sum_path}")

    # Show reconciliation results
    log("\nSum Reconciliation Results:")
    print(sum_df.to_string(index=False))

    # 3. Invariant check summary
    invariant_df = pd.DataFrame(all_invariant_checks)
    invariant_path = os.path.join(QC_OUTPUT_DIR, "10_invariant_checks.csv")
    invariant_df.to_csv(invariant_path, index=False)
    log(f"\nSaved: {invariant_path}")

    # Check for failures
    failed_invariants = invariant_df[invariant_df["status"] == "FAIL"]
    failed_sums = sum_df[sum_df["status"] == "FAIL"]

    log("\n" + "=" * 70)
    log("QC SUMMARY")
    log("=" * 70)

    log(f"\nInvariant Checks: {len(invariant_df)} total")
    log(f"  PASS: {len(invariant_df[invariant_df['status'] == 'PASS'])}")
    log(f"  FAIL: {len(failed_invariants)}")

    if not failed_invariants.empty:
        log("\nFAILED INVARIANTS:", "WARNING")
        print(failed_invariants.to_string(index=False))

    log(f"\nSum Reconciliation Checks: {len(sum_df)} total")
    log(f"  PASS: {len(sum_df[sum_df['status'] == 'PASS'])}")
    log(f"  FAIL: {len(failed_sums)}")

    if not failed_sums.empty:
        log("\nFAILED SUM RECONCILIATIONS:", "WARNING")
        print(failed_sums.to_string(index=False))

    # ==========================================================================
    # P&L SUMMARY CROSS-VALIDATION
    # ==========================================================================

    log("\n" + "=" * 70)
    log("P&L SUMMARY CROSS-VALIDATION")
    log("=" * 70)

    pnl_summary = all_normalized_dfs["P&L Summary"]

    # Get expected values from P&L Summary
    def get_pnl_value(label):
        row = pnl_summary[pnl_summary["p_l_summary"] == label]
        if not row.empty:
            return float(row["2018_total"].values[0])
        return None

    cross_validations = []

    # Revenue cross-validation
    recurring_expected = get_pnl_value("Recurring")
    recurring_actual = all_normalized_dfs["RecurringRevenue"]["2018_total"].sum()
    cross_validations.append({
        "category": "Recurring Revenue",
        "pnl_summary_value": recurring_expected,
        "computed_value": recurring_actual,
        "difference": abs(recurring_actual - recurring_expected) if recurring_expected else None,
        "status": "PASS" if recurring_expected and abs(recurring_actual - recurring_expected) < 0.01 else "FAIL"
    })

    pso_expected = get_pnl_value("PSO")
    pso_actual = all_normalized_dfs["PSORevenue"]["2018_total"].sum()
    cross_validations.append({
        "category": "PSO Revenue",
        "pnl_summary_value": pso_expected,
        "computed_value": pso_actual,
        "difference": abs(pso_actual - pso_expected) if pso_expected else None,
        "status": "PASS" if pso_expected and abs(pso_actual - pso_expected) < 0.01 else "FAIL"
    })

    perpetual_expected = get_pnl_value("Perpetual")
    perpetual_actual = all_normalized_dfs["PerpetualRevenue"]["2018_total"].sum()
    cross_validations.append({
        "category": "Perpetual Revenue",
        "pnl_summary_value": perpetual_expected,
        "computed_value": perpetual_actual,
        "difference": abs(perpetual_actual - perpetual_expected) if perpetual_expected else None,
        "status": "PASS" if perpetual_expected and abs(perpetual_actual - perpetual_expected) < 0.01 else "FAIL"
    })

    # Expense cross-validation
    hc_expected = get_pnl_value("HC Expense (W2)")
    hc_actual = all_normalized_dfs["Empl."]["2018_total"].sum()
    cross_validations.append({
        "category": "HC Expense (W2)",
        "pnl_summary_value": hc_expected,
        "computed_value": hc_actual,
        "difference": abs(hc_actual - hc_expected) if hc_expected else None,
        "status": "PASS" if hc_expected and abs(hc_actual - hc_expected) < 0.01 else "FAIL"
    })

    opex_expected = get_pnl_value("Non HC Expense (OPEX)")
    opex_actual = all_normalized_dfs["OPEX - NEmpl."]["2018_total"].sum()
    cross_validations.append({
        "category": "Non HC Expense (OPEX)",
        "pnl_summary_value": opex_expected,
        "computed_value": opex_actual,
        "difference": abs(opex_actual - opex_expected) if opex_expected else None,
        "status": "PASS" if opex_expected and abs(opex_actual - opex_expected) < 0.01 else "FAIL"
    })

    cogs_expected = get_pnl_value("Non HC Expense (COGS)")
    cogs_actual = all_normalized_dfs["COGS - NEmpl."]["2018_total"].sum()
    cross_validations.append({
        "category": "Non HC Expense (COGS)",
        "pnl_summary_value": cogs_expected,
        "computed_value": cogs_actual,
        "difference": abs(cogs_actual - cogs_expected) if cogs_expected else None,
        "status": "PASS" if cogs_expected and abs(cogs_actual - cogs_expected) < 0.01 else "FAIL"
    })

    cross_df = pd.DataFrame(cross_validations)
    cross_path = os.path.join(QC_OUTPUT_DIR, "11_pnl_cross_validation.csv")
    cross_df.to_csv(cross_path, index=False)
    log(f"\nSaved: {cross_path}")

    log("\nP&L Cross-Validation Results:")
    print(cross_df.to_string(index=False))

    all_cross_pass = all(cv["status"] == "PASS" for cv in cross_validations)

    # ==========================================================================
    # FINAL STATUS
    # ==========================================================================

    log("\n" + "=" * 70)
    log("PHASE 1c EXECUTION COMPLETE")
    log("=" * 70)

    all_pass = len(failed_invariants) == 0 and len(failed_sums) == 0 and all_cross_pass

    if all_pass:
        log("\n✓ ALL QC CHECKS PASSED")
        log("✓ Data is normalized and validated")
        log("✓ Ready for Phase 2")
    else:
        log("\n✗ SOME QC CHECKS FAILED - REVIEW REQUIRED", "WARNING")

    # Return results for external use
    return {
        "normalized_dfs": all_normalized_dfs,
        "qc_passed": all_pass,
        "execution_log": execution_log
    }


if __name__ == "__main__":
    results = main()

    # Save execution log
    log_path = "notes/phase_1c_execution_log.md"
    with open(log_path, "w") as f:
        f.write("# Phase 1c Execution Log\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("## Approved Rules Applied\n\n")
        f.write("- ✓ Rule 1: Convert numeric columns to float64\n")
        f.write("- ✓ Rule 4: Rename dept → department, dept_1 → expense_category\n")
        f.write("- ✓ Rule 5: Preserve string columns as-is\n\n")
        f.write("## Not Applied (Not Approved)\n\n")
        f.write("- ✗ Rule 2: Rounding\n")
        f.write("- ✗ Rule 3: Check-value handling\n\n")
        f.write("## Execution Log\n\n")
        f.write("```\n")
        for entry in results["execution_log"]:
            f.write(entry + "\n")
        f.write("```\n\n")
        f.write("## QC Status\n\n")
        f.write(f"**All checks passed: {results['qc_passed']}**\n")

    print(f"\nExecution log saved to: {log_path}")
