# Why #5: Decision-Safe vs Decision-Unsafe G&A Classification

**Question**: What portion of G&A can be treated as decision-safe vs decision-unsafe given the observed offset mechanics?

---

## A. Decision-Safe G&A Components

### Defining Characteristics

Spend qualifies as **decision-safe** when it exhibits the following properties:

1. **Near-zero offset ratio** — The gross amount recorded approximates the net amount retained, indicating minimal or no reversal activity
2. **External counterparty** — The spend represents cash-out transactions to third parties, not internal transfers
3. **Transactional clarity** — The expense reflects a discrete service or asset acquisition with identifiable commercial terms

### Categories Exhibiting Decision-Safe Patterns

Based on offset behavior established in prior Whys, categories demonstrating near-zero reversal include:

- **Outsourced Services** — External vendor payments for discrete deliverables
- **Hosting / Infrastructure** — Third-party platform and compute costs
- **External Contractors** — Non-employee labor acquired through commercial contracts

### Why These Do Not Depend on Allocation Mechanics

These categories persist through the offset process because:

- They represent **actual economic outflows** — cash leaves the entity to external parties
- They are **not subject to internal reallocation** — no intercompany or departmental transfer logic applies
- Their gross recording **equals their economic reality** — what is booked is what was spent

Acting on these figures does not require understanding internal allocation rules, chargeback structures, or accrual mechanics. The net figure is the economic figure.

---

## B. Decision-Unsafe G&A Components

### Defining Characteristics

Spend qualifies as **decision-unsafe** when it exhibits the following properties:

1. **High offset ratio** — A material portion of gross spend is reversed, indicating the net figure diverges significantly from the gross
2. **Internal or allocative nature** — The spend category is associated with shared resources, personnel, or facilities subject to cost distribution
3. **Structural reversal patterns** — Offsets occur in predictable, block-structured patterns suggesting systematic accounting treatment rather than ad hoc correction

### Categories Exhibiting Decision-Unsafe Patterns

Based on offset behavior established in prior Whys, categories demonstrating high or total reversal include:

- **Personnel / Compensation** — Subject to allocation across cost centers or legal entities
- **Occupancy / Facilities** — Frequently allocated based on headcount, square footage, or utilization formulas
- **Benefits** — Often pooled and redistributed across departments
- **Commissions** — May involve true-ups, clawbacks, or reallocation between periods or entities

### Why Offsets Materially Distort Economic Reality

For these categories, the **net figure may not represent true economic cost**:

- If reversals reflect **outbound allocations**, the net understates this entity's actual resource consumption (costs were pushed elsewhere)
- If reversals reflect **inbound allocation corrections**, the net may represent a residual after arbitrary distribution logic
- If reversals reflect **accrual true-ups**, the net conflates timing adjustments with underlying spend levels

The observable net figure is an **accounting residual**, not a clean measure of economic activity.

### Risks of Premature Action

Acting on decision-unsafe categories without process visibility introduces the following risks:

- **Misattribution** — Treating an allocation artifact as discretionary spend
- **Double-counting or under-counting** — If the same economic cost appears (or is netted) across multiple entities or periods
- **False precision** — Believing the net figure reflects controllable cost when it reflects formula-driven distribution
- **Unintended consequences** — Adjusting a figure that is mechanically derived from upstream inputs, not direct decisions

---

## C. Hard Boundaries of This P&L

### What This Dataset Can Definitively Support

1. **Identification of offset behavior by category and department** — The data reliably distinguishes high-offset from low-offset spend patterns
2. **Classification of spend into persistence vs reversal buckets** — Categories can be grouped by observed offset ratio with confidence
3. **Magnitude of gross-to-net reduction** — The aggregate scale of reversal activity is observable and consistent
4. **Structural vs random pattern determination** — The block-structured, bimodal distribution of offsets indicates systematic treatment, not error

### What This Dataset Fundamentally Cannot Answer

1. **Why reversals occur** — No allocation methodology, chargeback policy, or intercompany agreement is available to explain the mechanics
2. **Whether reversals are correct** — Without process documentation, it is not possible to assess if offset amounts are accurate or erroneous
3. **Period-over-period consistency** — No prior-period P&L exists to confirm whether offset patterns are stable, growing, or anomalous
4. **Direction of allocation flows** — It is not determinable whether this entity is a net sender or net receiver of allocated costs
5. **True economic cost of high-offset categories** — For decision-unsafe spend, the actual resource consumption by this entity remains unknown

### Irreducible Uncertainty

The absence of historical comparison and process documentation creates an **irreducible uncertainty band** around all high-offset categories. This uncertainty cannot be resolved through further analysis of this dataset alone.

---

## D. Implications for Next-Phase Diligence (Non-Prescriptive)

### Types of Process Visibility Required to Expand the Decision-Safe Perimeter

To move currently decision-unsafe categories into the decision-safe perimeter, the following types of visibility would be required:

1. **Allocation methodology documentation** — Written policies or system configurations defining how shared costs are distributed across cost centers or entities

2. **Intercompany or shared-services agreements** — Contractual or policy documents specifying chargeback rates, allocation bases, and settlement terms

3. **Prior-period P&L comparison** — At minimum, one additional period to assess whether offset patterns are stable or variable

4. **Journal entry detail for high-offset categories** — Transaction-level visibility into what drives the reversal entries (e.g., specific allocation runs, accrual reversals, manual adjustments)

5. **Cost center or entity hierarchy** — Structural information clarifying whether this P&L represents a standalone unit, a cost center within a larger entity, or an aggregation across multiple units

### What This Does Not Constitute

This section identifies **types of information** that would reduce uncertainty. It does not:

- Recommend a sequence of actions
- Assign owners or timelines
- Assert that such information exists or is obtainable
- Prioritize one type of visibility over another

---

## Closing Statement

This analysis establishes a **clean stopping point** for the current investigation. The P&L data supports confident action on decision-safe categories characterized by low offset ratios and external counterparties. It does not support confident action on decision-unsafe categories where offset mechanics materially distort the relationship between recorded and economic cost.

Further movement requires process visibility that is not present in this dataset.

**Why #5 analysis complete. Why-chain closed.**
