---
name: academic-paper
description: "Academic paper writing assistant: outline to draft to revise to format. Uses provided research materials, does not fabricate claims."
version: 1.1.0
author: Hermes Agent (adapted from Imbad0202/academic-research-skills)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [paper-writing, academic-writing, publication, thesis]
    related_skills: [deep-research, academic-paper-reviewer, academic-pipeline]
---

# Academic Paper

Write, revise, and format academic papers using provided research materials. This skill follows a disciplined writing pipeline: paper type confirmation, literature check, structured drafting, citation compliance, integrity disclosure.

**Data access: verified_only** -- writing phase does NOT actively search the web. Only use sources provided by the user or passed from deep-research.

## When to load

| Trigger | Mode |
|---------|------|
| write paper / write academic paper [topic] | full -- complete paper from outline to final |
| write review / write survey [topic] | full (literature review pattern) |
| revise paper | revision -- revise based on reviewer comments |
| outline / generate outline [topic] | outline-only -- produce structure only |
| write abstract / write abstract [topic] | abstract-only -- produce bilingual abstract |

Also load when user says: draft a paper, write a manuscript, help me write, I need to write a paper.

---

## Phase 0: Mode Dispatch and Paper Type Confirmation

### Mode selection

Parse user intent. If user says outline/structure -> outline-only. If abstract -> abstract-only. If revise/modify + provides draft+review -> revision. Otherwise: full mode.

### Paper type confirmation (full and outline-only)

Ask user to choose:
1. Empirical (IMRaD) -- original data collection and analysis
2. Literature Review -- thematic synthesis of existing research
3. Theoretical Analysis -- develop/critique/extend a framework
4. Case Study -- in-depth analysis of a specific case
5. Policy Brief -- evidence-based policy recommendations

Also confirm: target journal/conference (determines citation format and word limit), word count target (default 5000-8000 for full paper, 2000-3000 for conference), language.

---

## Phase 1: Literature Base Check

### Check available materials

Has user provided: deep-research report, annotated bibliography, user-provided sources, raw data?

### If no materials: STOP

Do NOT start writing without sources. Ask user to run deep-research first or provide sources.

### Anti-Leakage Protocol

When writing:
- Every factual claim MUST trace to a provided source
- If a required section has no source material -> flag MATERIAL GAP -- do NOT fill from memory
- The Methods section must describe ONLY what is documented in the user's materials
- Do NOT introduce references not in the provided bibliography

---

## Phase 2: Drafting

### Outline stage

Generate section-by-section outline based on paper type template. Present to user for confirmation before drafting.

### Title suggestions

Suggest 3-5 title options with different styles: descriptive, declarative, question, metaphorical. Let the user pick.

### Draft section by section (full mode)

Write each section sequentially. For each section: state the purpose, write from sources with Author Year citations, check citation anchors, flag MATERIAL GAPs where sources insufficient, proceed with user's confirmation between sections.

### Revision mode

Parse reviewer comments into actionable tasks. Map each to its section. Create revision tracking table. Apply revisions one by one. Produce clean + annotated versions.

---

## Phase 3: Citation Compliance

### In-text format (default APA 7th)

Format: [Author, Year] for narrative, (Author, Year) for parenthetical.

Chinese citation rules: Chinese authors use full surname, multiple separated by, English-Chinese mixed: English first.

### Location anchors

Every citation needs a location anchor: quote (direct quotation), page (specific page), section (section-level), none (general concept -- flag NO LOCATOR).

### Reference list

APA 7th: Author, A. A. (Year). Title. Journal, Volume(Issue), Pages. DOI

Supported formats: APA 7th (default), Chicago, MLA, IEEE, Vancouver.

### Citation verification

For each in-text citation: is the source in the reference list? Does the claim match what the source actually says? Does it have a location anchor? If any citation cannot be verified: `[UNVERIFIED CITATION — removed]` and do NOT include in final.

### CRITICAL — No fabricated references

NEVER fabricate references (author names, volume/issue/page, paper titles). When a source is needed but unavailable:
1. Mark `[MATERIAL GAP: description of what is missing]`
2. Tell the user what specific source is needed
3. Do NOT fill the gap from memory

Fabricated citations violate academic integrity and are worse than acknowledged gaps.

### Reference verification workflow

When the draft is complete, before delivery, run a verification pass on every reference:

1. Extract each DOI and verify via OpenAlex:
   ```bash
   curl -sL 'https://api.openalex.org/works/doi:{doi}' | python3 -c '
   import json,sys; d=json.load(sys.stdin);
   print(d.get("publication_year",""), d.get("title","")[:60])
   '
   ```
2. If DOI fails, search by title:
   ```bash
   curl -sL 'https://api.openalex.org/works?search={title_keywords}&per_page=3'
   ```
3. Mark each result: ✅ verified / ⚠️ needs confirmation / ❌ material gap
4. References that cannot be verified: flag `[UNVERIFIED CITATION — removed]` and exclude from the final draft

**Pitfall — Chinese references:** OpenAlex has limited coverage of Chinese-language journals. A failure to find a Chinese reference on OpenAlex does NOT prove it's fabricated — but placeholder author names (Example: 张三) DO prove fabrication. Always distinguish "unindexed but plausible" from "invented."

---

## Phase 4: Bilingual Abstract

### English abstract

Standard structure: Background (1-2 sentences), Purpose (1 sentence), Method (1-2 sentences), Findings (2-3 sentences), Implications (1-2 sentences). 150-250 words. 5-7 keywords.

### Chinese abstract

Same structure in Chinese. 200-300 characters. 3-5 keywords.

---

## Phase 5: Integrity and Disclosure

### Writing quality self-check

Before finalizing: structure completeness, citation coverage, anchor coverage, no fabricated content, no unfilled MATERIAL GAPs, bilingual abstract present, word count within target, consistent citation format.

### AI disclosure statement

Append to every paper:

AI use statement: This paper used Hermes Agent + [current model] for literature retrieval, citation formatting, grammar checking. All core arguments, data interpretation, and final conclusions are the responsibility of the author(s).

---

## Phase 6: Output

### Full paper structure

Title, Author(s), Date, Paper type, Target venue, Abstract (English + Chinese), Sections (1..N), AI Disclosure, References.

### Outline-only structure

Working title, Paper type, Target word count, Section list with estimated word counts per section, Preliminary reference list.

### Abstract-only structure

Working title, English Abstract, Keywords, Chinese Abstract, Keywords, Key References for Abstract.

### Revision output

Two files: paper_final.md (clean) + paper_revision_track.md (annotated with REVISED markers).

---

## Phase 7: Failure Handling

| Problem | Handling |
|---------|----------|
| No research materials | Stop. Ask user to run deep-research first. |
| Material gap in section | Flag MATERIAL GAP. Ask user to fill or authorize supplementation. |
| Citation cannot be verified | Remove. Note UNVERIFIED CITATION removed in draft. |
| User wants unsupported claim | Flag as AUTHOR CLAIM no source. |
| Word count over/under | Adjust section depth. |

### Pitfall: File corruption with special characters

When writing academic documents containing Chinese text, curly quotes, DOIs with slashes, or special characters, incremental writes (multiple small write_file calls) can corrupt the output due to shell escaping issues. Content ends up garbled or with double-escaped characters.

**Fix**: Write complete file content in a single write_file call. Do NOT build the document via incremental patch/write operations. For content over ~15KB, use execute_code with a Python script that builds the content string programmatically and calls write_file once.

---

## Linked Files

- references/paper_structure_patterns.md -- 6 paper structure templates
- references/anti_leakage_protocol.md -- Knowledge isolation rules
- references/apa7_chinese_citation_guide.md -- APA 7th Chinese rules
- templates/bilingual_abstract_template.md -- Bilingual abstract template
- templates/revision_tracking_template.md -- Revision tracking table

---

## Version History

- **1.2.0** (2026-06-09): Expanded reference integrity section. Added reference verification workflow (OpenAlex DOI resolution, title-fallback, status marking). Added Chinese-reference pitfall (distinguish unindexed from invented). Embedded the no-fabricated-references rule with specific examples of what constitutes fabrication.
- **1.1.0** (2026-06-09): Added pitfall: file corruption with special characters during incremental writes.
- **1.0.0** (2026-06-09): Initial port.