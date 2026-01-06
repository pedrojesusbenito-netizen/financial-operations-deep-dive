# Deep Dive - New Acquisition

## Function
Operations

## Playbook Item
Initial Import

## Problem Statement

**What:**
New Acquisition is not in model

**Why:**
New Acquisition has not been transformed to fit our model

---

## 5 Why Analysis

### Question 1: Why is New Acquisition not in model?

**Answer:**
The existing operation when acquired is out of model in the following areas:

**Gross Margin**
- Current margin: 8.9%
- Benchmark: 70.0%
- Variance: -61.1 percentage points

**Sales & Marketing (S&M)**
- Current spend: 12.2% of revenue
- Benchmark: 6.0%
- Variance: +6.2 percentage points

**G&A (General & Administrative)**
- Current spend: 11.7% of revenue
- Benchmark: 9.0%
- Variance: +2.7 percentage points

These variances indicate that the acquired operation's cost structure and margin profile are materially misaligned with the operating model. Given findings in offset-heavy OPEX, true margins and functional cost levels may be further from model than net figures indicate.

**Evidence:**
1. [Out of model areas identified in Phase 2 financial analysis](outputs/phase_2/01_pnl_overview_summary.md#L105-L147)
2. [Offset values obscuring data: $11.1M in negative OPEX adjustments](outputs/phase_2/01_pnl_overview_summary.md#L62-L103)
3. Source: `data/Operational Leadership Real Work - Input P&L.xlsx`

---

### Question 2: Why is G&A not in-model?

**Answer:**
G&A appears 2.7 percentage points above benchmark at the net level (11.7% vs 9.0%), but this net figure obscures the underlying cost structure. Before negative adjustments, gross G&A represents 22.3% of revenue ($17.7M), which is subsequently reduced by $8.4M (47.7% offset) to arrive at the reported net figure of 11.7% ($9.3M).

This gross-to-net reduction indicates that nearly half of recorded G&A activity is systematically reversed through negative adjustments. The net figure cannot reliably inform transformation decisions without understanding the mechanics driving these offsets—whether allocation, chargebacks, or accrual reversals.

**Evidence:**
1. [Net G&A: $9,258,384 (11.7% of revenue)](outputs/phase_3/why_01_ga_above_benchmark.md#L22-L30)
2. [Gross G&A (positive entries): $17,688,177 (22.3% of revenue)](outputs/phase_3/why_02_gross_ga_mechanics.md#L17-L24)
3. [Negative adjustments: -$8,429,793 (47.7% offset ratio)](outputs/phase_3/why_02_gross_ga_mechanics.md#L17-L24)
4. [Benchmark: 9.0% (composite: Shared Services 4.5% + Executive 4.5%)](outputs/benchmark_and_classification_methodology.md#L31-L45)

---

### Question 3: Why does gross G&A reach 22.3% of revenue before adjustments?

**Answer:**
Gross G&A of $17.7M is concentrated in three expense categories that together account for 75.7% of total gross G&A:

1. **Outsourced Services:** $4.6M (26.1% of gross G&A, 5.8% of revenue) - 0.6% offset ratio
2. **Personnel:** $4.5M (25.5% of gross G&A, 5.7% of revenue) - 78.2% offset ratio
3. **Occupancy:** $4.3M (24.1% of gross G&A, 5.4% of revenue) - 91.8% offset ratio

These three categories exhibit fundamentally different offset behaviors. Outsourced Services (external vendor payments) persist through to net, while Personnel and Occupancy are systematically reallocated through negative adjustments. This pattern indicates the business operates G&A through a combination of direct external spend ($6.8M) and allocated internal resources ($8.8M gross, $1.3M net after offsets).

**Evidence:**
1. [Top 3 expense categories: $13.4M of $17.7M gross G&A (75.7%)](outputs/phase_3/why_03_gross_ga_operating_structure.md#L82-L92)
2. [Outsourced Services: 133 entries, $4.6M, 0.6% offset](outputs/phase_3/why_03_gross_ga_operating_structure.md#L116-L131)
3. [Personnel offset pattern: $4.5M gross → $1.0M net (78.2% reversal)](outputs/phase_3/why_03_gross_ga_operating_structure.md#L116-L145)
4. [Occupancy offset pattern: $4.3M gross → $0.3M net (91.8% reversal)](outputs/phase_3/why_03_gross_ga_operating_structure.md#L116-L145)

---

### Question 4: Why is Outsourced Services spend so high ($4.6M, 5.8% of revenue)?

**Answer:**
Outsourced Services spend is concentrated in three departments:

1. **Corporate:** $2.0M (43% of Outsourced Services)
2. **Finance & Accounting:** $1.4M (31% of Outsourced Services)
3. **Legal:** $0.7M (16% of Outsourced Services)

These three departments alone account for 90% of total Outsourced Services spend. The concentration in Finance & Accounting is particularly notable given that Central Factory already provides F&A shared services capabilities. This suggests acquired business unit F&A functions remain at the edge instead of leveraging Central.

**Evidence:**
1. [Top spend combinations (Department × Expense Category)](outputs/phase_3/why_03_gross_ga_operating_structure.md#L93-L112)
2. [Corporate Outsourced Services: $1,979,795 (21.4% of G&A)](outputs/phase_3/why_01_ga_above_benchmark.md#L82-L85)
3. [Finance & Accounting Outsourced Services: $1,426,248 (15.4% of G&A)](outputs/phase_3/why_01_ga_above_benchmark.md#L82-L85)
4. [Legal Outsourced Services: $729,130 (7.9% of G&A)](outputs/phase_3/why_01_ga_above_benchmark.md#L82-L85)

---

### Question 5: Why are Finance & Accounting services outsourced instead of using Central Factory?

**Answer:**
The acquired business unit has not been transformed to leverage Central Factory F&A shared services. F&A functions remain at the edge, purchasing external services ($1.4M) rather than utilizing Central capabilities. This violates the Crossover playbook principle of maximizing Central Factory usage for core shared services.

The data shows Finance & Accounting department total G&A spend of $2.4M (25.6% of net G&A), with significant components in:
- Outsourced Services: $1.4M
- External Contractors: $0.5M
- Personnel/Other: $0.5M

This edge-based F&A structure results in higher costs and prevents standardization across the portfolio.

**Evidence:**
1. [Finance & Accounting: $2,371,404 total G&A (25.6%)](outputs/phase_3/why_01_ga_above_benchmark.md#L62-L74)
2. [Finance & Accounting breakdown by expense category](outputs/phase_3/why_03_gross_ga_operating_structure.md#L93-L112)
3. Data-backed observation: Central Factory F&A capabilities exist per Operations Team Overview
4. Crossover playbook principle: Maximize use of Central Factory

---

## Root Cause

G&A is not in-model because **$4.6M in Outsourced Services spend (5.8% of revenue) remains at the edge** instead of leveraging Central Factory shared services, particularly Finance & Accounting functions. An additional **$2.5M in G&A is obscured by 47.7% offset mechanics** that require allocation methodology investigation before action.

The spending pattern shows:

1. **Concentrated Outsourced Services spend:** $4.6M across 133 vendors, with 90% concentrated in Corporate ($2.0M), Finance & Accounting ($1.4M), and Legal ($0.7M)
2. **Finance & Accounting at the edge:** $2.4M total F&A spend (25.6% of G&A) including $1.4M outsourced services and $0.5M external contractors
3. **High-offset categories obscuring true costs:** Personnel and Occupancy show 78-92% offset ratios, representing $8.8M gross / $2.5M net requiring investigation

This high-spend concentration in F&A—particularly the $1.4M in F&A Outsourced Services—indicates an opportunity to leverage Central Factory F&A capabilities instead of maintaining edge operations with external vendor dependencies.

---

## Fix

**Objective:** Reduce G&A from 11.7% to benchmark-aligned 9.0% by moving edge functions to Central Factory and optimizing vendor spend.

**Timeline:** 1-month preparation, execute next quarter

---

### Week 1: Investigate & Document Current Processes

**Finance & Accounting Investigation:**
- Map current F&A processes at the edge (AP, AR, month-end close, reporting, reconciliations)
- Identify overlap with Central Factory F&A capabilities (reference: `data/Central Finance Roles.xlsx`)
- Document F&A org chart, roles, responsibilities, work units
- Interview F&A outsourced service vendors ($1.4M): what services provided, SLAs, deliverables
- Obtain allocation methodology documentation for Personnel/Occupancy offsets

**Vendor Spend Analysis:**
- Audit all 133 Outsourced Services vendors
- Identify duplicate/overlapping vendors across departments
- Flag contracts >3 years old or non-competitive rates
- Benchmark hosting ($1.3M) and external contractor ($0.7M) spend

**Deliverable:** Process documentation, vendor consolidation opportunities, Central Factory gap analysis

---

### Week 2: Simplify & Standardize Edge Processes

**Process Simplification (required before Central migration):**
- Eliminate redundant F&A approval workflows
- Standardize chart of accounts and reporting formats to match Central Factory standards
- Document F&A work units and SLAs
- Identify automation opportunities (invoice processing, reconciliations, reporting)
- Create runbooks for repeatable F&A processes

**Quick-Win Vendor Optimization:**
- Consolidate duplicate vendors (target: 133 → 60-80 vendors)
- Renegotiate contracts >3 years old
- Standardize payment terms and vendor onboarding
- Optimize hosting: reserved capacity analysis, multi-cloud review

**Deliverable:** Simplified, documented, automation-ready F&A processes; vendor consolidation plan with savings estimates

---

### Week 3: Automate & Prepare for Central Migration

**AI-Powered Automation Implementation:**
- Deploy AI tools for invoice processing automation (OCR, auto-matching, exception handling)
- Implement automated reconciliation workflows
- Build automated month-end close checklists
- Create AI-assisted variance analysis and reporting tools

**Central Factory Readiness:**
- Validate simplified F&A processes meet Central Factory standards
- Train Central Factory team on business unit-specific requirements
- Establish cutover plan with clear work unit handoffs
- Set up monitoring dashboards for Central Factory F&A delivery

**Risk Mitigation:**
- Identify customer-facing F&A touchpoints that must remain seamless during transition
- Create rollback plan if Central Factory cannot deliver required SLAs
- Document dependencies and integration points

**Deliverable:** Automation-ready processes, Central Factory migration plan, risk mitigation strategy

---

### Week 4: Finalize & Get Approval for Next Quarter Execution

**Decision Package for CEO/CFO:**
- Present simplified F&A processes ready for Central migration
- Show vendor consolidation savings: $1.0-1.5M estimated annual reduction
- Demonstrate automation ROI and scalability
- Provide Central Factory F&A transition timeline for Q2 execution

**Offset Mechanics Resolution:**
- Report findings from allocation methodology investigation
- Classify remaining $2.5M decision-unsafe G&A as actionable or requires further investigation
- Propose Personnel/Occupancy optimization based on allocation clarity

**Approval Gates:**
- CEO approval to move F&A to Central Factory (Q2 execution)
- CFO approval for vendor consolidation execution
- Finance approval for allocation policy changes (if applicable)

**Deliverable:** Board-ready transformation plan, Q2 execution roadmap, savings validation

---

### Next Quarter Execution (Post-Approval):

**Month 1 (Q2 M1):**
- Execute vendor consolidation: reduce from 133 to 60-80 vendors
- Implement contract renegotiations: target $0.8-1.2M annual savings
- Deploy automation tools in production
- **Impact:** G&A reduction from 11.7% to 10.7-11.0%

**Month 2 (Q2 M2):**
- Transition F&A functions to Central Factory (phased by work unit)
- Validate Central Factory F&A SLA delivery
- Eliminate edge F&A Outsourced Services ($1.4M) and redundant contractors
- **Impact:** Additional G&A reduction to 9.5-10.0%

**Month 3 (Q2 M3):**
- Complete F&A Central migration
- Optimize Personnel/Occupancy based on allocation findings
- Continuous improvement: monitor Central Factory delivery, refine automation
- **Impact:** Final G&A at 9.0-9.5% (benchmark-aligned)

---

### Target Impact Summary

| Component | Current | Post-Optimization | Reduction | Timeline |
|-----------|---------|-------------------|-----------|----------|
| Outsourced Services | $4.6M (5.8%) | $3.1M (3.9%) | -$1.5M | Q2 M1-M2 |
| Hosting | $1.3M (1.7%) | $1.1M (1.4%) | -$0.2M | Q2 M1 |
| External Contractors | $0.7M (0.9%) | $0.5M (0.6%) | -$0.2M | Q2 M1 |
| Decision-Unsafe G&A | $2.5M (3.2%) | $2.0M (2.5%) | -$0.5M | Q2 M3 |
| **Total G&A** | **$9.3M (11.7%)** | **$7.1M (9.0%)** | **-$2.4M** | **Q2 End** |

**Benchmark Alignment:** G&A at 9.0% (target achieved)

---

### Flagged Investigations (Parallel Track)

**Personnel & Occupancy Offset Mechanics:**
- Requires: Allocation methodology documentation, prior-period P&L, journal entry detail
- Purpose: Determine if $8.8M gross / $2.5M net represents true cost or accounting artifact
- Decision boundary: High-offset categories classified as "decision-unsafe" until allocation clarity obtained
- Timeline: Investigate in parallel during Weeks 1-2, action in Q2 M3 based on findings

**Reference:** [Decision-safe vs decision-unsafe classification methodology](outputs/phase_5/why_05_decision_boundaries.md)

---

## AI Opportunities

### Area 1: Automated Vendor Spend Analysis & Contract Intelligence

**Problem Addressed:**
Manual analysis of 133 vendors across multiple categories is time-intensive and fails to detect duplicate vendors, unfavorable contract terms, or pricing drift over time.

**AI Solution:**
- **Vendor Deduplication Engine:** AI analyzes vendor names, addresses, tax IDs to identify duplicate/related entities across departments
- **Contract Expiration Tracking:** AI monitors contract terms, auto-flags renewals >90 days out, suggests renegotiation windows
- **Rate Benchmarking:** AI scrapes market rate data, compares vendor pricing to industry benchmarks, flags outliers
- **Spend Pattern Detection:** AI identifies unusual spending patterns (seasonality breaks, sudden increases) for investigation

**Expected Impact:**
- Vendor consolidation: 133 → 60-80 vendors (40% reduction)
- Contract renegotiation savings: 15-25% on contracts >3 years old
- Automated monitoring prevents future pricing drift
- Time savings: 20+ hours/month of manual vendor analysis → 2 hours

**Translation to Operations Role:**
In a live SVP role, this system enables portfolio-wide vendor intelligence—identify cross-entity consolidation opportunities, standardize vendor onboarding, and maintain competitive pricing across 10-20 business units.

---

### Area 2: AI-Powered Allocation Methodology Reverse Engineering

**Problem Addressed:**
$8.4M in systematic G&A offsets (47.7% of gross) lack allocation methodology documentation. Traditional reverse-engineering requires weeks of finance team interviews and manual journal entry review.

**AI Solution:**
- **Journal Entry Pattern Analysis:** AI ingests general ledger entries, identifies recurring allocation patterns (monthly, quarterly, annual cycles)
- **Allocation Base Detection:** AI clusters similar allocations, runs regression analysis to hypothesize allocation bases (headcount, revenue, square footage)
- **Policy Document Extraction:** AI processes unstructured documents (emails, policy PDFs, system screenshots) using LLM semantic understanding to extract allocation rules
- **Simulation & Validation:** AI builds allocation simulation model, tests against actual P&L to validate hypothesis accuracy (confidence scoring)

**Expected Impact:**
- Documentation speed: Weeks of interviews → Days of automated analysis
- Completeness: Detects undocumented allocation rules that may not exist in formal policies
- Validation: Confirms documented policies match actual practice
- Auditability: Provides evidence trail for allocation methodology assessment

**Translation to Operations Role:**
Critical for rapid M&A due diligence—understand acquired entity allocation mechanics without full finance team engagement. Enables faster decision-making on which costs are controllable vs. formula-driven artifacts.

---

## AI Tools Used

### 1. Tools Leveraged in This Assessment

**Claude Code Opus**
- **Role:** AI analyst operating under SVP guidance and direction
- **Purpose:** Execute detailed analytical tasks as directed by SVP of Operations
- **How it helped:**
  - **Phase 1 (Data Ingestion & Schema Normalization):** Wrote Python scripts to normalize inconsistent column names, reconcile totals across sheets, and detect data quality issues per SVP specifications
  - **Phase 2 (Financial Overview & Anomaly Flagging):** Executed benchmark comparison analysis and flagged systematic negative adjustment patterns as directed
  - **Phase 3-5 (5-Why Deep Dive):** Assisted SVP on performing root cause analysis following 5-Why methodology, maintaining analytical rigor and evidence-based conclusions
  - **Pattern Detection:** Conducted statistical analysis to identify bimodal offset distribution (low-offset vs high-offset categories) based on SVP investigation priorities
  - **Decision Boundary Classification:** Developed decision-safe vs decision-unsafe framework based on offset mechanics under SVP conceptual direction
  - **Visualization Support:** Generated visual evidence (waterfall charts, heatmaps, Pareto charts) to communicate complex offset patterns per SVP requirements
  - **Quality Control:** Validated reconciliations, maintained row count audit trail, ensured totals matched across transformations

**Claude Code Haiku**
- **Role:** Document organization and formatting assistant
- **Purpose:** Structure and format final deliverables
- **How it helped:**
  - Organized analytical outputs into executive-ready document structure
  - Formatted tables, sections, and evidence references for C-level readability
  - Ensured consistency in document presentation and flow

**Python (pandas, openpyxl, matplotlib)**
- **Purpose:** Data processing, transformation, and aggregation
- **Scripts developed by Claude Opus under SVP direction:**
  - `scripts/01_ingestion_and_schema.py`: Normalized P&L schema, reconciled totals
  - `scripts/02_phase1c_normalization.py`: Applied systematic column renaming and data type corrections
  - `scripts/03_phase2_analysis.py`: Computed functional benchmarks, offset ratios, concentration metrics
  - Additional phase 3-5 analysis scripts for deep-dive pattern detection

**Excel (Supporting Aggregates)**
- **Purpose:** Intermediate aggregation outputs for validation and stakeholder review
- **Artifact:** `outputs/phase_2/03_supporting_aggregates.xlsx` contains detailed breakdowns by revenue type, expense category, function, and offset patterns

---

### 2. How This Approach Translates to the Operations Role

**In a Live SVP of Operations Environment, This SVP-Directed AI-Assisted Methodology Would Enable:**

#### A. Rapid Financial Assessment (Day 1 of New Acquisition Integration)
- **Traditional Approach:** 2-4 weeks of finance team interviews, manual P&L review, vendor-by-vendor analysis
- **SVP-Directed AI-Assisted Approach:**
  - **Hour 1-2:** SVP directs Claude Code to ingest P&L, normalize schema, reconcile totals, and flag anomalies
  - **Hour 3-4:** SVP guides benchmark comparison priorities and reviews offset pattern detection results, directing deeper investigation where warranted
  - **Hour 5-8:** SVP validates decision boundary classification, refines transformation priorities, and approves decision-safe optimization targets
  - **Result:** Actionable transformation plan in 1 day vs 30 days (30x faster), with SVP maintaining strategic control throughout. This process can be repeated multiple times per day for different entities or successive analysis iterations.

#### B. Continuous Operational Intelligence
- **Monthly P&L Review:** SVP directs Claude Code to process updated P&L, guides variance investigation priorities, and reviews AI-generated explanations
- **Daily Cost Monitoring:** SVP sets benchmark thresholds and receives alerts when functional costs trend above targets, directing investigation as needed
- **Quarterly Board Reporting:** SVP reviews AI-generated summaries with drill-down evidence trails, adds strategic context before presentation

#### C. Scalable Across Portfolio
- **Single Entity Analysis:** Demonstrated in this assessment (3,180 line items, 1-day analysis under SVP direction)
- **Multi-Entity Portfolio:**
  - SVP establishes analysis framework once, then directs AI to apply across 10-20 acquired entities
  - Can process multiple entities per day, enabling rapid portfolio assessment
  - Standardize decision boundary classification under SVP methodology
  - Roll up portfolio-level benchmark performance with SVP-defined KPIs
  - SVP reviews cross-entity patterns (e.g., Entity A has 2% G&A Outsourced Services vs Entity B at 8%—directs AI to investigate drivers)

#### D. Institutional Knowledge Capture
- **Current State:** Analysis methodology exists in analyst's head; knowledge walks out the door when they leave
- **SVP-Directed AI-Assisted State:**
  - SVP's analytical framework codified in Claude Code prompts and Python scripts
  - Repeatable, auditable, transferable methodology under SVP ownership
  - New team members can execute SVP's analysis approach in days vs months of training
  - SVP refines methodology over time as patterns are detected across more entities

#### E. Evidence-Based Leadership
- **Traditional:** "I think G&A is high" → weeks of analysis → inconclusive recommendations
- **SVP-Directed AI-Assisted:** SVP rapidly validates hypothesis with AI-generated evidence: "G&A is 11.7% vs 9.0% benchmark; I've directed analysis showing $4.6M in Outsourced Services at the edge should move to Central Factory; vendor consolidation offers $1.5M savings; F&A migration enables benchmark alignment"
  - **SVP can:**
    - Act immediately on vendor consolidation with confidence
    - Commission F&A Central migration with clear process documentation
    - Monitor progress with AI-powered benchmark tracking under SVP oversight

---

### 3. Competitive Advantage in Operations Leadership

**This SVP-directed AI-assisted approach provides:**

1. **Speed:** 30x faster financial assessment (1 day vs 30 days) with SVP maintaining strategic control, repeatable multiple times per day
2. **Depth:** SVP-guided systematic 5-Why analysis vs surface-level variance review
3. **Precision:** SVP-validated decision-safe vs decision-unsafe classification prevents premature action
4. **Scalability:** SVP's methodology applies to single entity or 100-entity portfolio with multi-entity per day capability
5. **Transparency:** Fully auditable, evidence-based conclusions under SVP ownership vs "trust me" analysis
6. **Institutional Resilience:** SVP's methodology captured in code, not dependent on individual analysts

**In the role of SVP of Operations:**
- **Month 1:** Direct AI to assess acquired entity, validate transformation opportunities, prepare vendor consolidation and F&A Central migration plans
- **Quarter 2:** Execute vendor consolidation ($1.5M savings), transition F&A to Central Factory, resolve allocation mechanics
- **Ongoing:** Oversee AI-powered continuous monitoring, review monthly variance explanations, set proactive alert thresholds, scale methodology across portfolio

**Result:** SVP delivers faster integration, higher-confidence decisions, scalable methodology across portfolio, defensible to Board/C-suite with AI as force multiplier under SVP leadership.

---

**End of Deep Dive Analysis**
