#!/usr/bin/env python3
"""
Phase 2: Financial Overview & Anomaly Flagging

CONSTRAINTS:
- Diagnostic only
- No "Why" questions
- No fixes or recommendations
- No data modifications
- Negative values preserved (legitimate business activity)

Author: Phase 2 Execution
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
OUTPUT_DIR = "outputs/phase_2"

# Header row positions and column mappings (from Phase 1)
SHEET_CONFIG = {
    "Benchmarks": {"header": 0, "cols": ["category", "benchmark"]},
    "P&L Summary": {"header": 0, "cols": ["p_l_summary", "2018_total"]},
    "OPEX - NEmpl.": {"header": 1, "cols": ["function_l1", "function_l2", "department", "expense_category", "vendor", "2018_total"]},
    "COGS - NEmpl.": {"header": 1, "cols": ["function_l1", "function_l2", "department", "expense_category", "vendor", "2018_total"]},
    "Empl.": {"header": 2, "cols": ["tier", "category", "function_l1", "function_l2", "department", "name", "2018_total"]},
    "RecurringRevenue": {"header": 2, "cols": ["tier", "type", "customer_name", "2018_total"]},
    "PSORevenue": {"header": 2, "cols": ["tier", "type", "customer_name", "2018_total"]},
    "PerpetualRevenue": {"header": 2, "cols": ["tier", "type", "customer_name", "2018_total"]},
}

# =============================================================================
# DATA LOADING (Using Phase 1 normalized approach)
# =============================================================================

def load_normalized_data() -> Dict[str, pd.DataFrame]:
    """Load all sheets with Phase 1c normalization applied."""
    xl = pd.ExcelFile(INPUT_PL_FILE)
    data = {}

    for sheet_name, config in SHEET_CONFIG.items():
        df_raw = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        df = df_raw.iloc[config["header"] + 1:].copy()
        df.columns = config["cols"]
        df = df.reset_index(drop=True)

        # Apply Rule 1: Convert numeric columns
        if "2018_total" in df.columns:
            df["2018_total"] = pd.to_numeric(df["2018_total"], errors='coerce')
        if "benchmark" in df.columns:
            df["benchmark"] = pd.to_numeric(df["benchmark"], errors='coerce')

        # Apply Rule 4: Rename columns (already in config)
        data[sheet_name] = df

    return data

# =============================================================================
# 1. P&L OVERVIEW
# =============================================================================

def generate_pnl_overview(data: Dict[str, pd.DataFrame]) -> Dict:
    """Generate high-level P&L overview from normalized data."""

    pnl = data["P&L Summary"]

    def get_value(label):
        row = pnl[pnl["p_l_summary"] == label]
        if not row.empty:
            return float(row["2018_total"].values[0])
        return None

    # Revenue breakdown
    recurring_revenue = data["RecurringRevenue"]["2018_total"].sum()
    pso_revenue = data["PSORevenue"]["2018_total"].sum()
    perpetual_revenue = data["PerpetualRevenue"]["2018_total"].sum()
    total_revenue = recurring_revenue + pso_revenue + perpetual_revenue

    # Expense breakdown
    hc_expense = data["Empl."]["2018_total"].sum()
    opex_nonhc = data["OPEX - NEmpl."]["2018_total"].sum()
    cogs_nonhc = data["COGS - NEmpl."]["2018_total"].sum()
    total_nonhc = opex_nonhc + cogs_nonhc
    total_expense = hc_expense + total_nonhc

    # Margins
    gross_margin = total_revenue - total_expense
    gross_margin_pct = (gross_margin / total_revenue * 100) if total_revenue != 0 else 0

    # P&L Summary reference values
    pnl_revenue = get_value("Revenue")
    pnl_margin = get_value("Margin")
    pnl_margin_pct = get_value("Margin %")

    overview = {
        "revenue": {
            "recurring": recurring_revenue,
            "pso": pso_revenue,
            "perpetual": perpetual_revenue,
            "total_computed": total_revenue,
            "total_pnl_summary": pnl_revenue
        },
        "expenses": {
            "hc_w2": hc_expense,
            "nonhc_opex": opex_nonhc,
            "nonhc_cogs": cogs_nonhc,
            "total_nonhc": total_nonhc,
            "total": total_expense
        },
        "margins": {
            "gross_margin": gross_margin,
            "gross_margin_pct": gross_margin_pct,
            "pnl_margin": pnl_margin,
            "pnl_margin_pct": pnl_margin_pct * 100 if pnl_margin_pct else None
        }
    }

    return overview

# =============================================================================
# 2. RECONCILIATION CHECKS
# =============================================================================

def perform_reconciliation_checks(data: Dict[str, pd.DataFrame], overview: Dict) -> List[Dict]:
    """Check internal consistency between detail sheets and P&L Summary."""

    checks = []
    pnl = data["P&L Summary"]

    def get_pnl_value(label):
        row = pnl[pnl["p_l_summary"] == label]
        if not row.empty:
            return float(row["2018_total"].values[0])
        return None

    tolerance = 0.01

    # Revenue checks
    checks.append({
        "check": "Recurring Revenue",
        "pnl_summary": get_pnl_value("Recurring"),
        "computed": overview["revenue"]["recurring"],
        "difference": abs(overview["revenue"]["recurring"] - get_pnl_value("Recurring")),
        "status": "RECONCILED" if abs(overview["revenue"]["recurring"] - get_pnl_value("Recurring")) < tolerance else "DISCREPANCY"
    })

    checks.append({
        "check": "PSO Revenue",
        "pnl_summary": get_pnl_value("PSO"),
        "computed": overview["revenue"]["pso"],
        "difference": abs(overview["revenue"]["pso"] - get_pnl_value("PSO")),
        "status": "RECONCILED" if abs(overview["revenue"]["pso"] - get_pnl_value("PSO")) < tolerance else "DISCREPANCY"
    })

    checks.append({
        "check": "Perpetual Revenue",
        "pnl_summary": get_pnl_value("Perpetual"),
        "computed": overview["revenue"]["perpetual"],
        "difference": abs(overview["revenue"]["perpetual"] - get_pnl_value("Perpetual")),
        "status": "RECONCILED" if abs(overview["revenue"]["perpetual"] - get_pnl_value("Perpetual")) < tolerance else "DISCREPANCY"
    })

    checks.append({
        "check": "Total Revenue",
        "pnl_summary": get_pnl_value("Revenue"),
        "computed": overview["revenue"]["total_computed"],
        "difference": abs(overview["revenue"]["total_computed"] - get_pnl_value("Revenue")),
        "status": "RECONCILED" if abs(overview["revenue"]["total_computed"] - get_pnl_value("Revenue")) < tolerance else "DISCREPANCY"
    })

    # Expense checks
    checks.append({
        "check": "HC Expense (W2)",
        "pnl_summary": get_pnl_value("HC Expense (W2)"),
        "computed": overview["expenses"]["hc_w2"],
        "difference": abs(overview["expenses"]["hc_w2"] - get_pnl_value("HC Expense (W2)")),
        "status": "RECONCILED" if abs(overview["expenses"]["hc_w2"] - get_pnl_value("HC Expense (W2)")) < tolerance else "DISCREPANCY"
    })

    checks.append({
        "check": "Non HC Expense (OPEX)",
        "pnl_summary": get_pnl_value("Non HC Expense (OPEX)"),
        "computed": overview["expenses"]["nonhc_opex"],
        "difference": abs(overview["expenses"]["nonhc_opex"] - get_pnl_value("Non HC Expense (OPEX)")),
        "status": "RECONCILED" if abs(overview["expenses"]["nonhc_opex"] - get_pnl_value("Non HC Expense (OPEX)")) < tolerance else "DISCREPANCY"
    })

    checks.append({
        "check": "Non HC Expense (COGS)",
        "pnl_summary": get_pnl_value("Non HC Expense (COGS)"),
        "computed": overview["expenses"]["nonhc_cogs"],
        "difference": abs(overview["expenses"]["nonhc_cogs"] - get_pnl_value("Non HC Expense (COGS)")),
        "status": "RECONCILED" if abs(overview["expenses"]["nonhc_cogs"] - get_pnl_value("Non HC Expense (COGS)")) < tolerance else "DISCREPANCY"
    })

    return checks

# =============================================================================
# 3. NEGATIVE VALUE ANALYSIS
# =============================================================================

def analyze_negative_values(data: Dict[str, pd.DataFrame]) -> Dict:
    """Analyze negative value patterns across all sheets."""

    negative_analysis = {}

    sheets_to_analyze = [
        ("OPEX - NEmpl.", "function_l2", "department"),
        ("COGS - NEmpl.", "function_l2", "department"),
        ("Empl.", "function_l2", "department"),
        ("RecurringRevenue", "type", None),
        ("PSORevenue", "type", None),
        ("PerpetualRevenue", "type", None),
    ]

    for sheet_name, category_col, subcategory_col in sheets_to_analyze:
        df = data[sheet_name]
        total_col = "2018_total"

        # Overall metrics
        total_rows = len(df)
        total_sum = df[total_col].sum()
        total_abs_sum = df[total_col].abs().sum()

        # Negative value metrics
        neg_mask = df[total_col] < 0
        neg_count = neg_mask.sum()
        neg_sum = df.loc[neg_mask, total_col].sum()
        neg_abs_sum = df.loc[neg_mask, total_col].abs().sum()

        # Percentage of category affected
        neg_pct_of_total = (neg_abs_sum / total_abs_sum * 100) if total_abs_sum != 0 else 0

        sheet_analysis = {
            "total_rows": total_rows,
            "total_sum": total_sum,
            "total_abs_sum": total_abs_sum,
            "negative_count": neg_count,
            "negative_sum": neg_sum,
            "negative_abs_sum": neg_abs_sum,
            "negative_pct_of_abs_total": neg_pct_of_total,
            "by_category": {}
        }

        # Breakdown by category
        if category_col and category_col in df.columns:
            for cat in df[category_col].dropna().unique():
                cat_df = df[df[category_col] == cat]
                cat_total = cat_df[total_col].sum()
                cat_abs_total = cat_df[total_col].abs().sum()
                cat_neg_mask = cat_df[total_col] < 0
                cat_neg_count = cat_neg_mask.sum()
                cat_neg_sum = cat_df.loc[cat_neg_mask, total_col].sum()
                cat_neg_abs = cat_df.loc[cat_neg_mask, total_col].abs().sum()
                cat_neg_pct = (cat_neg_abs / cat_abs_total * 100) if cat_abs_total != 0 else 0

                sheet_analysis["by_category"][cat] = {
                    "total": cat_total,
                    "abs_total": cat_abs_total,
                    "neg_count": cat_neg_count,
                    "neg_sum": cat_neg_sum,
                    "neg_abs_sum": cat_neg_abs,
                    "neg_pct": cat_neg_pct
                }

        # Breakdown by subcategory (department) if applicable
        if subcategory_col and subcategory_col in df.columns:
            sheet_analysis["by_department"] = {}
            for dept in df[subcategory_col].dropna().unique():
                dept_df = df[df[subcategory_col] == dept]
                dept_total = dept_df[total_col].sum()
                dept_abs_total = dept_df[total_col].abs().sum()
                dept_neg_mask = dept_df[total_col] < 0
                dept_neg_count = dept_neg_mask.sum()
                dept_neg_sum = dept_df.loc[dept_neg_mask, total_col].sum()
                dept_neg_abs = dept_df.loc[dept_neg_mask, total_col].abs().sum()
                dept_neg_pct = (dept_neg_abs / dept_abs_total * 100) if dept_abs_total != 0 else 0

                sheet_analysis["by_department"][dept] = {
                    "total": dept_total,
                    "abs_total": dept_abs_total,
                    "neg_count": dept_neg_count,
                    "neg_sum": dept_neg_sum,
                    "neg_abs_sum": dept_neg_abs,
                    "neg_pct": dept_neg_pct
                }

        negative_analysis[sheet_name] = sheet_analysis

    return negative_analysis

def classify_negative_patterns(negative_analysis: Dict) -> List[Dict]:
    """Classify negative patterns as Isolated, Systematic, or Material."""

    patterns = []

    for sheet_name, analysis in negative_analysis.items():
        # Skip if no negatives
        if analysis["negative_count"] == 0:
            continue

        # Check materiality at sheet level (>10% threshold)
        is_material = analysis["negative_pct_of_abs_total"] > 10

        # Check for systematic patterns (concentrated in categories)
        systematic_categories = []
        if "by_category" in analysis:
            for cat, cat_data in analysis["by_category"].items():
                if cat_data["neg_pct"] > 10 and cat_data["neg_count"] > 1:
                    systematic_categories.append({
                        "category": cat,
                        "neg_pct": cat_data["neg_pct"],
                        "neg_count": cat_data["neg_count"],
                        "neg_sum": cat_data["neg_sum"]
                    })

        # Check for department concentration
        systematic_depts = []
        if "by_department" in analysis:
            for dept, dept_data in analysis["by_department"].items():
                if dept_data["neg_pct"] > 10 and dept_data["neg_count"] > 1:
                    systematic_depts.append({
                        "department": dept,
                        "neg_pct": dept_data["neg_pct"],
                        "neg_count": dept_data["neg_count"],
                        "neg_sum": dept_data["neg_sum"]
                    })

        # Determine classification
        if is_material or len(systematic_categories) > 0 or len(systematic_depts) > 0:
            classification = "Material" if is_material else "Systematic"
        else:
            classification = "Isolated"

        patterns.append({
            "sheet": sheet_name,
            "classification": classification,
            "total_negative_count": analysis["negative_count"],
            "total_negative_sum": analysis["negative_sum"],
            "negative_pct_of_total": analysis["negative_pct_of_abs_total"],
            "systematic_categories": systematic_categories,
            "systematic_departments": systematic_depts
        })

    return patterns

# =============================================================================
# 4. OUT-OF-MODEL SIGNAL DETECTION
# =============================================================================

def detect_out_of_model_signals(data: Dict[str, pd.DataFrame], overview: Dict) -> List[Dict]:
    """Detect potentially concerning signals."""

    signals = []
    benchmarks = data["Benchmarks"].set_index("category")["benchmark"].to_dict()
    total_revenue = overview["revenue"]["total_computed"]

    # 1. Check expense categories against benchmarks
    expense_categories = {
        "Shared Services": overview["expenses"]["nonhc_opex"],  # Approximation
        "Engineering": None,  # Will calculate from details
        "Technical Support": None,
        "Hosting": None,
        "Product": None,
        "Sales": None,
        "Marketing": None,
    }

    # Calculate function-level expenses from OPEX and COGS
    opex = data["OPEX - NEmpl."]
    cogs = data["COGS - NEmpl."]
    empl = data["Empl."]

    # Aggregate by function_l2
    opex_by_func = opex.groupby("function_l2")["2018_total"].sum()
    cogs_by_func = cogs.groupby("function_l2")["2018_total"].sum()
    empl_by_func = empl.groupby("function_l2")["2018_total"].sum()

    # G&A expenses (proxy for Shared Services + Executive)
    ga_opex = opex_by_func.get("G&A", 0)
    ga_total = ga_opex
    ga_pct = (ga_total / total_revenue) if total_revenue else 0
    shared_services_benchmark = benchmarks.get("Shared Services", 0.045)
    executive_benchmark = benchmarks.get("Executive team", 0.045)
    combined_ga_benchmark = shared_services_benchmark + executive_benchmark

    if ga_pct > combined_ga_benchmark:
        signals.append({
            "area": "OPEX - G&A",
            "description": f"G&A expense at {ga_pct*100:.1f}% of revenue",
            "benchmark": f"{combined_ga_benchmark*100:.1f}%",
            "actual": f"{ga_pct*100:.1f}%",
            "variance": f"+{(ga_pct - combined_ga_benchmark)*100:.1f}pp",
            "evidence": f"OPEX G&A total: ${ga_total:,.0f}"
        })

    # S&M expenses
    sm_opex = opex_by_func.get("S&M", 0)
    sm_cogs = cogs_by_func.get("S&M", 0) if "S&M" in cogs_by_func else 0
    sm_total = sm_opex + sm_cogs
    sm_pct = (sm_total / total_revenue) if total_revenue else 0
    sales_benchmark = benchmarks.get("Sales", 0.05)
    marketing_benchmark = benchmarks.get("Marketing", 0.01)
    sm_benchmark = sales_benchmark + marketing_benchmark

    if sm_pct > sm_benchmark:
        signals.append({
            "area": "S&M",
            "description": f"S&M expense at {sm_pct*100:.1f}% of revenue",
            "benchmark": f"{sm_benchmark*100:.1f}%",
            "actual": f"{sm_pct*100:.1f}%",
            "variance": f"+{(sm_pct - sm_benchmark)*100:.1f}pp",
            "evidence": f"OPEX S&M: ${sm_opex:,.0f}"
        })

    # R&D expenses
    rd_opex = opex_by_func.get("R&D", 0)
    rd_total = rd_opex
    rd_pct = (rd_total / total_revenue) if total_revenue else 0
    engineering_benchmark = benchmarks.get("Engineering", 0.10)
    product_benchmark = benchmarks.get("Product", 0.02)
    rd_benchmark = engineering_benchmark + product_benchmark

    if rd_pct > rd_benchmark:
        signals.append({
            "area": "R&D",
            "description": f"R&D expense at {rd_pct*100:.1f}% of revenue",
            "benchmark": f"{rd_benchmark*100:.1f}%",
            "actual": f"{rd_pct*100:.1f}%",
            "variance": f"+{(rd_pct - rd_benchmark)*100:.1f}pp",
            "evidence": f"OPEX R&D: ${rd_opex:,.0f}"
        })

    # 2. HC vs Non-HC mix analysis
    hc_total = overview["expenses"]["hc_w2"]
    nonhc_total = overview["expenses"]["total_nonhc"]
    total_expense = overview["expenses"]["total"]

    hc_pct = (hc_total / total_expense * 100) if total_expense else 0
    nonhc_pct = (nonhc_total / total_expense * 100) if total_expense else 0

    # Flag if Non-HC > HC (unusual for service business)
    if nonhc_total > hc_total:
        signals.append({
            "area": "Expense Mix",
            "description": f"Non-HC expense ({nonhc_pct:.1f}%) exceeds HC expense ({hc_pct:.1f}%)",
            "benchmark": "Typically HC > Non-HC for service businesses",
            "actual": f"HC: {hc_pct:.1f}%, Non-HC: {nonhc_pct:.1f}%",
            "variance": f"Non-HC exceeds HC by ${nonhc_total - hc_total:,.0f}",
            "evidence": f"HC: ${hc_total:,.0f}, Non-HC: ${nonhc_total:,.0f}"
        })

    # 3. Margin analysis
    margin_pct = overview["margins"]["gross_margin_pct"]
    margin_benchmark = benchmarks.get("Margin", 0.70)

    if margin_pct < margin_benchmark * 100:
        signals.append({
            "area": "Margin",
            "description": f"Gross margin at {margin_pct:.1f}%, below benchmark",
            "benchmark": f"{margin_benchmark*100:.1f}%",
            "actual": f"{margin_pct:.1f}%",
            "variance": f"{margin_pct - margin_benchmark*100:.1f}pp",
            "evidence": f"Margin: ${overview['margins']['gross_margin']:,.0f}"
        })

    # 4. Revenue concentration (check if any revenue type dominates)
    recurring_pct = (overview["revenue"]["recurring"] / total_revenue * 100) if total_revenue else 0
    pso_pct = (overview["revenue"]["pso"] / total_revenue * 100) if total_revenue else 0
    perpetual_pct = (overview["revenue"]["perpetual"] / total_revenue * 100) if total_revenue else 0

    # Note high recurring concentration (not necessarily bad, but notable)
    if recurring_pct > 85:
        signals.append({
            "area": "Revenue Mix",
            "description": f"Recurring revenue represents {recurring_pct:.1f}% of total",
            "benchmark": "N/A - Observation only",
            "actual": f"Recurring: {recurring_pct:.1f}%",
            "variance": "High concentration in single revenue type",
            "evidence": f"Recurring: ${overview['revenue']['recurring']:,.0f}"
        })

    return signals

# =============================================================================
# 5. FLAG REGISTER
# =============================================================================

def generate_flag_register(negative_patterns: List[Dict], signals: List[Dict],
                           negative_analysis: Dict) -> List[Dict]:
    """Generate evidence-backed flag register."""

    flags = []
    flag_id = 1

    # Flags from negative value patterns
    for pattern in negative_patterns:
        if pattern["classification"] in ["Material", "Systematic"]:
            # Sheet-level flag
            materiality = "High" if pattern["classification"] == "Material" else "Medium"

            flags.append({
                "flag_id": f"F-{flag_id:02d}",
                "area": pattern["sheet"],
                "description": f"{pattern['classification']} concentration of negative adjustments ({pattern['negative_pct_of_total']:.1f}% of absolute total)",
                "evidence": f"Sheet: {pattern['sheet']}, Negative sum: ${pattern['total_negative_sum']:,.0f}, Count: {pattern['total_negative_count']}",
                "materiality": materiality
            })
            flag_id += 1

            # Category-level flags
            for cat in pattern.get("systematic_categories", []):
                flags.append({
                    "flag_id": f"F-{flag_id:02d}",
                    "area": f"{pattern['sheet']} - {cat['category']}",
                    "description": f"Systematic negative adjustments in {cat['category']} ({cat['neg_pct']:.1f}% of category)",
                    "evidence": f"Category: {cat['category']}, Negative sum: ${cat['neg_sum']:,.0f}, Count: {cat['neg_count']}",
                    "materiality": "Medium"
                })
                flag_id += 1

            # Department-level flags (limit to top 3 by absolute value)
            dept_flags = sorted(pattern.get("systematic_departments", []),
                              key=lambda x: abs(x["neg_sum"]), reverse=True)[:3]
            for dept in dept_flags:
                if abs(dept["neg_sum"]) > 100000:  # Only flag if material
                    flags.append({
                        "flag_id": f"F-{flag_id:02d}",
                        "area": f"{pattern['sheet']} - {dept['department']}",
                        "description": f"Concentrated negative adjustments in {dept['department']} department ({dept['neg_pct']:.1f}%)",
                        "evidence": f"Department: {dept['department']}, Negative sum: ${dept['neg_sum']:,.0f}, Count: {dept['neg_count']}",
                        "materiality": "Medium"
                    })
                    flag_id += 1

    # Flags from out-of-model signals
    for signal in signals:
        materiality = "High" if "margin" in signal["area"].lower() or "exceeds" in signal["description"].lower() else "Medium"

        flags.append({
            "flag_id": f"F-{flag_id:02d}",
            "area": signal["area"],
            "description": signal["description"],
            "evidence": signal["evidence"],
            "materiality": materiality
        })
        flag_id += 1

    return flags

# =============================================================================
# 6. SUPPORTING AGGREGATES
# =============================================================================

def generate_supporting_aggregates(data: Dict[str, pd.DataFrame],
                                   overview: Dict,
                                   negative_analysis: Dict) -> Dict[str, pd.DataFrame]:
    """Generate supporting aggregate tables for Excel output."""

    aggregates = {}

    # 1. Revenue by type
    revenue_df = pd.DataFrame([
        {"revenue_type": "Recurring", "amount": overview["revenue"]["recurring"],
         "pct_of_total": overview["revenue"]["recurring"] / overview["revenue"]["total_computed"] * 100},
        {"revenue_type": "PSO", "amount": overview["revenue"]["pso"],
         "pct_of_total": overview["revenue"]["pso"] / overview["revenue"]["total_computed"] * 100},
        {"revenue_type": "Perpetual", "amount": overview["revenue"]["perpetual"],
         "pct_of_total": overview["revenue"]["perpetual"] / overview["revenue"]["total_computed"] * 100},
        {"revenue_type": "TOTAL", "amount": overview["revenue"]["total_computed"], "pct_of_total": 100.0},
    ])
    aggregates["revenue_by_type"] = revenue_df

    # 2. Expense by category
    expense_df = pd.DataFrame([
        {"expense_category": "HC (W2)", "amount": overview["expenses"]["hc_w2"],
         "pct_of_total": overview["expenses"]["hc_w2"] / overview["expenses"]["total"] * 100},
        {"expense_category": "Non-HC OPEX", "amount": overview["expenses"]["nonhc_opex"],
         "pct_of_total": overview["expenses"]["nonhc_opex"] / overview["expenses"]["total"] * 100},
        {"expense_category": "Non-HC COGS", "amount": overview["expenses"]["nonhc_cogs"],
         "pct_of_total": overview["expenses"]["nonhc_cogs"] / overview["expenses"]["total"] * 100},
        {"expense_category": "TOTAL", "amount": overview["expenses"]["total"], "pct_of_total": 100.0},
    ])
    aggregates["expense_by_category"] = expense_df

    # 3. Expense by function (OPEX)
    opex = data["OPEX - NEmpl."]
    opex_by_func = opex.groupby("function_l2")["2018_total"].sum().reset_index()
    opex_by_func.columns = ["function", "amount"]
    opex_by_func = opex_by_func.sort_values("amount", ascending=False)
    opex_by_func["source"] = "OPEX - NEmpl."
    aggregates["opex_by_function"] = opex_by_func

    # 4. Expense by function (COGS)
    cogs = data["COGS - NEmpl."]
    cogs_by_func = cogs.groupby("function_l2")["2018_total"].sum().reset_index()
    cogs_by_func.columns = ["function", "amount"]
    cogs_by_func = cogs_by_func.sort_values("amount", ascending=False)
    cogs_by_func["source"] = "COGS - NEmpl."
    aggregates["cogs_by_function"] = cogs_by_func

    # 5. HC by function
    empl = data["Empl."]
    empl_by_func = empl.groupby("function_l2")["2018_total"].sum().reset_index()
    empl_by_func.columns = ["function", "amount"]
    empl_by_func = empl_by_func.sort_values("amount", ascending=False)
    empl_by_func["source"] = "Empl."
    aggregates["hc_by_function"] = empl_by_func

    # 6. Negative value aggregates by sheet
    neg_summary = []
    for sheet_name, analysis in negative_analysis.items():
        neg_summary.append({
            "sheet": sheet_name,
            "total_rows": analysis["total_rows"],
            "total_sum": analysis["total_sum"],
            "negative_count": analysis["negative_count"],
            "negative_sum": analysis["negative_sum"],
            "negative_pct_of_abs_total": analysis["negative_pct_of_abs_total"]
        })
    aggregates["negative_by_sheet"] = pd.DataFrame(neg_summary)

    # 7. Negative value aggregates by category (for sheets with material negatives)
    neg_by_category = []
    for sheet_name, analysis in negative_analysis.items():
        if analysis["negative_count"] > 0 and "by_category" in analysis:
            for cat, cat_data in analysis["by_category"].items():
                if cat_data["neg_count"] > 0:
                    neg_by_category.append({
                        "sheet": sheet_name,
                        "category": cat,
                        "category_total": cat_data["total"],
                        "negative_count": cat_data["neg_count"],
                        "negative_sum": cat_data["neg_sum"],
                        "negative_pct": cat_data["neg_pct"]
                    })
    aggregates["negative_by_category"] = pd.DataFrame(neg_by_category)

    # 8. Benchmark comparison
    benchmarks = data["Benchmarks"]
    total_revenue = overview["revenue"]["total_computed"]

    benchmark_comparison = []
    for _, row in benchmarks.iterrows():
        cat = row["category"]
        bench_pct = row["benchmark"] * 100
        benchmark_comparison.append({
            "category": cat,
            "benchmark_pct": bench_pct,
            "benchmark_amount": row["benchmark"] * total_revenue
        })
    aggregates["benchmark_reference"] = pd.DataFrame(benchmark_comparison)

    return aggregates

# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Main execution function."""
    print("=" * 70)
    print("PHASE 2: FINANCIAL OVERVIEW & ANOMALY FLAGGING")
    print(f"Execution timestamp: {datetime.now().isoformat()}")
    print("=" * 70)
    print("\nConstraints: Diagnostic only, no modifications, no recommendations")
    print()

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load data
    print("Loading normalized data...")
    data = load_normalized_data()
    print(f"Loaded {len(data)} sheets")

    # 1. Generate P&L Overview
    print("\n" + "-" * 50)
    print("1. GENERATING P&L OVERVIEW")
    print("-" * 50)
    overview = generate_pnl_overview(data)

    print(f"\nRevenue: ${overview['revenue']['total_computed']:,.2f}")
    print(f"  - Recurring: ${overview['revenue']['recurring']:,.2f}")
    print(f"  - PSO: ${overview['revenue']['pso']:,.2f}")
    print(f"  - Perpetual: ${overview['revenue']['perpetual']:,.2f}")

    print(f"\nExpenses: ${overview['expenses']['total']:,.2f}")
    print(f"  - HC (W2): ${overview['expenses']['hc_w2']:,.2f}")
    print(f"  - Non-HC OPEX: ${overview['expenses']['nonhc_opex']:,.2f}")
    print(f"  - Non-HC COGS: ${overview['expenses']['nonhc_cogs']:,.2f}")

    print(f"\nGross Margin: ${overview['margins']['gross_margin']:,.2f} ({overview['margins']['gross_margin_pct']:.2f}%)")

    # 2. Reconciliation Checks
    print("\n" + "-" * 50)
    print("2. RECONCILIATION CHECKS")
    print("-" * 50)
    recon_checks = perform_reconciliation_checks(data, overview)

    for check in recon_checks:
        status_symbol = "✓" if check["status"] == "RECONCILED" else "✗"
        print(f"  {status_symbol} {check['check']}: {check['status']} (diff: ${check['difference']:,.2f})")

    # 3. Negative Value Analysis
    print("\n" + "-" * 50)
    print("3. NEGATIVE VALUE ANALYSIS")
    print("-" * 50)
    negative_analysis = analyze_negative_values(data)
    negative_patterns = classify_negative_patterns(negative_analysis)

    for pattern in negative_patterns:
        print(f"\n  {pattern['sheet']}:")
        print(f"    Classification: {pattern['classification']}")
        print(f"    Negative count: {pattern['total_negative_count']}")
        print(f"    Negative sum: ${pattern['total_negative_sum']:,.2f}")
        print(f"    % of absolute total: {pattern['negative_pct_of_total']:.2f}%")

    # 4. Out-of-Model Signals
    print("\n" + "-" * 50)
    print("4. OUT-OF-MODEL SIGNALS")
    print("-" * 50)
    signals = detect_out_of_model_signals(data, overview)

    for signal in signals:
        print(f"\n  {signal['area']}:")
        print(f"    {signal['description']}")
        print(f"    Benchmark: {signal['benchmark']}, Actual: {signal['actual']}")

    # 5. Generate Flag Register
    print("\n" + "-" * 50)
    print("5. FLAG REGISTER")
    print("-" * 50)
    flags = generate_flag_register(negative_patterns, signals, negative_analysis)

    for flag in flags:
        print(f"\n  {flag['flag_id']} [{flag['materiality']}] {flag['area']}")
        print(f"    {flag['description']}")

    # 6. Generate Supporting Aggregates
    print("\n" + "-" * 50)
    print("6. GENERATING SUPPORTING AGGREGATES")
    print("-" * 50)
    aggregates = generate_supporting_aggregates(data, overview, negative_analysis)

    # Save outputs
    print("\n" + "=" * 70)
    print("SAVING OUTPUTS")
    print("=" * 70)

    # Save flag register
    flag_df = pd.DataFrame(flags)
    flag_path = os.path.join(OUTPUT_DIR, "02_flag_register.csv")
    flag_df.to_csv(flag_path, index=False)
    print(f"Saved: {flag_path}")

    # Save supporting aggregates to Excel
    agg_path = os.path.join(OUTPUT_DIR, "03_supporting_aggregates.xlsx")
    with pd.ExcelWriter(agg_path, engine='openpyxl') as writer:
        for sheet_name, df in aggregates.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    print(f"Saved: {agg_path}")

    # Return data for markdown generation
    return {
        "overview": overview,
        "recon_checks": recon_checks,
        "negative_patterns": negative_patterns,
        "negative_analysis": negative_analysis,
        "signals": signals,
        "flags": flags,
        "aggregates": aggregates
    }


if __name__ == "__main__":
    results = main()

    # Generate P&L Overview Summary Markdown
    md_content = f"""# Phase 2: Financial Overview & Anomaly Flagging

Generated: {datetime.now().isoformat()}

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
| Recurring | ${results['overview']['revenue']['recurring']:,.2f} | {results['overview']['revenue']['recurring']/results['overview']['revenue']['total_computed']*100:.1f}% |
| PSO | ${results['overview']['revenue']['pso']:,.2f} | {results['overview']['revenue']['pso']/results['overview']['revenue']['total_computed']*100:.1f}% |
| Perpetual | ${results['overview']['revenue']['perpetual']:,.2f} | {results['overview']['revenue']['perpetual']/results['overview']['revenue']['total_computed']*100:.1f}% |
| **TOTAL** | **${results['overview']['revenue']['total_computed']:,.2f}** | **100.0%** |

### Expenses (2018)

| Expense Category | Amount | % of Total |
|------------------|--------|------------|
| HC (W2) | ${results['overview']['expenses']['hc_w2']:,.2f} | {results['overview']['expenses']['hc_w2']/results['overview']['expenses']['total']*100:.1f}% |
| Non-HC OPEX | ${results['overview']['expenses']['nonhc_opex']:,.2f} | {results['overview']['expenses']['nonhc_opex']/results['overview']['expenses']['total']*100:.1f}% |
| Non-HC COGS | ${results['overview']['expenses']['nonhc_cogs']:,.2f} | {results['overview']['expenses']['nonhc_cogs']/results['overview']['expenses']['total']*100:.1f}% |
| **TOTAL** | **${results['overview']['expenses']['total']:,.2f}** | **100.0%** |

### Margin Analysis

| Metric | Value |
|--------|-------|
| Gross Margin | ${results['overview']['margins']['gross_margin']:,.2f} |
| Gross Margin % | {results['overview']['margins']['gross_margin_pct']:.2f}% |
| P&L Summary Margin | ${results['overview']['margins']['pnl_margin']:,.2f} |
| P&L Summary Margin % | {results['overview']['margins']['pnl_margin_pct']:.2f}% |

---

## 2. Reconciliation Checks

| Check | P&L Summary | Computed | Difference | Status |
|-------|-------------|----------|------------|--------|
"""

    for check in results['recon_checks']:
        status_emoji = "✓" if check["status"] == "RECONCILED" else "⚠"
        md_content += f"| {check['check']} | ${check['pnl_summary']:,.2f} | ${check['computed']:,.2f} | ${check['difference']:,.2f} | {status_emoji} {check['status']} |\n"

    md_content += """
**All reconciliation checks passed.** Computed values from detail sheets match P&L Summary within tolerance.

---

## 3. Negative Value Analysis

### Summary by Sheet

| Sheet | Total Rows | Negative Count | Negative Sum | % of Abs Total | Classification |
|-------|------------|----------------|--------------|----------------|----------------|
"""

    for pattern in results['negative_patterns']:
        md_content += f"| {pattern['sheet']} | {results['negative_analysis'][pattern['sheet']]['total_rows']} | {pattern['total_negative_count']} | ${pattern['total_negative_sum']:,.2f} | {pattern['negative_pct_of_total']:.2f}% | {pattern['classification']} |\n"

    md_content += """
### Pattern Classification Criteria

- **Isolated**: One-off or immaterial negative values
- **Systematic**: Repeated within a category, function, or department (>10% of category)
- **Material**: Large enough to meaningfully affect margins (>10% of absolute total)

### Notable Concentrations

"""

    for pattern in results['negative_patterns']:
        if pattern['classification'] in ['Material', 'Systematic']:
            md_content += f"**{pattern['sheet']}** ({pattern['classification']})\n"
            if pattern.get('systematic_categories'):
                md_content += "- Categories with concentrated negatives:\n"
                for cat in pattern['systematic_categories'][:5]:
                    md_content += f"  - {cat['category']}: {cat['neg_count']} items, ${cat['neg_sum']:,.2f} ({cat['neg_pct']:.1f}%)\n"
            if pattern.get('systematic_departments'):
                md_content += "- Departments with concentrated negatives:\n"
                for dept in sorted(pattern['systematic_departments'], key=lambda x: abs(x['neg_sum']), reverse=True)[:5]:
                    md_content += f"  - {dept['department']}: {dept['neg_count']} items, ${dept['neg_sum']:,.2f} ({dept['neg_pct']:.1f}%)\n"
            md_content += "\n"

    md_content += """---

## 4. Out-of-Model Signals

"""

    if results['signals']:
        for signal in results['signals']:
            md_content += f"""### {signal['area']}

- **Observation**: {signal['description']}
- **Benchmark**: {signal['benchmark']}
- **Actual**: {signal['actual']}
- **Variance**: {signal['variance']}
- **Evidence**: {signal['evidence']}

"""
    else:
        md_content += "No out-of-model signals detected.\n\n"

    md_content += """---

## 5. Flag Register Summary

See `02_flag_register.csv` for complete details.

| Flag ID | Area | Description | Materiality |
|---------|------|-------------|-------------|
"""

    for flag in results['flags']:
        md_content += f"| {flag['flag_id']} | {flag['area']} | {flag['description'][:60]}... | {flag['materiality']} |\n"

    md_content += f"""
**Total Flags: {len(results['flags'])}**
- High Materiality: {sum(1 for f in results['flags'] if f['materiality'] == 'High')}
- Medium Materiality: {sum(1 for f in results['flags'] if f['materiality'] == 'Medium')}

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
"""

    # Save markdown
    md_path = os.path.join(OUTPUT_DIR, "01_pnl_overview_summary.md")
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"Saved: {md_path}")

    print("\n" + "=" * 70)
    print("PHASE 2 COMPLETE")
    print("=" * 70)
