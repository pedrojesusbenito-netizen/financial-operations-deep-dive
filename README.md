# README: Financial Operations Deep Dive - Assessment Analysis

**Author:** Pedro Benito  
**Date:** January 6, 2026  
**Assessment:** Operational Leadership Real Work - Deep Dive Exercise  
**Repository:** financial-operations-deep-dive

---

## Executive Summary

This repository contains a comprehensive financial analysis of a newly acquired business unit, executed using AI-assisted methodology with Claude Code. The analysis identifies $2.4M in G&A optimization opportunities (moving from 11.7% to 9.0% of revenue) by transitioning Finance & Accounting functions from edge operations to Central Factory.

**Key Finding:** The business unit's G&A appears 2.7 percentage points above benchmark at the net level (11.7% vs 9.0%), but this obscures a more complex picture—gross G&A of $17.7M (22.3% of revenue) is reduced by $8.4M (47.7%) through systematic negative adjustments. This analysis establishes which expenses are "decision-safe" (actionable now) versus "decision-unsafe" (requiring process visibility before action).

---

## What This Analysis Accomplishes

### Primary Deliverable
A board-ready Deep Dive (DD) that:
- ✓ Identifies root causes for out-of-model G&A expenses using 5-Why methodology
- ✓ Proposes moving Finance & Accounting functions to Central Factory
- ✓ Quantifies $2.4M in savings opportunities with realistic execution timeline
- ✓ Identifies AI opportunities for vendor intelligence and allocation reverse-engineering
- ✓ Demonstrates AI-first operational analysis methodology scalable across portfolio

### Secondary Deliverables
- Audit-grade data quality validation (57 QC checks, 100% pass rate)
- Methodological transparency documentation for third-party review
- Reusable analytical framework for rapid M&A due diligence
- Visual analytics suite for executive communication

---

## Analysis Process Overview

### Phase 1: Data Ingestion & Normalization (Foundation)
**Objective:** Establish trustworthy analytical foundation before drawing conclusions

**Key Activities:**
1. **Header Detection & Schema Normalization** - Identified metadata rows across 9 sheets, normalized column naming conventions (Function L1 → function_l1)
2. **Duplicate Column Analysis** - Validated that two "Dept" columns contained semantically different data (department vs. expense_category)
3. **Data Quality Assessment** - Identified floating point precision artifacts, 100% null columns, negative value patterns
4. **Normalization Proposal** - Created formal proposal document with 5 rules (3 mandatory, 2 optional) requiring SVP approval before execution
5. **QC Validation** - Generated 11 validation artifacts confirming row counts, null counts, sum totals unchanged post-normalization

**Why This Matters:** Most analysts start analyzing immediately and discover data quality issues when conclusions are questioned. I invested upfront in validation to ensure every downstream conclusion was defensible.

**Key Decision:** Proposed optional rounding rule but explicitly recommended NOT applying it without approval, preserving full precision for auditability. This decision prioritized defensibility over cosmetic cleanliness.

**Artifacts:** `notes/assumptions.md`, `notes/phase_1b_findings.md`, `notes/phase_1c_execution_log.md`, `outputs/qc/*.csv`

---

### Phase 2: Financial Overview & Anomaly Flagging (Discovery)
**Objective:** Systematic identification of out-of-model areas before investigating root causes

**Key Activities:**
1. **P&L Reconciliation** - Validated computed aggregates match P&L Summary within tolerance
2. **Benchmark Comparison** - Constructed composite benchmarks (G&A = Shared Services 4.5% + Executive 4.5% = 9.0%)
3. **Negative Value Analysis** - Classified negative adjustments by materiality and concentration
4. **Flag Register Creation** - Generated 16 flags across 3 materiality levels with specific evidence

**Why This Matters:** Created a systematic inventory of anomalies rather than jumping to the most obvious issue. This prevented tunnel vision and ensured comprehensive assessment.

**Key Decision:** Applied benchmarks to NET values (standard practice) but flagged this as a limitation requiring investigation. This set up the critical discovery in Phase 3 that gross G&A is 22.3% before 47.7% offsets.

**Artifacts:** `outputs/phase_2/01_pnl_overview_summary.md`, `outputs/phase_2/02_flag_register.csv`, `outputs/phase_2/03_supporting_aggregates.xlsx`

---

### Phase 3-5: 5-Why Root Cause Analysis (Deep Dive)
**Objective:** Progressive narrowing from symptom to actionable root cause

**Why Chain:**
1. **Why #1:** Why is G&A above benchmark (11.7% vs 9.0%)? → Identified $2.1M variance concentrated in Outsourced Services (49.6% of net G&A)
2. **Why #2:** Why does gross G&A reach 22.3% before adjustments? → Discovered 47.7% offset ratio, three categories account for 75.7% of gross
3. **Why #3:** What operating structure is implied by gross G&A footprint? → Found bimodal offset pattern (low <10% vs high >50%), external costs persist while internal allocations reverse
4. **Why #4:** Why are large volumes of G&A systematically reversed? → Created 5 visualizations showing block-structured offset patterns, not random corrections
5. **Why #5:** What can be treated as decision-safe vs decision-unsafe? → Established classification framework based on offset behavior and counterparty type

**Why This Matters:** Each Why builds logically on the previous answer, progressively narrowing scope. The chain closes at a natural boundary—where the data alone cannot answer further questions without process documentation.

**Key Decision:** Created "decision-safe vs decision-unsafe" classification framework (Why #5). This was NOT in the original assessment instructions but emerged as necessary to handle epistemic uncertainty in financial data where 47.7% of activity is systematically reversed. This framework enables immediate action on low-offset external spend ($4.6M Outsourced Services) while flagging high-offset internal allocations ($8.8M) as requiring allocation methodology documentation before optimization.

**Artifacts:** `outputs/phase_3/why_01_ga_above_benchmark.md` through `why_03_gross_ga_operating_structure.md`, `outputs/phase_4_visuals/why_04_reversal_mechanics.md`, `outputs/phase_5/why_05_decision_boundaries.md`

---

### Methodology Disclosure (Auditability)
**Objective:** Enable third-party validation of analytical logic without re-running analysis

**Key Activities:**
1. Documented benchmark source (exclusively from provided P&L benchmark sheet)
2. Explained composite benchmark construction (G&A, S&M, R&D)
3. Disclosed expense classification logic (function_l2 filtering rules)
4. Explained treatment of offsets (benchmarks applied to NET values)
5. Stated methodological boundaries (what data supports vs cannot answer)

**Why This Matters:** A CEO needs to defend this analysis to a board. An auditor needs to validate the methodology. A future analyst needs to replicate or extend the work. This document makes all of that possible.

**Key Decision:** Explicitly documented where conclusions rely on accounting representations (e.g., "If offsets represent allocation artifacts rather than true cost reductions, benchmark variances would differ"). This intellectual honesty strengthens credibility rather than weakening it.

**Artifacts:** `outputs/benchmark_and_classification_methodology.md`

---

## Key Technical Decisions & Rationale

### 1. Version Control for Financial Analysis
**Decision:** Used Git with systematic commits after each phase  
**Rationale:** Creates audit trail, enables rollback if needed, demonstrates analytical progression  
**Alternative Considered:** Single final commit - rejected because it loses analytical narrative  

### 2. Normalization Approval Gates
**Decision:** Created proposal document requiring explicit approval before executing transformations  
**Rationale:** Financial data transformations are high-stakes—wrong normalization invalidates all downstream analysis  
**Alternative Considered:** Apply "safe" transformations automatically - rejected because "safe" is subjective  

### 3. Decision-Safe/Unsafe Classification Framework
**Decision:** Created binary classification based on offset behavior, counterparty type, and transactional clarity  
**Rationale:** 47.7% of G&A is systematically reversed—cannot confidently optimize without understanding why  
**Alternative Considered:** Treat all G&A as actionable - rejected because high-offset categories may be allocation artifacts, not true economic costs  

### 4. Visualization-Led Why #4
**Decision:** Created 5 custom visualizations (waterfall, heatmap, Pareto) before writing narrative  
**Rationale:** Offset patterns are complex—visuals reveal block structure that tables cannot  
**Alternative Considered:** Tables only - rejected because patterns harder to communicate to executives  

### 5. Benchmark Application to NET Values
**Decision:** Applied benchmarks to net G&A (11.7%) not gross (22.3%)  
**Rationale:** Standard practice in financial analysis, enables apples-to-apples comparison  
**Trade-off:** Acknowledged limitation that net figures may obscure true activity if offsets are allocation artifacts  

---

## What I Would Do Differently

### If I Could Start Over

**1. Earlier Pattern Recognition**
I discovered the 47.7% offset ratio in Why #2 (after already analyzing net figures in Why #1). If I had run an offset analysis in Phase 2, I could have flagged decision-unsafe categories earlier and focused investigation on decision-safe spend immediately.

**Learning:** Always analyze offset/reversal patterns before benchmark comparisons when dealing with P&Ls that include negative adjustments.

**2. More Concise Visualization Narrative**
Why #4 contains 5 visualizations with detailed "What the visual shows" descriptions. While thorough, this could be more concise for executive consumption—possibly a 1-page visual summary + detailed appendix structure.

**Learning:** Executives want insight-per-square-inch density. Consider "executive summary visual" + "analytical detail visual" pairs.

**3. Vendor Consolidation Quick Win Analysis**
The DD identifies $4.6M in Outsourced Services across 133 vendors but doesn't drill into vendor consolidation opportunities until the Fix section. A Phase 3 "Why" focused on vendor fragmentation (e.g., "Why 133 vendors for $4.6M spend?") could have strengthened the vendor consolidation recommendation.

**Learning:** When concentration analysis reveals fragmentation (133 vendors), investigate before jumping to functional transformation (moving to Central).

### If I Had More Time

**1. Prior-Period Comparison**
The single-period P&L creates irreducible uncertainty around high-offset categories. If a prior-period P&L existed, I could validate whether offset patterns are stable, growing, or anomalous—which would shift items from decision-unsafe to decision-safe.

**What I'd Do:** Request Q3 2018 P&L (if available) and analyze offset pattern consistency across periods.

**2. Department-Level Deep Dives**
Finance & Accounting is identified as the transformation target ($2.4M, 25.6% of G&A) but could benefit from deeper analysis:
- What specific F&A processes exist at the edge? (AP, AR, close, reporting, reconciliations)
- Which processes overlap with Central Factory capabilities?
- What's the detailed org chart and role mapping?

**What I'd Do:** Create "DD within a DD" for F&A department specifically, with work-unit-level granularity.

**3. Allocation Methodology Hypothesis Testing**
Why #4 offers three hypotheses for reversal mechanics (allocation/reallocation, chargebacks, accrual reversals) but doesn't attempt to discriminate between them using available data patterns.

**What I'd Do:** Analyze reversal timing patterns (e.g., do they occur monthly, quarterly, annually?), reversal size distributions, and department-to-department flow patterns to narrow hypothesis space.

---

## Tools & Methodology

### AI Tools Used

**Claude Code Opus (Primary Analyst)**
- Role: Execute detailed analytical tasks under SVP direction
- Usage: Data ingestion scripts, statistical analysis, pattern detection, visualization generation, QC validation
- Methodology: I provided structured phase-by-phase direction; Claude executed technical implementation

**Claude Code Haiku (Document Formatting)**
- Role: Structure and format final deliverables
- Usage: Executive document formatting, table cleanup, section organization

**Python Ecosystem (Technical Foundation)**
- pandas: Data transformation and aggregation
- openpyxl: Excel file I/O
- matplotlib: Visualization generation

### Methodological Approach

**SVP-Directed AI-Assisted Analysis**
I maintained strategic control while leveraging AI for execution:
- I designed the phase structure (1 → 1b → 1c → 2 → 3 → 4 → 5)
- I wrote specific prompts defining scope, constraints, and deliverables for each phase
- I reviewed outputs and made approval decisions (e.g., which normalization rules to apply)
- I created novel frameworks (decision-safe/unsafe) based on patterns AI revealed

**Approval Gates & QC Discipline**
- Phase 1b: Created normalization proposal requiring explicit approval before execution
- Phase 1c: Executed only approved rules, generated validation confirming no data corruption
- Phase 2-5: Each phase included QC reconciliation against prior phases

**Audit Trail Maintenance**
- Git commits after each phase with descriptive messages
- QC artifacts documenting every transformation
- Methodology disclosure explaining analytical logic
- Explicit acknowledgment of limitations and boundaries

---

## How This Translates to the Operations Role

### Immediate Value (Month 1)
**Rapid Entity Assessment**
This methodology enables 1-day financial assessment of newly acquired entities:
- Day 1: Ingest P&L, normalize, reconcile, flag anomalies
- Day 2-3: Execute 5-Why investigation on top priority flags
- Day 4: Present actionable transformation plan to CEO/CFO

**Traditional approach:** 2-4 weeks of finance team interviews and manual analysis  
**AI-assisted approach:** 3-4 days with audit-ready documentation

### Scalable Value (Quarter 1+)
**Portfolio-Wide Operations Intelligence**
Once methodology is proven on one entity, it scales to the portfolio:
- Process 10-20 entities using same analytical framework
- Build cross-entity benchmarking dashboard (Entity A: 8% G&A vs Entity B: 14% G&A)
- Identify common optimization patterns (e.g., if 5 entities all have edge-based F&A, consolidate migration)
- Codify institutional knowledge in repeatable scripts

### Strategic Value (Year 1+)
**Acquisition Integration Velocity**
Trilogy's stated goal: acquire 1 company/week. This requires:
- **Day 1 assessment capability** - Determine if target is integrable (this methodology provides)
- **Rapid transformation playbooks** - Standardized approaches to moving functions Central (F&A migration template established)
- **Evidence-based prioritization** - Decision-safe/unsafe framework prevents wasted effort on non-actionable items

**Institutional Resilience**
Traditional operations knowledge exists in analysts' heads and walks out the door when they leave. This methodology captures knowledge in code:
- New team members execute SVP's analytical approach in days vs months of training
- Methodology improves over time as patterns detected across more entities
- SVP refines framework based on what works across portfolio, not just single entity

---

## Repository Structure

```
financial-operations-deep-dive/
├── README.md (this file)
├── data/
│   ├── Operational Leadership Real Work - Input P&L.xlsx
│   └── Central Finance Roles.xlsx
├── notes/
│   ├── assumptions.md (Phase 1 data ingestion decisions)
│   ├── phase_1b_findings.md (Validation & justification)
│   ├── phase_1b_normalization_proposal.md (Transformation rules proposal)
│   └── phase_1c_execution_log.md (Execution log with QC results)
├── outputs/
│   ├── benchmark_and_classification_methodology.md (Methodology disclosure)
│   ├── qc/ (11 QC validation artifacts)
│   ├── phase_2/ (Financial overview, flag register, aggregates)
│   ├── phase_3/ (Why #1-#3 analysis documents)
│   ├── phase_4_visuals/ (5 visualizations + Why #4 narrative)
│   └── phase_5/ (Why #5 decision boundaries framework)
├── scripts/ (Python analysis scripts - generated by Claude Code)
└── Conversation.txt (Full AI conversation transcript)
```

---

## Key Insights & Learnings

### 1. Hidden Complexity in "Simple" Financial Data
The P&L appeared straightforward: G&A at 11.7% vs 9.0% benchmark, 2.7pp gap. Reality: gross G&A at 22.3% reduced by 47.7% through systematic offsets, creating irreducible uncertainty about true economic costs.

**Learning:** Always investigate negative adjustments and offset patterns before making optimization recommendations. Net figures can obscure rather than reveal true activity.

### 2. Decision Boundaries Are Not Weakness
Explicitly stating "I cannot confidently optimize Personnel and Occupancy categories without allocation methodology documentation" feels like admitting failure. In reality, it prevents costly mistakes (optimizing accounting artifacts rather than true costs) and focuses effort on actionable items.

**Learning:** Intellectual honesty about boundaries strengthens credibility with executives who have seen too many consultants overclaim certainty.

### 3. Visualization Changes Conversation
Tables showing offset ratios by category are defensible but forgettable. A heatmap showing red (high-offset) and green (low-offset) blocks creates instant pattern recognition and executive comprehension.

**Learning:** Invest in visualization for complex patterns. The 30 minutes creating the offset ratio heatmap paid for itself in communication value.

### 4. Methodology Documentation Is Strategic Asset
The benchmark_and_classification_methodology.md document is not wasted time. Value:
- CEO can defend analysis to board without me in the room
- Auditor can validate without re-running
- Future analyst can extend methodology to next entity
- Institutional knowledge captured, not lost when I leave

**Learning:** Documentation is not overhead—it's strategic investment in organizational capability.

---

## Success Metrics

**Assessment Deliverables (Met)**
- ✓ Deep Dive template completed with 5-Why analysis reaching root cause
- ✓ Proposed moving at least one function closer to in-model (F&A to Central)
- ✓ Identified AI opportunities (vendor intelligence, allocation reverse-engineering)
- ✓ Demonstrated Claude Code usage (documented in Conversation.txt)
- ✓ Avoided all antipatterns (no "planning to have a plan," no dumping bad processes on Central)
- ✓ CEO-presentation quality (board-ready with audit trail)

**Technical Quality Metrics (Achieved)**
- 57 invariant checks: 100% pass rate
- 10 sum reconciliation checks: 100% pass rate
- 6 P&L cross-validation checks: 100% pass rate
- 0 data integrity issues discovered post-analysis

**Analytical Depth (Demonstrated)**
- 5 Why questions (exceeded minimum 3)
- 16 anomaly flags identified and classified by materiality
- 3,180 line items analyzed across 9 sheets
- 11 QC artifacts generated for auditability
- 5 executive visualizations created
- 1 novel framework invented (decision-safe/unsafe)

---

## Closing Reflection

This assessment challenged me to think like an SVP of Operations—not just analyzing a business, but building a methodology that scales across a portfolio. The decision-safe/unsafe framework emerged from necessity: when 47.7% of G&A is systematically reversed and I don't know why, I need a principled way to separate "act now" from "investigate first."

The AI-first approach enabled depth and speed I couldn't achieve manually: 57 QC checks executed in seconds, 5 visualizations generated in minutes, methodology captured in reusable code. But the strategic decisions—what to investigate, when to stop, what's decision-safe—remained human judgment.

I'm proud of this work not because it's perfect, but because it's honest about its limitations while being actionable within those boundaries. That's the balance I'd bring to the SVP of Operations role: move fast where data supports confidence, slow down where uncertainty requires caution, and always build systems that enable others to move fast later.

---

**Contact:** Pedro Benito  
**Repository:** github.com/[username]/financial-operations-deep-dive  
**Assessment Date:** January 6, 2026
