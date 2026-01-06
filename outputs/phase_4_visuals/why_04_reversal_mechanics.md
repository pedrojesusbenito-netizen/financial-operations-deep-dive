# Why #4: Process Mechanics Behind Gross G&A Reversals

**Question**: Why does this business record large volumes of G&A spend that are later reversed or offset at the department and expense-category level?

**Date**: 2026-01-06

---

## Executive Summary

The data shows that 47.7% of gross G&A ($8.4M of $17.7M) is systematically reversed through negative adjustments. This reversal activity is not uniformly distributed—it is concentrated in specific expense categories (Personnel, Occupancy, Commissions) and specific departments (Benefits, Occupancy). Other categories (Outsourced Services, Hosting) show near-zero reversal activity. The pattern is consistent with structured accounting or operational mechanisms rather than random corrections.

---

## I. Visual Findings

### Chart A: G&A Waterfall — Scale of Reversal

![Waterfall Chart](phase_4_visuals/A_waterfall_chart.png)

**What the visual shows:**
- Gross G&A of $17.7M (22.3% of revenue) is reduced by $8.4M in negative adjustments
- Net G&A lands at $9.3M (11.7% of revenue)
- The reversal represents 47.7% of gross—nearly half of recorded G&A is subsequently offset

---

### Chart B: Gross vs Net by Expense Category

![Gross vs Net by Category](phase_4_visuals/B_gross_vs_net_by_category.png)

**What the visual shows:**
- Three categories exhibit high offset behavior:
  - **Occupancy**: 92% offset ($4.3M gross → $0.3M net)
  - **Personnel**: 78% offset ($4.5M gross → $1.0M net)
  - **Commissions**: 82% offset ($18K gross → $3K net)
- Three categories exhibit near-zero offset:
  - **Outsourced Services**: 1% offset ($4.6M gross → $4.6M net)
  - **Hosting**: 0% offset ($1.3M gross → $1.3M net)
  - **External Contractors**: 1% offset ($0.7M gross → $0.7M net)
- **T&E/Other** shows partial offset (45%)

---

### Chart C: Offset Ratio Heatmap (Department × Category)

![Offset Heatmap](phase_4_visuals/C_offset_ratio_heatmap.png)

**What the visual shows:**
- **Red zones (high offset)** are concentrated in specific intersections:
  - Benefits × Personnel: 100% offset
  - Occupancy × Occupancy: 100% offset
  - Occupancy × T&E/Other: 100% offset
  - G&A × Personnel: 100% offset
- **Green zones (low offset)** span multiple departments:
  - Corporate × Outsourced Services: 0% offset
  - Finance & Accounting × Outsourced Services: 0% offset
  - Legal × Outsourced Services: 0% offset
  - Enterprise Systems × Hosting: 0% offset
- The pattern is **block-structured**, not random

---

### Chart D: Pareto Analysis with Offset Overlay

![Pareto Chart](phase_4_visuals/D_pareto_with_offset.png)

**What the visual shows:**
- The three largest expense categories by gross spend (Outsourced Services, Personnel, Occupancy) have **divergent offset behavior**:
  - Outsourced Services ($4.6M): 1% offset (green bar)
  - Personnel ($4.5M): 78% offset (red bar)
  - Occupancy ($4.3M): 92% offset (red bar)
- High-offset categories represent $8.8M (49.7%) of gross G&A but only $1.3M (14.4%) of net G&A
- Low-offset categories represent $6.8M (38.5%) of gross but $6.8M (73.1%) of net

---

### Chart E: Department-Level Gross vs Net

![Department Gross vs Net](phase_4_visuals/E_department_gross_vs_net.png)

**What the visual shows:**
- **Benefits** department: $3.1M gross, 100% offset, net ≈ $0
- **Occupancy** department: $4.1M gross, 96% offset, net = $0.2M
- **Corporate** department: $2.7M gross, 2% offset, net = $2.6M
- **Legal** department: $0.8M gross, 0% offset, net = $0.8M
- Departments cluster into two groups: those with minimal offset and those with near-complete offset

---

## II. Mechanical Inferences

The following mechanisms are **consistent with the observed patterns**. These are hypotheses, not conclusions.

### Hypothesis 1: Allocation and Reallocation Accounting

This pattern is consistent with a mechanism where:
- Costs are initially recorded in G&A (gross entry)
- A subsequent entry reallocates them to other cost centers (negative adjustment)
- The net G&A reflects only the portion not reallocated

This would explain why:
- Certain categories (Personnel, Occupancy) have high offset ratios
- The Benefits department shows 100% offset
- Outsourced Services shows minimal offset (external costs not reallocated)

### Hypothesis 2: Intercompany or Shared-Services Chargebacks

This pattern is consistent with a mechanism where:
- Shared-services costs are recorded in G&A
- Chargebacks to business units create offsetting negative entries
- Net G&A represents the portion not recovered via chargebacks

This would explain why:
- Department-level offsets are concentrated (Benefits, Occupancy)
- Category-level offsets are systematic (Personnel, Occupancy expense types)
- External vendor costs (Outsourced Services, Hosting) are not offset

### Hypothesis 3: Accrual Reversals or True-Ups

This pattern is consistent with a mechanism where:
- Costs are accrued based on estimates (gross entries)
- Actual costs differ from estimates, creating reversals
- High-volume transaction categories show more reversal activity

This would explain why:
- Personnel (payroll-related) shows high offset
- Occupancy (facility-related) shows high offset
- External contracted amounts (Outsourced Services) show minimal adjustment

---

## III. Boundary Conditions

### What the data does NOT support:

1. **Random error correction**: The offset pattern is too systematic and concentrated to be explained by ad-hoc corrections

2. **Uniform accounting treatment**: Different expense categories receive materially different offset treatment, indicating differentiated process mechanics

3. **Single-mechanism explanation**: The co-existence of 0% and 100% offset categories suggests multiple mechanisms may be operating simultaneously

4. **External vendor reversals**: Outsourced Services, Hosting, and External Contractors—all externally-sourced costs—show near-zero offset, suggesting reversals are concentrated in internally-sourced or allocated costs

---

## IV. Summary of Patterns

| Pattern | Evidence | Implication |
|---------|----------|-------------|
| Bimodal offset distribution | Categories cluster at <10% or >50% offset | Distinct process treatment by category |
| Department concentration | Benefits (100%), Occupancy (96%) nearly fully offset | Department-level mechanisms at work |
| External vs internal divergence | External costs (Outsourced Services, Hosting) persist; internal allocations (Personnel, Occupancy) reverse | Reversal activity tied to internal processes |
| Block structure in heatmap | Offset ratios form coherent blocks, not scattered points | Systematic, not random, reversal behavior |

---

## V. Visual Artifact References

| Chart | File | Purpose |
|-------|------|---------|
| A | `outputs/phase_4_visuals/A_waterfall_chart.png` | Scale of gross-to-net reduction |
| B | `outputs/phase_4_visuals/B_gross_vs_net_by_category.png` | Category-level persistence vs reversal |
| C | `outputs/phase_4_visuals/C_offset_ratio_heatmap.png` | Systematic patterns by dept × category |
| D | `outputs/phase_4_visuals/D_pareto_with_offset.png` | Concentration of reversal activity |
| E | `outputs/phase_4_visuals/E_department_gross_vs_net.png` | Department-level offset behavior |

---

## VI. Data Source References

- **Sheet**: `OPEX - NEmpl.`
- **Filter**: `function_l2 = "G&A"`
- **Positive entries**: 785 entries, $17,688,177
- **Negative entries**: 286 entries, -$8,429,793
- **Net**: 1,071 entries, $9,258,384

---

**Why #4 analysis complete. Awaiting SVP review for next Why.**
