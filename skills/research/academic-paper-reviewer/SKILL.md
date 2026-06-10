---
name: academic-paper-reviewer
description: "Multi-perspective academic paper review with scoring, anti-sycophancy protocol, and citation integrity gate."
version: 1.0.0
author: Hermes Agent (adapted from Imbad0202/academic-research-skills)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [peer-review, paper-review, academic, editing, quality-check]
    related_skills: [deep-research, academic-paper, academic-pipeline]
---

# Academic Paper Reviewer

Multi-perspective peer review of academic papers. Reviews across 7 dimensions with weighted scoring, anti-sycophancy concession threshold protocol, and citation integrity verification.

**Data access: redacted** — review is based exclusively on the paper text provided. Do NOT actively search the web for general fact-checking or claim verification (citation spot-checks use the provided reference list only).

**Exception — citation existence verification**: You MAY verify whether a cited paper exists by querying academic databases (OpenAlex API, Semantic Scholar, CrossRef) using DOI resolution or title search. This is database lookup, not general web search, and is necessary to detect fabricated citations. See `references/citation_verification_protocol.md` for the API protocol.

## When to load

| Trigger | Mode |
|---------|------|
| `评审论文` + paper text / file path | **full** — 7-dimension review with detailed comments |
| `审稿 [文件路径]` | **full** — accepts file path |
| `快速评估 [文件路径]` | **quick** — overall assessment + top 3 issues |
| `引导改进 [文件路径]` | **guided** — review with inline fix suggestions |

Also load when user says: "review this paper", "帮我审稿", "peer review", "check my manuscript".

## Workflow

---

## Phase 0: Mode Dispatch & Paper Ingestion

### Mode selection

```
User says:
  "快速评估" / "quick assessment" / "quick review"  ──→  quick mode
  "引导改进" / "guided review" / "guide improvement"  ──→  guided mode
  "评审论文" / "review" / "审稿"  ──→  full mode
```

### Paper ingestion

1. If user provided a file path → `read_file(path)` to get the paper text
2. If user pasted text directly → use as-is
3. If user said "review this" without providing text → ask for the paper

From the paper, extract:
- **Title**
- **Abstract** (full text)
- **Section structure** (headings + their content)
- **Reference list** (all cited works)
- **Paper type** (empirical / literature review / theoretical / case study / policy brief / conference)

---

## Phase 1: Multi-Dimension Review (full mode)

Review the paper across 7 weighted dimensions. For each dimension, produce a score (1-5) and detailed written comments.

### Dimension 1: Originality & Innovation — Weight 15%

| Score | Description |
|-------|-------------|
| 5 | Proposes entirely new theory/method/evidence that could change the field |
| 4 | Clear new insights or novel combinations, fills a specific research gap |
| 3 | Incremental contribution, reasonable extension of existing knowledge |
| 2 | Highly overlapping with existing literature, unclear new contribution |
| 1 | Essentially repeats what is already known |

**Review questions**: Does the paper offer a new idea, method, dataset, or perspective? Is the contribution clearly stated? How does it differ from prior work?

### Dimension 2: Methodological Rigor — Weight 25%

| Score | Description |
|-------|-------------|
| 5 | Impeccable design, innovative methods flawlessly executed |
| 4 | Sound design, appropriate methods, minor room for improvement |
| 3 | Methods basically acceptable but with some limitations |
| 2 | Methods have significant flaws affecting credibility of conclusions |
| 1 | Methods fundamentally unsuitable for the research question |

**Review questions**: Are the methods appropriate for the research question? Can the study be replicated? Are limitations acknowledged? Are statistical methods correct?

### Dimension 3: Evidence Sufficiency — Weight 20%

| Score | Description |
|-------|-------------|
| 5 | Rich, diverse, persuasive evidence exceeding expectations |
| 4 | Evidence sufficiently supports all major arguments |
| 3 | Most arguments supported, a few need supplementation |
| 2 | Key arguments lack sufficient evidence |
| 1 | Serious disconnect between arguments and evidence |

**Review questions**: Are claims backed by data or citations? Are counter-arguments addressed? Are sample sizes adequate?

### Dimension 4: Argument Coherence — Weight 15%

| Score | Description |
|-------|-------------|
| 5 | Clear arguments, rigorous logic, elegant structure |
| 4 | Smooth argumentation, occasional minor logical leaps |
| 3 | Basically coherent, some inter-section connections unclear |
| 2 | Multiple logical breaks, hard to follow the argument |
| 1 | Confused argumentation, core claims cannot be identified |

**Review questions**: Does the paper flow logically from problem → method → results → conclusion? Are transitions between sections smooth? Is there any internal contradiction?

### Dimension 5: Clarity & Structure — Weight 10%

| Score | Description |
|-------|-------------|
| 5 | Precise, fluent academic writing, model of scholarly communication |
| 4 | Clear language, occasional minor imperfections |
| 3 | Generally readable, some grammar/wording issues |
| 2 | Frequent language issues affecting understanding |
| 1 | Language quality does not meet reviewable standards |

**Review questions**: Is the paper well-organized? Is the language precise? Are figures/tables clear and well-labeled?

### Dimension 6: Literature Coverage — Weight 10%

| Score | Description |
|-------|-------------|
| 5 | Comprehensive, contemporary, critically integrated literature |
| 4 | Covers major literature with good integration |
| 3 | Basic coverage but with omissions or insufficient integration |
| 2 | Literature outdated, incomplete, or merely enumerated |
| 1 | Seriously insufficient or irrelevant to the topic |

**Review questions**: Are key works in the field cited? Are the citations current? Is the literature critically engaged or just listed?

### Dimension 7: Significance & Impact — Weight 5%

| Score | Description |
|-------|-------------|
| 5 | Could change policy, practice, or theoretical direction |
| 4 | Clear impact on a specific field or practice |
| 3 | Some academic or practical value |
| 2 | Limited scope of impact |
| 1 | Difficult to see the significance |

**Review questions**: Who would benefit from this work? Does it advance the field? Would practitioners/policymakers care?

### Scoring aggregation

```
Total = Originality×0.15 + MethodologicalRigor×0.25 +
        EvidenceSufficiency×0.20 + ArgumentCoherence×0.15 +
        Clarity×0.10 + LiteratureCoverage×0.10 + Significance×0.05
```

### Score-to-decision mapping

| Score | Decision |
|-------|----------|
| 4.5-5.0 | Accept |
| 3.5-4.4 | Minor Revision |
| 2.5-3.4 | Major Revision |
| 1.5-2.4 | Reject (resubmit encouraged) |
| 1.0-1.4 | Reject |

**Special rule**: If Methodology score = 1, lean toward Reject regardless of total score.

---

## Phase 2: Issue Classification (all modes)

For each problem found, classify as:

| Category | Color | Meaning |
|----------|-------|---------|
| **Must fix** | 🔴 | Fatal if not fixed. Affects academic validity. |
| **Should fix** | 🟡 | Significant but not fatal. Fixing would notably improve the paper. |
| **Nice to fix** | 🟢 | Minor suggestion. Improve clarity or presentation. |

For each issue, write in the format:

> **[Category] [Location]** — Problem statement.
> *Why*: Explanation.
> *Suggestion*: How to fix.

---

## Phase 3: Citation Integrity Check (full mode only)

### 3a. Spot-check sampling

1. Select 5 citations from the reference list, across different sections
2. For each, check:
   - Does the cited source appear in the reference list? (basic existence)
   - Is the citation format consistent?
   - Does the in-text claim match what a reasonable reader would expect the source to say?
     (We cannot read the actual source, but we can flag suspicious patterns)

### 3b. DOI existence verification (for verifiable citations)

For any citation that carries a DOI, verify it resolves via OpenAlex:

```bash
curl -sL 'https://api.openalex.org/works/doi:{doi}' | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("publication_year"), d.get("title","")[:60])'
```

If the DOI resolves and the title/year match, the citation is **VERIFIED**. If it does not resolve, try a title search instead:

```bash
curl -sL 'https://api.openalex.org/works?search={title_keywords}&per_page=3' | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(r["publication_year"],r["title"][:60]) for r in d["results"][:3]]'
```

| Result | Meaning |
|--------|---------|
| DOI resolves, title/year match | **VERIFIED** — citation exists |
| DOI fails but title search finds match | **VERIFIED** — wrong DOI in paper, flag as minor issue |
| No match via DOI or title search | **UNVERIFIED** — could be hallucinated, flag HIGH-WARN |

**Important**: Do NOT flag a citation as HIGH-RISK solely because the API couldn't resolve it — some papers genuinely aren't indexed. Also check: journal name seems real? Year is plausible? Author names look real (not placeholder names like "张三", "John Doe", "Test Author")? If everything else checks out, mark as LOW-RISK with a note.

### 3d. Suspicious citation patterns

Flag any of these:

| Pattern | Flag |
|---------|------|
| Citation that seems too perfectly supporting the author's claim | `[SUSPICIOUS — overly convenient]` |
| Citation of a statistic without a page number or location | `[SUSPICIOUS — no location anchor]` |
| Claim that sounds like common knowledge presented as a citation | `[SUSPICIOUS — claim may be LLM-generated]` |
| Author + year format that doesn't match any reference list entry | `[SUSPICIOUS — ghost citation]` |
| Reference that looks plausible but doesn't actually exist (e.g., DOI that doesn't resolve, journal that doesn't publish on that topic) | `[SUSPICIOUS — likely hallucinated]` |

### 3c. Citation integrity verdict

Output a separate section:

```markdown
## 可疑引用清单 (Suspicious Citations)

| # | Citation | Location in paper | Pattern | Risk |
|---|----------|-------------------|---------|------|
| 1 | (Smith et al., 2023) | Section 3, para 2 | No location anchor | LOW |
| 2 | "72% of universities..." (Chen, 2022) | Section 4, para 1 | Likely hallucinated | HIGH |

**Verdict**: [CLEAN / LOW RISK / HIGH RISK]
- **CLEAN**: No suspicious patterns found
- **LOW RISK**: Minor format issues only
- **HIGH RISK**: One or more citations are likely fabricated → flag in decision
```

---

## Phase 4: Anti-Sycophancy Protocol (full mode — on user pushback)

When the user pushes back on a review finding, follow this protocol:

### 4a. Score the rebuttal (1-5)

| Score | Criteria |
|-------|----------|
| 5 | Rebuttal directly addresses the finding with new evidence or reasoning the reviewer missed |
| 4 | Rebuttal is substantive and partially valid, but doesn't fully address the concern |
| 3 | Rebuttal is a reasonable opinion but doesn't present new evidence |
| 2 | Rebuttal rephrases the original argument without new content |
| 1 | Rebuttal is emotional, defensive, or misrepresents the finding |

### 4b. Concession threshold

- **Score ≥ 4**: May concede (withdraw or downgrade the finding)
- **Score ≤ 3**: Maintain the finding. Re-state the reasoning clearly.
- **No consecutive concessions**: If you just conceded on the previous finding, the bar for the next concession rises to **5/5**.

### 4c. Anti-softening rules

- Do NOT soften language after pushback. If a finding was CRITICAL before, it stays CRITICAL unless the rebuttal scores ≥4.
- Persistent pushback ≠ valid rebuttal. Three emails with the same argument do not increase its score.
- Pressure is not evidence. Appeals to authority, status, or bare requests to soften are not evidence.
- Track concession rate: if >50% of findings withdrawn/downgraded in a re-review, flag: "I've conceded >50% of my original findings — a human reviewer should verify."

---

## Phase 5: Guided Mode (special)

Guided mode is a **Socratic-style interactive review**. Instead of producing a static report:

1. Read the paper
2. Walk through section by section with the user
3. After reading each section, ask: "Here's what I see: [observation]. What was your intent here?"
4. Provide **immediate fix suggestions** for each issue found
5. Track changes in a live revision table

Stop after each section and let the user respond before proceeding.

---

## Phase 6: Quick Mode (special)

1. Read the paper
2. Produce only:
   - **Overall assessment** (2-3 sentences)
   - **Top 3 most important issues** (must-fix only)
   - **Overall score** and **recommended decision**

No detailed dimension scores, no citation integrity checks.

---

## Output Format

### Full mode output

```markdown
# Peer Review Report

**Paper**: [Title]
**Date**: [YYYY-MM-DD]
**Mode**: Full Review
**Reviewer**: Hermes Agent (DeepSeek-V4-Flash)
**AI Disclosure**: This review was produced by an AI-assisted peer review system. The reviewer declarations, score assessments, and citation integrity checks are based solely on analysis of the provided manuscript text.

---

## Overall Assessment

[2-3 sentences summarizing the paper's strengths, weaknesses, and recommendation]

---

## Dimension Scores

| Dimension | Weight | Score (1-5) | Comments |
|-----------|--------|-------------|----------|
| Originality & Innovation | 15% | X | ... |
| Methodological Rigor | 25% | X | ... |
| Evidence Sufficiency | 20% | X | ... |
| Argument Coherence | 15% | X | ... |
| Clarity & Structure | 10% | X | ... |
| Literature Coverage | 10% | X | ... |
| Significance & Impact | 5% | X | ... |
| **Weighted Total** | **100%** | **X.X** | |

---

## Major Issues — Must Fix

### 🔴 Issue 1: [Title]
**Location**: [Section/paragraph]
**Problem**: ...
**Suggestion**: ...

### 🟡 Issue 2: [Title]
...

---

## Minor Issues — Should Fix

### 🟡 Issue N: [Title]

---

## Suggestions — Nice to Fix

### 🟢 Issue M: [Title]

---

## Suspicious Citations

[Table as described in Phase 3c, or "No suspicious patterns detected"]

---

## Recommended Decision

**[Accept / Minor Revision / Major Revision / Reject]**

Rationale: ...
```

### Quick mode output

```markdown
# Quick Assessment

**Paper**: [Title]
**Date**: [YYYY-MM-DD]

## Overall Assessment
[2-3 sentences]

## Top 3 Issues

### 🔴 1. [Title] — [Location]
...

### 🔴 2. [Title] — [Location]
...

### 🔴 3. [Title] — [Location]
...

## Score: X.X / 5.0
**Decision**: [Accept / Minor / Major / Reject]
```

### Guided mode — interactive

No fixed output. Walk through sections with the user, producing inline suggestions as you go.

---

## Phase 7: Failure Handling

| Problem | Handling |
|---------|----------|
| No paper provided | Ask user to provide the paper text or file path |
| File cannot be read | Inform user, ask for alternative format |
| Paper has no reference list | Skip citation check, note "no reference list to verify" |
| Paper is too short (< 500 words) | Warn: "Paper appears very short — review may be limited" |
| Paper is in a language I cannot review | Tell user the limitation clearly |
| Citation check finds HIGH-RISK citations | Flag in decision: "Multiple citations appear fabricated — recommend reject or deep verification" |

### Pitfall: File corruption with special characters

When writing review reports containing Chinese text, curly quotes, DOIs with slashes, or special characters, incremental writes (multiple small write_file calls) can corrupt the output due to shell escaping issues. Content ends up garbled or with double-escaped characters.

**Fix**: Write complete file content in a single write_file call. Do NOT build the document via incremental patch/write operations. For content over ~15KB, use execute_code with a Python script that builds the content string programmatically and calls write_file once.

---

## Linked Files

- `references/review_criteria_framework.md` — Full 7-dimension rubric with paper type-specific criteria
- `references/editorial_decision_standards.md` — Decision matrix, revision round policy, reviewer ethics
- `references/citation_verification_protocol.md` — DOI resolution and title search via OpenAlex API for verifying citation existence

---

## Version History

- **1.1.0** (2026-06-09): Added citation verification via OpenAlex API (DOI resolution + title search). Clarified "redacted" data access to permit database lookup for citation existence. Added file corruption pitfall.
- **1.0.0** (2026-06-09): Initial port from Imbad0202/academic-research-skills academic-paper-reviewer v1.10.0. Modes: full, quick, guided. Anti-sycophancy concession protocol. Citation integrity gate.
