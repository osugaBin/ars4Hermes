# Systematic Review Mode — Protocol

## 5-Phase PRISMA-Compliant Pipeline

```
User: "Systematic review of [topic]"
     |
=== Phase 1: SCOPING ===
     |
     |-> Formulate PICOS RQ
     |   - Population, Intervention, Comparator, Outcome, Study design
     |   - Explicit eligibility criteria (inclusion/exclusion)
     |
     |-> Design Search Strategy
     |   - Multi-database, documented strategy
     |   - Pre-specified date range, language limits
     |
     +-> Review with User
         - Confirm RQ + eligibility criteria before Phase 2
     |
=== Phase 2: INVESTIGATION ===
     |
     |-> Search + Screen
     |   - Multi-angle web_search
     |   - Dual-pass screening (title -> full text)
     |   - Document excluded studies with reasons
     |
     |-> Source Verification
     |   - Predatory journal screening
     |   - Quality grading per source_quality_hierarchy.md
     |
     +-> Risk of Bias (simplified)
         - Per-study: Selection / Performance / Detection / Attrition
         - Traffic-light: Low / Some Concerns / High
     |
=== Phase 3: ANALYSIS ===
     |
     |-> Narrative Synthesis (always)
     |   - Thematic grouping of findings
     |   - Direction of effect across studies
     |
     |-> Optional: Quantitative synthesis if feasible
     |   - Heterogeneity assessment
     |   - Subgroup analysis considerations
     |
     +-> GRADE certainty assessment
         - High / Moderate / Low / Very Low per outcome
     |
=== Phase 4: COMPOSITION ===
     |
     +-> Write PRISMA-compliant report
         - PRISMA flow diagram (text-based)
         - Study characteristics table
         - Risk of bias summary
         - GRADE summary table
     |
=== Phase 5: REVIEW ===
     |
     +-> Integrity check:
         - Citation verification gate
         - Frame lock check (both sides presented?)
         - AI research failure mode check
```

## Checkpoint Rules

1. PICOS question must be confirmed before Phase 2
2. Risk of bias assessed for all included studies before Phase 3
3. GRADE assessment required for every reported outcome
4. PRISMA checklist items (27 items) should be traceable in the report
5. Every citation must be verified as resolvable

## PRISMA Flow Diagram (text format for reports)

```
Records identified through search (N)
  │
  ├── Duplicates removed (N)
  │
  ├── Records screened (N)
  │   ├── Excluded at title/abstract (N, with reasons)
  │   └── Full text assessed (N)
  │       ├── Excluded (N, with reasons)
  │       └── Included in synthesis (N)
  │           ├── Included in narrative synthesis (N)
  │           └── Included in quantitative synthesis (N, if applicable)
```
