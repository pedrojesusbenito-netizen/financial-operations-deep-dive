#!/usr/bin/env python3
"""
Phase 1: Data Ingestion, Schema Detection & Structural QC

This script safely ingests all sheets from the Input P&L file and Central Finance Roles file,
detects headers programmatically, normalizes schemas, and generates QC artifacts.

Author: Phase 1 Execution
Date: 2026-01-05

IMPORTANT: This script does NOT modify raw data files.
"""

import pandas as pd
import numpy as np
import re
import os
from datetime import datetime
from typing import Dict, List, Tuple, Any, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_PL_FILE = "data/Operational Leadership Real Work - Input P&L.xlsx"
CENTRAL_FINANCE_FILE = "data/Central Finance Roles.xlsx"
QC_OUTPUT_DIR = "outputs/qc"
ASSUMPTIONS_FILE = "notes/assumptions.md"

# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def to_snake_case(name: str) -> str:
    """
    Convert a column name to snake_case.

    Examples:
        "Function L1" -> "function_l1"
        "2018 total" -> "2018_total"
        "Customer Name" -> "customer_name"
        "Hourly Rate (USD)" -> "hourly_rate_usd"
    """
    if pd.isna(name):
        return "unnamed"

    name = str(name).strip()

    # Remove parentheses content but keep the text
    name = re.sub(r'\(([^)]+)\)', r'_\1', name)

    # Replace special characters with underscores
    name = re.sub(r'[^\w\s]', '_', name)

    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)

    # Remove consecutive underscores
    name = re.sub(r'_+', '_', name)

    # Convert to lowercase
    name = name.lower()

    # Remove leading/trailing underscores
    name = name.strip('_')

    return name if name else "unnamed"


def is_likely_header_row(row: pd.Series, total_cols: int) -> bool:
    """
    Determine if a row is likely a header row based on heuristics.

    A header row typically:
    - Has mostly non-null values
    - Contains mostly string values
    - Does not contain metadata markers like "IN USD"
    - Has values that look like column names (not pure numbers)
    """
    non_null_count = row.notna().sum()

    # Must have at least 50% non-null values
    if non_null_count < total_cols * 0.5:
        return False

    non_null_values = row.dropna()

    # Check if most values are strings (not numbers)
    string_count = sum(1 for v in non_null_values if isinstance(v, str) or
                       (not pd.isna(v) and not isinstance(v, (int, float))))

    # At least 50% should be string-like
    if string_count < len(non_null_values) * 0.5:
        return False

    # Check for metadata markers (these indicate non-header rows)
    metadata_markers = ["IN USD", "Maintenance", "Perpetual"]
    first_values = [str(v).strip() for v in non_null_values.head(3) if not pd.isna(v)]

    for marker in metadata_markers:
        if any(marker == v for v in first_values):
            return False

    return True


def detect_header_row(df_raw: pd.DataFrame, sheet_name: str) -> Tuple[int, List[str]]:
    """
    Programmatically detect the header row index for a given sheet.

    Returns:
        Tuple of (header_row_index, list_of_reasons)
    """
    reasons = []
    total_cols = df_raw.shape[1]
    max_rows_to_check = min(5, df_raw.shape[0])

    for idx in range(max_rows_to_check):
        row = df_raw.iloc[idx]

        if is_likely_header_row(row, total_cols):
            reasons.append(f"Row {idx} identified as header: contains {row.notna().sum()}/{total_cols} non-null values")

            # Additional check: ensure subsequent row has actual data (numbers or different pattern)
            if idx + 1 < df_raw.shape[0]:
                next_row = df_raw.iloc[idx + 1]
                numeric_count = sum(1 for v in next_row if isinstance(v, (int, float)) and not pd.isna(v))
                if numeric_count > 0:
                    reasons.append(f"Confirmed: Row {idx + 1} contains {numeric_count} numeric values (data row)")

            return idx, reasons

    # Fallback: assume row 0 is header
    reasons.append("Fallback: Using row 0 as header (no clear header detected)")
    return 0, reasons


def normalize_dataframe(df_raw: pd.DataFrame, header_row: int, sheet_name: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Normalize a DataFrame by setting the correct header and converting column names to snake_case.

    Returns:
        Tuple of (normalized_df, metadata_dict)
    """
    # Extract original column names
    original_columns = df_raw.iloc[header_row].tolist()

    # Handle duplicate column names by making them unique
    seen = {}
    unique_original = []
    for col in original_columns:
        col_str = str(col) if not pd.isna(col) else "unnamed"
        if col_str in seen:
            seen[col_str] += 1
            unique_original.append(f"{col_str}_{seen[col_str]}")
        else:
            seen[col_str] = 0
            unique_original.append(col_str)

    # Convert to snake_case
    normalized_columns = [to_snake_case(col) for col in unique_original]

    # Handle any remaining duplicates after normalization
    seen_normalized = {}
    final_columns = []
    for col in normalized_columns:
        if col in seen_normalized:
            seen_normalized[col] += 1
            final_columns.append(f"{col}_{seen_normalized[col]}")
        else:
            seen_normalized[col] = 0
            final_columns.append(col)

    # Create normalized DataFrame (skip rows before and including header)
    df_normalized = df_raw.iloc[header_row + 1:].copy()
    df_normalized.columns = final_columns
    df_normalized = df_normalized.reset_index(drop=True)

    metadata = {
        "original_columns": original_columns,
        "normalized_columns": final_columns,
        "header_row": header_row,
        "data_start_row": header_row + 1,
        "original_row_count": df_raw.shape[0],
        "rows_before_header": header_row,
        "rows_ingested": len(df_normalized)
    }

    return df_normalized, metadata


def calculate_null_rates(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate null rates for each column in a DataFrame."""
    total_rows = len(df)
    null_counts = df.isnull().sum()
    null_rates = (null_counts / total_rows * 100).round(2)

    result = pd.DataFrame({
        "column": df.columns,
        "null_count": null_counts.values,
        "total_rows": total_rows,
        "null_rate_pct": null_rates.values
    })

    return result


# =============================================================================
# MAIN INGESTION LOGIC
# =============================================================================

def ingest_excel_file(file_path: str, file_label: str) -> Tuple[Dict[str, pd.DataFrame], List[Dict], List[str]]:
    """
    Ingest all sheets from an Excel file.

    Returns:
        Tuple of (dict of normalized DataFrames, list of QC records, list of assumptions)
    """
    print(f"\n{'='*60}")
    print(f"Ingesting: {file_path}")
    print(f"{'='*60}")

    xl = pd.ExcelFile(file_path)
    normalized_dfs = {}
    qc_records = []
    assumptions = []

    for sheet_name in xl.sheet_names:
        print(f"\n--- Processing sheet: {sheet_name} ---")

        # Read raw data without header
        df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        original_row_count = df_raw.shape[0]
        original_col_count = df_raw.shape[1]

        print(f"  Raw dimensions: {original_row_count} rows x {original_col_count} cols")

        # Detect header row
        header_row, detection_reasons = detect_header_row(df_raw, sheet_name)
        print(f"  Detected header row: {header_row}")
        for reason in detection_reasons:
            print(f"    - {reason}")

        # Normalize DataFrame
        df_normalized, metadata = normalize_dataframe(df_raw, header_row, sheet_name)

        # Store normalized DataFrame
        normalized_dfs[sheet_name] = df_normalized

        # Calculate rows dropped
        rows_dropped = original_row_count - metadata["rows_ingested"] - 1  # -1 for header row

        # Log assumptions if any
        if header_row > 0:
            assumption = f"[{file_label}][{sheet_name}] Rows 0-{header_row-1} treated as metadata/non-data rows"
            assumptions.append(assumption)
            print(f"  Assumption logged: {assumption}")

        # Create QC record
        qc_record = {
            "file": file_label,
            "sheet_name": sheet_name,
            "original_row_count": original_row_count,
            "detected_header_row": header_row,
            "data_start_row": metadata["data_start_row"],
            "rows_ingested": metadata["rows_ingested"],
            "rows_dropped": rows_dropped,
            "drop_reason": f"Non-data rows before header (rows 0-{header_row})" if rows_dropped > 0 else "None",
            "original_col_count": original_col_count,
            "normalized_col_count": len(metadata["normalized_columns"])
        }
        qc_records.append(qc_record)

        print(f"  Rows ingested: {metadata['rows_ingested']}")
        print(f"  Columns: {metadata['normalized_columns']}")

    return normalized_dfs, qc_records, assumptions


def generate_column_mapping_report(all_metadata: Dict[str, Dict]) -> pd.DataFrame:
    """Generate a report showing original vs normalized column names."""
    records = []

    for sheet_name, metadata in all_metadata.items():
        for orig, norm in zip(metadata["original_columns"], metadata["normalized_columns"]):
            records.append({
                "sheet_name": sheet_name,
                "original_column": str(orig),
                "normalized_column": norm,
                "transformation_applied": "Yes" if str(orig) != norm else "No"
            })

    return pd.DataFrame(records)


def generate_null_rate_report(normalized_dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Generate a null rate report for all sheets."""
    all_null_rates = []

    for sheet_name, df in normalized_dfs.items():
        null_rates = calculate_null_rates(df)
        null_rates.insert(0, "sheet_name", sheet_name)
        all_null_rates.append(null_rates)

    if all_null_rates:
        return pd.concat(all_null_rates, ignore_index=True)
    return pd.DataFrame()


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    print("=" * 60)
    print("PHASE 1: DATA INGESTION, SCHEMA DETECTION & STRUCTURAL QC")
    print(f"Execution timestamp: {datetime.now().isoformat()}")
    print("=" * 60)

    # Ensure output directories exist
    os.makedirs(QC_OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(ASSUMPTIONS_FILE), exist_ok=True)

    all_assumptions = []
    all_qc_records = []
    all_normalized_dfs = {}
    all_metadata = {}

    # ==========================================================================
    # INGEST INPUT P&L FILE
    # ==========================================================================

    pnl_dfs, pnl_qc, pnl_assumptions = ingest_excel_file(INPUT_PL_FILE, "Input P&L")
    all_assumptions.extend(pnl_assumptions)
    all_qc_records.extend(pnl_qc)

    for sheet_name, df in pnl_dfs.items():
        all_normalized_dfs[f"pnl_{sheet_name}"] = df
        # Store metadata for column mapping
        xl = pd.ExcelFile(INPUT_PL_FILE)
        df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        header_row, _ = detect_header_row(df_raw, sheet_name)
        _, metadata = normalize_dataframe(df_raw, header_row, sheet_name)
        all_metadata[f"pnl_{sheet_name}"] = metadata

    # ==========================================================================
    # INGEST CENTRAL FINANCE ROLES FILE
    # ==========================================================================

    cfr_dfs, cfr_qc, cfr_assumptions = ingest_excel_file(CENTRAL_FINANCE_FILE, "Central Finance Roles")
    all_assumptions.extend(cfr_assumptions)
    all_qc_records.extend(cfr_qc)

    for sheet_name, df in cfr_dfs.items():
        all_normalized_dfs[f"cfr_{sheet_name}"] = df
        xl = pd.ExcelFile(CENTRAL_FINANCE_FILE)
        df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        header_row, _ = detect_header_row(df_raw, sheet_name)
        _, metadata = normalize_dataframe(df_raw, header_row, sheet_name)
        all_metadata[f"cfr_{sheet_name}"] = metadata

    # ==========================================================================
    # GENERATE QC OUTPUTS
    # ==========================================================================

    print("\n" + "=" * 60)
    print("GENERATING QC OUTPUTS")
    print("=" * 60)

    # 1. Sheet-level QC summary
    qc_summary_df = pd.DataFrame(all_qc_records)
    qc_summary_path = os.path.join(QC_OUTPUT_DIR, "01_sheet_ingestion_summary.csv")
    qc_summary_df.to_csv(qc_summary_path, index=False)
    print(f"\n[QC] Sheet ingestion summary saved to: {qc_summary_path}")
    print(qc_summary_df.to_string(index=False))

    # 2. Column mapping report
    column_mapping_df = generate_column_mapping_report(all_metadata)
    column_mapping_path = os.path.join(QC_OUTPUT_DIR, "02_column_name_mapping.csv")
    column_mapping_df.to_csv(column_mapping_path, index=False)
    print(f"\n[QC] Column name mapping saved to: {column_mapping_path}")
    print(f"     Total columns mapped: {len(column_mapping_df)}")

    # 3. Null rate report
    null_rate_df = generate_null_rate_report(all_normalized_dfs)
    null_rate_path = os.path.join(QC_OUTPUT_DIR, "03_null_rate_summary.csv")
    null_rate_df.to_csv(null_rate_path, index=False)
    print(f"\n[QC] Null rate summary saved to: {null_rate_path}")

    # Show high null rate columns (>50%)
    high_null = null_rate_df[null_rate_df["null_rate_pct"] > 50]
    if not high_null.empty:
        print("\n[QC] Columns with >50% null rate:")
        print(high_null.to_string(index=False))
    else:
        print("\n[QC] No columns with >50% null rate detected.")

    # 4. Data type summary
    dtype_records = []
    for key, df in all_normalized_dfs.items():
        for col in df.columns:
            dtype_records.append({
                "sheet_key": key,
                "column": col,
                "pandas_dtype": str(df[col].dtype),
                "sample_value": str(df[col].dropna().iloc[0]) if not df[col].dropna().empty else "N/A"
            })
    dtype_df = pd.DataFrame(dtype_records)
    dtype_path = os.path.join(QC_OUTPUT_DIR, "04_data_type_summary.csv")
    dtype_df.to_csv(dtype_path, index=False)
    print(f"\n[QC] Data type summary saved to: {dtype_path}")

    # 5. Row count reconciliation
    print("\n" + "-" * 60)
    print("ROW COUNT RECONCILIATION")
    print("-" * 60)

    total_original = sum(r["original_row_count"] for r in all_qc_records)
    total_ingested = sum(r["rows_ingested"] for r in all_qc_records)
    total_header_rows = len(all_qc_records)  # One header per sheet
    total_metadata_rows = sum(r["detected_header_row"] for r in all_qc_records)

    print(f"Total original rows across all sheets: {total_original}")
    print(f"Total header rows (1 per sheet): {total_header_rows}")
    print(f"Total metadata rows (before headers): {total_metadata_rows}")
    print(f"Total data rows ingested: {total_ingested}")
    print(f"Expected: {total_original} - {total_header_rows} - {total_metadata_rows} = {total_original - total_header_rows - total_metadata_rows}")

    if total_ingested == total_original - total_header_rows - total_metadata_rows:
        print("[PASS] Row counts reconcile correctly.")
    else:
        print("[FLAG] Row count discrepancy detected - manual review recommended.")

    # ==========================================================================
    # SAVE ASSUMPTIONS
    # ==========================================================================

    print("\n" + "=" * 60)
    print("DOCUMENTING ASSUMPTIONS")
    print("=" * 60)

    assumptions_content = f"""# Phase 1 Ingestion Assumptions

Generated: {datetime.now().isoformat()}

## Header Detection Assumptions

"""

    for assumption in all_assumptions:
        assumptions_content += f"- {assumption}\n"

    if not all_assumptions:
        assumptions_content += "- No special assumptions required; all sheets had headers at row 0.\n"

    assumptions_content += """
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
"""

    with open(ASSUMPTIONS_FILE, "w") as f:
        f.write(assumptions_content)

    print(f"Assumptions documented in: {ASSUMPTIONS_FILE}")

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================

    print("\n" + "=" * 60)
    print("PHASE 1 COMPLETE - SUMMARY")
    print("=" * 60)

    print(f"\nFiles ingested: 2")
    print(f"  - {INPUT_PL_FILE}: {len(pnl_dfs)} sheets")
    print(f"  - {CENTRAL_FINANCE_FILE}: {len(cfr_dfs)} sheets")
    print(f"\nTotal sheets processed: {len(all_normalized_dfs)}")
    print(f"Total data rows ingested: {total_ingested}")
    print(f"QC artifacts generated: 4 files in {QC_OUTPUT_DIR}/")
    print(f"Assumptions documented: {ASSUMPTIONS_FILE}")

    print("\n" + "=" * 60)
    print("STOPPING - AWAITING SVP APPROVAL BEFORE PHASE 2")
    print("=" * 60)

    return all_normalized_dfs, all_qc_records, all_assumptions


if __name__ == "__main__":
    main()
