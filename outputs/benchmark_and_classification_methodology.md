# Benchmark and Classification Methodology Disclosure

**Purpose**: To support review, auditability, and executive confidence by formally disclosing the methodology used in the financial analysis and 5-Why investigation.

**Scope**: This document describes *how* conclusions were derived. It does not revise, extend, or recommend actions.

---

## 1. Benchmark Reference Table (As Applied)

All benchmark values originate exclusively from the **Benchmarks** sheet of `data/Operational Leadership Real Work - Input P&L.xlsx`.

| Benchmark Name | Benchmark Percentage | Source Location |
|----------------|---------------------|-----------------|
| Margin | 70.0% | Benchmarks sheet, Row 1 |
| Shared Services | 4.5% | Benchmarks sheet, Row 2 |
| Executive team | 4.5% | Benchmarks sheet, Row 3 |
| Sales | 5.0% | Benchmarks sheet, Row 4 |
| Marketing | 1.0% | Benchmarks sheet, Row 5 |
| Technical Support | 2.0% | Benchmarks sheet, Row 6 |
| Hosting | 1.0% | Benchmarks sheet, Row 7 |
| Product | 2.0% | Benchmarks sheet, Row 8 |
| Engineering | 10.0% | Benchmarks sheet, Row 9 |
| Expense Total | 30.0% | Benchmarks sheet, Row 10 |

**No external or industry benchmarks were introduced.**

---

## 2. Functional Area Benchmark Construction

### G&A (General & Administrative)

```
Functional Area: G&A
Benchmark Construction: COMPOSITE
  - Shared Services: 4.5%
  - Executive Team: 4.5%
Composite Benchmark: 9.0%
Rationale: Combined representation of central administrative overhead.
           The P&L data contains a single "G&A" category under function_l2,
           which encompasses both shared services and executive functions.
           No granular breakdown exists in the source data to map these
           benchmark lines separately.
```

### S&M (Sales & Marketing)

```
Functional Area: S&M
Benchmark Construction: COMPOSITE
  - Sales: 5.0%
  - Marketing: 1.0%
Composite Benchmark: 6.0%
Rationale: The P&L data contains a single "S&M" category under function_l2,
           combining both sales and marketing expenses. The benchmark sheet
           provides separate Sales and Marketing lines, which were summed
           to create a comparable composite.
```

### R&D (Research & Development)

```
Functional Area: R&D
Benchmark Construction: COMPOSITE
  - Engineering: 10.0%
  - Product: 2.0%
Composite Benchmark: 12.0%
Rationale: The P&L data contains a single "R&D" category under function_l2.
           Engineering and Product benchmark lines were combined to create
           a comparable composite for R&D activities.
```

### Hosting

```
Functional Area: Hosting
Benchmark Construction: DIRECT 1:1 MAPPING
  - Hosting: 1.0%
Composite Benchmark: N/A (single line)
Rationale: Direct mapping where Hosting expenses in the P&L can be
           compared directly to the Hosting benchmark line.
```

### Technical Support

```
Functional Area: Technical Support
Benchmark Construction: DIRECT 1:1 MAPPING
  - Technical Support: 2.0%
Composite Benchmark: N/A (single line)
Rationale: Direct mapping available.
```

### Margin

```
Functional Area: Margin
Benchmark Construction: DIRECT 1:1 MAPPING
  - Margin: 70.0%
Composite Benchmark: N/A (single line)
Rationale: Direct comparison of computed margin percentage to benchmark.
```

---

## 3. Expense Classification Logic

### Source Data Structure

Expense data originates from three sheets:
- **OPEX - NEmpl.**: Non-headcount operating expenses
- **COGS - NEmpl.**: Non-headcount cost of goods sold
- **Empl.**: Headcount (W2) expenses

### Column Normalization Applied

| Original Column | Normalized Column | Notes |
|-----------------|-------------------|-------|
| Function L1 | function_l1 | Snake_case conversion |
| Function L2 | function_l2 | Snake_case conversion |
| Dept | department | First occurrence renamed |
| Dept.1 | expense_category | Second occurrence renamed to disambiguate |
| Vendor | vendor | Snake_case conversion |
| 2018 total | 2018_total | Snake_case conversion |

### Functional Area Classification

| Functional Area | Classification Rule | Source Sheet(s) |
|-----------------|---------------------|-----------------|
| G&A | `function_l2 = "G&A"` | OPEX - NEmpl. |
| S&M | `function_l2 = "S&M"` | OPEX - NEmpl., COGS - NEmpl. |
| R&D | `function_l2 = "R&D"` | OPEX - NEmpl. |

### G&A Classification Detail

G&A expenses were identified using the filter `function_l2 = "G&A"` applied to the OPEX - NEmpl. sheet.

**Departments included in G&A** (as present in source data):
- Benefits
- Finance & Accounting
- GMs & Office Admins
- Human Resources
- IT
- Legal
- Occupancy

**Expense categories included in G&A** (as present in source data):
- Commissions
- External Contractors
- Hosting / Other
- Legal Fees
- Occupancy
- Outsourced Services
- Personnel / Compensation
- Travel & Meals
- Other (miscellaneous categories)

### Rows Excluded from Benchmarking

No rows were excluded from benchmarking comparisons. All rows present in the source data sheets were included in aggregations.

### Handling of Ambiguous Rows

No manual overrides or assumptions were applied to row classification. Classification relied entirely on the `function_l2` column values as recorded in the source data.

---

## 4. Treatment of Offset and Negative Entries

### Benchmark Application Basis

**Benchmarks were applied to NET values.**

The `2018_total` column contains both positive (expense) and negative (offset/reversal) entries. When comparing functional areas to benchmarks:

- The sum of all `2018_total` values for the functional area was used
- This sum includes both positive and negative entries
- The resulting net figure was divided by total revenue to produce the percentage compared to benchmark

### Example: G&A Benchmark Comparison

```
G&A Gross (positive entries only): $17,688,177
G&A Negative (offset entries only): -$8,429,793
G&A Net (sum of all entries): $9,258,384
Total Revenue: $79,194,484
G&A as % of Revenue: 11.7%
Benchmark: 9.0%
Variance: +2.7 percentage points
```

### Consistency of Treatment

Offset-heavy categories and low-offset categories were treated consistently:

- All functional areas were compared to benchmarks using NET values
- No adjustments were made to isolate gross spend before comparison
- No functional areas were excluded due to high offset ratios

### Flagged Limitation

The use of net values for benchmark comparison was flagged as a limitation in the analysis:

- Net G&A (11.7%) was compared to benchmark (9.0%)
- However, gross G&A (22.3%) significantly exceeds the benchmark
- This limitation was explicitly investigated in the Why-chain (Whys #1-4)
- The decision-boundary analysis (Why #5) classified high-offset categories as "decision-unsafe" specifically because net figures may not represent true economic cost

---

## 5. Methodological Boundaries and Known Limitations

### What the Methodology Supports Confidently

1. **Identification of functional areas exceeding benchmarks** — Net values by function_l2 can be reliably compared to composite benchmarks derived from the provided benchmark sheet.

2. **Detection of systematic offset patterns** — Offset ratios by department and expense category were computed consistently and reveal structured reversal behavior.

3. **Classification of expense persistence** — Categories with near-zero offset ratios can be confidently identified as representing true economic cost.

4. **Reconciliation to P&L Summary** — Computed aggregates from detail sheets match P&L Summary values, confirming data integrity.

### Where Conclusions Rely on Accounting Representations

1. **Functional area boundaries** — Classification depends entirely on the `function_l2` values as recorded in the source data. If source data misclassifies expenses, the analysis inherits that misclassification.

2. **Benchmark composites** — The mapping of P&L functional areas to benchmark lines required judgment (e.g., G&A → Shared Services + Executive Team). Alternative mappings would produce different variance conclusions.

3. **Net vs Gross interpretation** — Benchmark comparisons used net values, which assume accounting offsets represent legitimate reductions. If offsets are erroneous or represent allocation artifacts rather than true cost reductions, benchmark variances would differ.

### Why Some Figures May Understate or Obscure True Activity

**Net G&A understates gross activity by 47.7%.**

- Gross G&A: $17.7M (22.3% of revenue)
- Net G&A: $9.3M (11.7% of revenue)
- Offset: $8.4M (47.7% of gross)

The offset mechanics distort visibility into true economic activity for high-offset categories. Specifically:

- **If offsets represent outbound allocations**: This entity's actual resource consumption is higher than net figures suggest (costs were pushed to other entities/cost centers).
- **If offsets represent inbound allocation corrections**: Net figures may represent accounting residuals after arbitrary distribution formulas.
- **If offsets represent accrual reversals**: Net figures conflate timing adjustments with underlying spend levels.

Without allocation methodology documentation or prior-period comparison, the true economic meaning of offset entries cannot be determined from this dataset.

---

## 6. Final Confirmation Statements

### G&A Benchmark Derivation

The G&A benchmark of **9.0%** was derived as follows:

| Component | Percentage | Source |
|-----------|------------|--------|
| Shared Services | 4.5% | Benchmarks sheet, Row 2 |
| Executive Team | 4.5% | Benchmarks sheet, Row 3 |
| **Composite Total** | **9.0%** | Arithmetic sum |

### Source Exclusivity

**Confirmed**: All benchmark values originate exclusively from the **Benchmarks** sheet of the provided P&L file (`data/Operational Leadership Real Work - Input P&L.xlsx`).

**Confirmed**: No external benchmarks, industry standards, or analyst estimates were introduced.

### Post-Analysis Integrity

**Confirmed**: No post-analysis benchmark reinterpretation was performed.

- Benchmark values were extracted once during Phase 2
- Composite benchmarks were constructed prior to variance analysis
- No benchmark values were adjusted after observing actual expense percentages
- The same benchmark constructs were applied consistently across all Whys

---

## Appendix: Benchmark-to-P&L Mapping Summary

| P&L Functional Area | Benchmark Component(s) | Mapping Type | Composite % |
|---------------------|------------------------|--------------|-------------|
| G&A | Shared Services + Executive Team | Composite | 9.0% |
| S&M | Sales + Marketing | Composite | 6.0% |
| R&D | Engineering + Product | Composite | 12.0% |
| Hosting | Hosting | Direct | 1.0% |
| Technical Support | Technical Support | Direct | 2.0% |
| Margin | Margin | Direct | 70.0% |
| Expense Total | Expense Total | Direct | 30.0% |

---

**Methodology disclosure complete.**
