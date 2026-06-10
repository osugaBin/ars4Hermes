---
name: deep-research
description: "Academic deep research with web sources: systematic retrieval, cross-validation, integrity gates, structured reporting."
version: 1.1.0
author: Hermes Agent (adapted from Imbad0202/academic-research-skills)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [research, academic, literature-review, systematic-review, fact-check, socratic]
    related_skills: [academic-paper, academic-paper-reviewer, academic-pipeline]
---

# Deep Research

Conduct thorough academic-grade research using web sources. This skill guides you through a disciplined workflow: intent detection → retrieval → cross-validation → integrity gate → structured output.

## When to load

The user says or implies any of:

| Trigger | Mode |
|---------|------|
| `开始深度研究 [主题]` / `deep research [topic]` | **full** — 10-15 sources, complete report |
| `快速调研 [主题]` / `quick research [topic]` | **quick** — 5-6 core sources, brief |
| `系统综述 [主题]` / `systematic review [topic]` | **systematic-review** — PRISMA pipeline |
| `引导我研究 [主题]` / `guide my research [topic]` | **socratic** — guided Socratic dialogue |
| `事实核查 [主张]` / `fact-check [claim]` | **fact-check** — verify specific claims |
| `文献综述 [主题]` / `literature review [topic]` | **lit-review** — annotated bibliography + synthesis |

Also load when the user asks to "research", "investigate", "look into", "find sources on", or "what does the literature say about" anything academic or evidence-based.

## Workflow

This is a structured workflow — execute the relevant phase(s) in order. Each phase has explicit tool calls, checkpoints, and output format. Do not skip the **Integrity Gate** (Phase 4) — it is mandatory for all modes except fact-check.

---

## Phase 0: Mode Dispatch (always run first)

Parse the user's request and select the mode. Use this decision tree:

```
User says:
  "引导我研究" / "guide my research" / "帮我想想"  ──→  socratic mode
  "系统综述" / "systematic review" / "PRISMA"  ──→  systematic-review mode
  "快速调研" / "quick research" / "quick look"  ──→  quick mode
  "事实核查" / "fact-check" / "verify" / "check claim"  ──→  fact-check mode
  "文献综述" / "literature review"  ──→  lit-review mode
  Unclear / general "research" / "deep research"  ──→  full mode (ask to clarify RQ first)
```

### Mode parameters

| Mode | Min sources | Output length | Socratic? | Integrity gate? |
|------|-------------|---------------|-----------|-----------------|
| full | 10-15 | 3000-8000 words | No | Yes |
| quick | 5-6 | 500-1500 words | No | Yes |
| systematic-review | 15+ (PRISMA) | 5000+ words | No | Yes |
| socratic | 0 (dialogue) | Research Plan Summary | Yes | N/A |
| fact-check | 3-5 per claim | 300-800 words | No | N/A |
| lit-review | 8-12 | 1500-4000 words | No | Yes |

---

## Phase 1: Retrieve & Extract (all modes except socratic)

### 1a. Formulate search strategy

Generate 3-5 search queries using different angles:
- Primary keywords (the core topic)
- Synonyms / related terms
- Methodological angle (e.g., "meta-analysis", "systematic review", "survey")
- Opposite / critical angle (e.g., "criticism of", "limitations of")
- Specific authoritative sources if known (site:.edu, site:.gov)

**Preferred method**: Use `web_search(query="...", limit=10)` for each query. When it works, this is the fastest path.

**Fallback method (when web_search times out consistently)**: Some networks block the DuckDuckGo/Google/Brave backends. After 2-3 web_search failures, switch to academic API endpoints via curl in terminal. These are rate-limited but require no API key:

- **OpenAlex**: `curl -sL 'https://api.openalex.org/works?search={query}&per_page=10' | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(r["publication_year"], r["title"][:90]) for r in d["results"][:10]]'`
  - Returns title, year, DOI, citation count, venue
  - Filter by concept: `&filter=concepts.display_name:Statistics+education`
  - See `references/openalex_api_protocol.md` for full details

- **arXiv**: `curl -sL 'http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=10' | grep -o '<title>[^<]*</title>'`
  - Returns paper titles (first result is the query itself, skip it)

- **Semantic Scholar**: `curl -sL 'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&limit=10&fields=title,year,url' | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(p["title"], p.get("year","")) for p in d.get("data",[])]'`

**Academic API reliability notes**:
- OpenAlex is the most reliable (self-hosted, doesn't block Chinese IPs, no auth needed)
- Semantic Scholar and OpenAlex may time out on SSL handshake from some networks; when that happens, try the plain-HTTP arXiv endpoint or use `curl -k` (insecure)
- If all APIs time out, use browser_navigate to Bing/Baidu Scholar as last resort

For systematic-review mode, also formulate a **PICOS** question.
- **P**opulation / Problem
- **I**ntervention / Exposure
- **C**omparison / Control
- **O**utcome
- **S**tudy design

### 1b. Screen results

Filter search results by:
1. Relevance to the research question
2. Source quality (prefer: peer-reviewed journals, academic institutions, government/research orgs)
3. Recency (prefer < 5 years unless historical context needed)

**Predatory publication red flags** — exclude if:
- No identifiable editorial board
- Not indexed in Scopus / WoS / PubMed
- Excessively broad scope ("International Journal of Everything")
- APC suspiciously low
- Acceptance claimed within 72 hours

### 1c. Extract content

For each included source, use `web_extract(urls=[url])` to get the full content.
If web_extract fails (DuckDuckGo backend), use `browser_navigate(url)` + `browser_console(expression)` / `browser_vision()` to read the page.

Extract these dimensions from each source:
- Core thesis / argument
- Key data / statistics (with numbers)
- Methodology used
- Main conclusions
- Limitations explicitly stated
- Conflicts of interest / funding

Store in a structured working table (internal only, not delivered to user):

```
| # | Source | Type | Key Claims | Data | Methodology | Limitations | Quality Grade |
|---|--------|------|------------|------|-------------|-------------|---------------|
| 1 | [URL]  | [journal/report/news] | ... | ... | ... | ... | A/B/C/D |
```

### 1d. Source quality grading (per source)

Grade each source on this simplified scale:

| Grade | Meaning | Examples |
|-------|---------|----------|
| A | Primary evidence | Peer-reviewed meta-analysis, RCT, systematic review |
| B | Good supporting evidence | Cohort study, controlled study, well-documented report |
| C | Adequate with caveats | Case study, survey, editorial, policy brief |
| D | Weak / use only if necessary | Blog post, opinion piece, unverified preprint |
| F | Do not use | Predatory journal, self-published, no methodology |

---

## Phase 2: Cross-Validation (all modes — MANDATORY)

Compare all extracted sources systematically. You MUST do this step before writing any output.

### 2a. Build consensus map

Group claims by topic. For each claim, determine:

- **Consensus**: 3+ independent sources agree on the same finding
  → Mark as `[CONSENSUS]` with supporting source URLs

- **Partial agreement**: 2 sources agree, no contradicting evidence
  → Mark as `[SUPPORTED]` with sources

- **Contradiction**: Sources make conflicting claims
  → Mark as `[CONTRADICTION]` with both sides' sources

- **Isolated claim**: Only one source makes this claim
  → Mark as `[ISOLATED]` and note "needs verification"

### 2b. Evidence hierarchy check

For each claim, check if the best available evidence level supports it:
- A Level I-II claim can be overturned by a Level I-II counter-study → present as contradiction
- A Level III claim supported only by Level VI-VII sources → downgrade to `[WEAK EVIDENCE]`
- A claim from an A-grade source should be weighted heavier than from a D-grade source — flag discrepancies

### 2c. Citation verification (mandatory for systematic-review mode)

Every citation in the final output must:
1. Have a resolvable URL (not just a DOI without a link)
2. Be verifiable by web_extract or browser_navigate
3. Have the claim actually present in the extracted content (no hallucinated citations)

If any citation cannot be verified, flag it in the report: `[UNVERIFIED CITATION — removed from final report]`

### 2d. Reference Integrity Verification Protocol (ALL modes — NEW)

After compiling the research report, verify every reference for basic existence. This prevents hallucinated or fabricated citations from entering the downstream writing pipeline.

**Method: OpenAlex DOI verification**

For each reference with a DOI:
```bash
curl -sL 'https://api.openalex.org/works/doi:{doi}' | python3 -c '
import json,sys; d=json.load(sys.stdin);
print(d["publication_year"], "|", d["title"][:80], "|", d["cited_by_count"])
'
```

- If the DOI resolves and the year/title match → **VERIFIED**
- If the DOI does not resolve → try searching by title via OpenAlex:
  `curl -sL 'https://api.openalex.org/works?search={title_keywords}&per_page=3'`
- If title search also fails → mark as `[需人工确认]`

**Hard rules (do NOT violate):**

1. **NEVER fabricate a reference.** Inventing author names, volume/issue/page numbers, DOIs, or paper titles is a violation of academic integrity. It is worse than acknowledging a gap.

2. **When a real source cannot be found:**
   - Mark `[MATERIAL GAP: description of specific source needed]`
   - Tell the user what is missing
   - Do NOT fill the gap from parametric memory

3. **Resolve DOIs, don't guess them.** If you don't have a verified DOI, search for it via OpenAlex. Do NOT construct a plausible-looking DOI.

4. **Placeholder/alias names are fabrication.** "张三", "李四", "John Doe", "et al." with no real first author — these are fabrication indicators.

5. **Each reference in the final report must carry a verification status:**
   - ✅ VERIFIED — confirmed via API
   - ⚠️ NEEDS CONFIRMATION — title search succeeded but DOI uncertain
   - ❌ MATERIAL GAP — no source found, truthfully flagged

**Reference verification is NOT optional.** A research report with unverified references cannot proceed to the writing pipeline.

See `scripts/verify_references.py` for an automated verification workflow.

---

## Phase 3: Socratic Mode (only for socratic mode)

### 3a. Intent detection

In the first response, classify the user's intent:

- **Exploratory conversation**: User is still forming the question, trying to find a research direction. Key signals: vague topic, "I'm interested in...", "not sure what...", changing direction.
  → Stay in exploration mode. Disable auto-convergence. Never suggest "shall I write a summary?"

- **Goal-oriented**: User has a specific question or direction. Key signals: specific question, named theory/concept, comparative framing.
  → Standard convergence behavior. Can transition to full mode when the RQ is clear.

### 3b. Socratic dialogue structure

Use the **5-layer progression**, moving deeper only after at least 2 rounds per layer:

**Layer 1: Problem Framing**
Ask questions like:
- "What is the question you truly want to answer?"
- "Why does this question matter? To whom?"
- "If your research succeeds, how would the world be different?"
Extract `[INSIGHT: ...]` from each user response.

**Layer 2: Methodology Reflection**
- "How do you plan to answer this question? Why this approach?"
- "Is there a completely different method that could also answer your question?"
- "What is the biggest weakness of your method?"

**Layer 3: Evidence Design**
- "What kind of evidence would convince you of your conclusion?"
- "What evidence would make you change your conclusion?"
- "What are you most worried about not finding?"

**Layer 4: Critical Self-Examination**
- "What does your research assume? What if those assumptions don't hold?"
- "How would someone with the opposite view refute you?"
- "What negative impact could your research have?"

**Layer 5: Significance & Contribution**
- "Why should readers care about your findings?"
- "What aspects of understanding does your research change?"
At least 1 round.

### 3c. Dialogue rules

- Mentor responses: 200-400 words
- At least 2 rounds per layer before advancing
- User can request to skip to the next layer at any time
- **No convergence after 10 rounds** → suggest switching to `full` mode
- **Exceeds 15 rounds** → auto-compile INSIGHTs and end
- If user requests direct answers → gently decline: "I'm here to help you think through it — the question you arrive at yourself will be stronger"

### 3d. Termination

When dialogue converges or max rounds reached, compile a **Research Plan Summary**:

```markdown
# Research Plan Summary

## Research Question
> [Final refined RQ]

## Key INSIGHTs from Dialogue
- [INSIGHT 1]
- [INSIGHT 2]
- ...

## Suggested Next Steps
1. [Recommended mode: full / lit-review / academic-paper]
2. [Brief rationale]
```

---

## Phase 4: Integrity Gate (MANDATORY for full / quick / lit-review / systematic-review)

Before writing the final report, check for **5 AI research failure modes**:

### F1: Fabricated citations
- For every key claim, verify the source supports it. Re-extract if uncertain.
- If a source URL returns nothing relevant → `[完整性警告：引用来源不支撑该论断 — 已移除]`

### F2: Fabricated methodology
- Did you describe a methodology (meta-analysis, systematic search, statistical test) that you did NOT actually perform?
- If yes → `[完整性警告：方法捏造 — 该方法未实际执行]`

### F3: Shortcut reliance
- Did you substitute general knowledge for specific sourced evidence?
- Every substantive claim needs a source URL. If you find one without a URL → `[完整性警告：缺乏来源支持]`

### F4: Frame lock
- Did you only present one side of the argument?
- If the literature contains opposing views and you didn't present them → `[完整性警告：框架锁定 — 需要补充对立观点]`

### F5: Hallucinated data
- Every number, statistic, or percentage must trace to a source. If you can't → `[完整性警告：数据来源不明]`

**If ANY failure is detected**, open the report with:

> **⚠️ [完整性警告：{failure_type}]**
> {Description of what was found and how it was handled}

### Citation existence gate (systematic-review mode only)

For systematic-review mode, run an additional deterministic check:
- Every citation key must resolve to a live URL or DOI
- Use `web_extract(url)` or `browser_navigate(url)` to confirm at least the first page loads
- Mark unresolved citations: `[UNVERIFIED CITATION — URL does not resolve]`
- DO NOT include unresolvable citations in the final report

---

## Phase 5: Compose Report

### Full mode report structure

```markdown
# Research Report: [Topic]

**Date**: [YYYY-MM-DD]
**Mode**: Full Deep Research
**Sources consulted**: [N]
**Sources cited**: [M]
**AI Disclosure**: This report was produced with AI-assisted research using web-based retrieval and cross-validation. All claims are sourced to verifiable URLs.

---

## Executive Summary
[~200 words. Question, key findings, main conclusion.]

---

## [Section 1: Background & Research Question]

### Context
[...]

### Research Question
> [Single clear sentence]

---

## [Section 2: Consensus Findings]

### Finding 2.1: [Title]
[Detailed analysis with inline citations as `[Source N]`]
**Evidence strength**: [Strong / Moderate / Emerging]
**Sources**: [URL1], [URL2]

### Finding 2.2: [Title]
[...]

---

## [Section 3: Contradictions & Debates]

### Issue 3.1: [Topic of disagreement]

**Position A**: [Claim + source URL]
**Position B**: [Counter-claim + source URL]
**Assessment**: [Which side has stronger evidence and why]

---

## [Section 4: Research Gaps]

- [Gap 1]
- [Gap 2]
- [Gap 3]

---

## [Section 5: Conclusion & Implications]
[...]

---

## References

1. [Author(s)], "[Title]", [Publication], [Year]. URL: [Full URL]
2. [Author(s)], ...
```

### Quick mode report structure

Use `templates/research_brief_template.md` from linked files:

```markdown
# Research Brief: [Topic]

**Date**: [YYYY-MM-DD]
**Sources**: [N]

## Executive Summary
[100-150 words]

## Key Findings
- Finding 1 with source [URL] — evidence strength
- Finding 2 with source [URL] — evidence strength
- Finding 3 with source [URL] — evidence strength

## Key Sources
1. [URL] — [brief annotation]
2. [URL] — [brief annotation]
```

### Fact-check mode report structure

```markdown
# Fact-Check Report

**Claim**: [Exact claim]
**Date**: [YYYY-MM-DD]

## Verdict: [TRUE / MOSTLY TRUE / MIXED / MOSTLY FALSE / FALSE / UNVERIFIABLE]

## Evidence
- Supporting: [source URL] — [key excerpt]
- Contradicting: [source URL] — [key excerpt]

## Source Quality Assessment
[Brief grade of best available evidence]

## Confidence Level: [High / Medium / Low]
[Justification]
```

### Systematic-review mode report structure

```markdown
# Systematic Review: [Topic]

**Date**: [YYYY-MM-DD]
**Protocol**: PRISMA 2020-compliant
**Registration**: Not registered (recommend PROSPERO for journal submission)

## Background & PICOS Question
- **P**: ...
- **I**: ...
- **C**: ...
- **O**: ...
- **S**: ...

## Methods
### Search Strategy
- Query: [exact query string]
- Databases: web_search (multi-angle)
- Date range: [X-Y]
- Inclusion: [criteria]
- Exclusion: [criteria]

## Results
### PRISMA Flow
- Records identified: [N]
- Screened: [N]
- Full text assessed: [N]
- Included: [N]
- Excluded with reasons: [list]

### Study Characteristics
| Study | Design | Population | Intervention | Outcome | Quality |
|-------|--------|------------|--------------|---------|--------|
| ... | ... | ... | ... | ... | ... |

### Risk of Bias (simplified)
| Study | Selection | Performance | Detection | Attrition | Overall |
|-------|-----------|-------------|-----------|-----------|---------|
| ... | Low/High/Unclear | ... | ... | ... | ... |

### Synthesis
[Qualitative or quantitative synthesis]

## Discussion

## Limitations

## Conclusion

## References
```

### Lit-review mode report structure

```markdown
# Literature Review: [Topic]

**Date**: [YYYY-MM-DD]
**Sources**: [N]

## Thematic Synthesis
### Theme 1: [Title]
- [Source A] argues...
- [Source B] finds...
- Synthesis: [What the collective evidence says]

### Theme 2: [Title]
[...]

## Evidence Matrix
| Source | Theme 1 | Theme 2 | Theme 3 | Quality |
|--------|---------|---------|---------|--------|
| [URL]  | ✓ |   | ✓ | A |
| [URL]  |   | ✓ |   | B |

## Research Gaps Identified
1. ...
2. ...

## References
```

---

## Phase 6: Handling Failures (when things go wrong)

### F1 — Insufficient sources (< min for mode)
1. Expand search: add synonyms, broader terms, adjacent fields
2. Relax date range (5 → 10 years)
3. If still insufficient → tell the user: "Only [N] relevant sources found. This may be a new/niche area. Options: (a) accept as exploratory, (b) broaden the question, (c) include grey literature."

### F2 — User abandons mid-process
- Compile partial findings into a Progress Summary
- Don't push; offer to save and resume later

### F3 — All sources below quality threshold (all C/D)
- Report to user: "Available sources are mostly [reasons]. Will use with explicit caveats."
- Every finding must carry a `[Caveat: source quality is limited]` marker

---

## Hermes Tool Integration

### web_search
- Use for all search phases
- limit=10 by default; increase to 20 for systematic-review
- Use diverse queries (different angles, not just rephrasing the same one)
- **Pitfall**: DuckDuckGo backend (the default) is unreliable from some networks — consistently times out on academic queries. When this happens, DO NOT retry web_search more than 2-3 times. Switch immediately to the academic API fallbacks (OpenAlex, arXiv, Semantic Scholar) documented in Phase 1a.

### web_extract
- Use for reading full source content
- Falls back to browser tools if DuckDuckGo backend blocks extraction

### browser_navigate / browser_snapshot / browser_vision
- Fallback for pages that web_extract can't access
- Also use for citation verification (check that URL actually loads)

### delegate_task
- For systematic-review mode with 15+ sources: delegate parallel extraction
  ```
  delegate_task(tasks=[
      {"goal": "Extract key claims from sources 1-5", "toolsets": ["web", "terminal"]},
      {"goal": "Extract key claims from sources 6-10", "toolsets": ["web", "terminal"]},
      {"goal": "Extract key claims from sources 11-15", "toolsets": ["web", "terminal"]},
  ])
  ```
- For lit-review mode with diverse subtopics: delegate per-theme extraction

### write_file
- Save the final report to a file at the user's specified path, or suggest one
- Naming: `deep-research_<topic>_<mode>_<YYYY-MM-DD>.md`

---

## Linked Files

- `references/source_quality_hierarchy.md` — Full evidence grading framework (7 levels, field-specific adjustments, predatory publication indicators)
- `references/systematic_review_protocol.md` — PRISMA 5-phase pipeline with checkpoint rules
- `references/socratic_mode_protocol.md` — 5-layer Socratic dialogue protocol
- `templates/research_brief_template.md` — Quick mode output template
- `references/failure_paths.md` — Complete failure path map (F1-F11)
- `references/openalex_api_protocol.md` — OpenAlex academic API: queries, parsing, rate limits, fallback strategy when web_search fails
- `scripts/verify_references.py` — Batch DOI verification via OpenAlex: resolves each DOI and returns verification status. Run via `python3 ~/.hermes/skills/research/deep-research/scripts/verify_references.py --dois "doi1,doi2,..."`

## Version History

- **1.1.0** (2026-06-09): Added academic API fallback strategy (OpenAlex, arXiv, Semantic Scholar) for when web_search (DuckDuckGo backend) is unreachable. Added openalex_api_protocol.md reference.
- **1.0.0** (2026-06-09): Initial port from Imbad0202/academic-research-skills deep-research v2.9.4. Adapted for Hermes Agent toolset (web_search, web_extract, browser, delegate_task). Modes: full, quick, systematic-review, socratic, fact-check, lit-review.
