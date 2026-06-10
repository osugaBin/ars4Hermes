---
name: academic-pipeline
description: "Full academic research-to-publication pipeline: research → integrity check → writing → citation audit → peer review → final output, with mandatory gates at Stage 2.5 and 4.5."
version: 1.0.0
author: Hermes Agent (adapted from Imbad0202/academic-research-skills)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [pipeline, orchestration, academic, research-to-paper, workflow]
    related_skills: [deep-research, academic-paper, academic-paper-reviewer]
---

# Academic Pipeline

Orchestrates the full academic research-to-publication workflow: deep research → integrity gate → paper writing → citation audit → peer review → final output. Loads and coordinates the other three ARS4Hermes skills (`deep-research`, `academic-paper`, `academic-paper-reviewer`).

**Every stage boundary requires user confirmation before proceeding.**

## When to load

| Trigger | Behaviour |
|---------|-----------|
| `启动学术全流程 [选题]` | Full pipeline from research to final paper |
| `从零开始写论文 [选题]` | Same as above — assumes no prior materials |

Also load when user says: "full pipeline", "从研究到发表", "write a paper from scratch".

## Pipeline Overview

```
Stage 1: DEEP RESEARCH  ──→  [User Confirm]
    │
    ▼
Stage 2.5: INTEGRITY GATE (MANDATORY)  ──→  [PASS / FAIL → fix → re-check]
    │                                       max 3 retries
    ▼
Stage 3: PAPER WRITING  ──→  [User Confirm]
    │
    ▼
Stage 4.5: CITATION AUDIT (MANDATORY)  ──→  [PASS / FAIL → fix → re-check]
    │                                         max 3 retries
    ▼
Stage 5: PEER REVIEW  ──→  [Decision: Accept / Minor / Major / Reject]
    │
    ├── Accept ──→ Stage 6: FINAL OUTPUT
    ├── Minor ──→ User revises → Stage 6
    └── Major ──→ User revises → re-review (max 1 re-revise round) → Stage 6
    │
    ▼
Stage 6: FINAL OUTPUT + PROCESS SUMMARY
```

## Data Flow

| Stage | Produces | Consumes |
|-------|----------|----------|
| 1 | `stage1_research.md` (deep-research report) | User's topic |
| 2.5 | `stage25_integrity.md` | `stage1_research.md` |
| 3 | `stage3_draft.md` (paper draft) | `stage1_research.md` (after gate pass) |
| 4.5 | `stage45_citation_audit.md` | `stage3_draft.md` |
| 5 | `stage5_review.md` (review report) | `stage3_draft.md` (after audit pass) |
| 6 | `final_paper.md` + `process_summary.md` | All previous outputs |

Files are saved to the user's designated output directory under `~/Desktop/Hermes/ars4Hermes/eg<N>/`. Ask for a project label at pipeline start — each run gets its own `eg<N>` directory (eg1, eg2, ...). File naming convention is fixed:

```
eg<N>/
├── stage1_research.md
├── stage25_integrity.md
├── stage3_draft.md
├── stage45_citation_audit.md
├── stage5_review.md
├── final_paper.md
└── process_summary.md
```

**Pitfall — network-dependent Stage 1**: `web_search` may time out on some networks. When that happens, fall back to academic API endpoints (OpenAlex, arXiv) via `curl`. Stage 1 will produce API-returned metadata rather than full web-extracted content. Stage 2.5 (integrity gate) must adapt accordingly: verify citations against what the APIs returned.

**Checkpoint convention**: After each stage, present a summary and ask the user to type 继续 (continue) to proceed. The user may also say 修改 to go back and adjust.

---

## Stage 1: Deep Research

### 1a. Confirm topic and mode

Ask the user:
> 研究主题是：「[用户说的选题]」，对吗？
> 希望用什么模式？
> - **完整模式**（10-15 个来源，完整报告）
> - **系统综述模式**（PRISMA 流程，适合发表）

Let the user confirm or refine the topic before proceeding.

### 1b. Execute deep-research

Load the `deep-research` skill and run full or systematic-review mode. This means I (the agent) follow the deep-research workflow:

1. Formulate 3-5 search queries at different angles
2. Execute `web_search` for each query
3. Screen results by relevance, quality, recency
4. Extract content with `web_extract` (fallback to browser tools)
5. Build consensus map (Phase 2 cross-validation)
6. Run integrity gate (Phase 4 — check 5 AI failure modes)
7. Compose full research report

### 1c. Save and checkpoint

Save the research report to a file:

```
<workdir>/academic-pipeline/
  └── stage1_research.md
```

Present brief summary to user:
> ✅ 深度研究完成。
> - 来源数量：N
> - 共识发现：M 个
> - 矛盾点：K 个
> - 完整性检查：[PASS / WARN — see report]
>
> 已保存至：<path>
> 输入「继续」进入完整性门控检查，或输入「修改」调整研究方向。

Wait for user confirmation (`继续` / `continue` / `确认`) before proceeding to Stage 2.5.

---

## Stage 2.5: Integrity Gate (MANDATORY — cannot skip)

### 2a. Run integrity checks on the research report

Even though deep-research already ran its own integrity check, Stage 2.5 is an independent re-verification from a pipeline perspective. Check:

**F1 — Fabricated citations**:
- Spot-check 5 citations from the research report
- For each: does the extracted content from the source URL actually support the claim?
- If any citation claim does not match the extracted content → `[HIGH-WARN: Fabricated citation — claim not found in source]`

**F2 — Methodology fabrication**:
- Does the report claim a methodology (meta-analysis, systematic review, statistical test) that was NOT actually performed?
- If yes → `[HIGH-WARN: Methodology fabrication — method not executed]`

**F3 — Frame lock**:
- Does the report present only one side of a contested topic?
- If contradictory evidence exists in the extracted sources but the report only shows one view → `[HIGH-WARN: Frame lock — opposing views omitted]`

**F4 — Hallucinated data**:
- Every number/statistic/percentage in the report should trace to a source
- If any has no source → `[WARN: Data without source]`

### 2b. Decision

| Result | Action |
|--------|--------|
| All CLEAR | Save integrity report as `stage25_integrity.md`. Proceed to Stage 3. |
| WARN-only (no HIGH-WARN) | Log in report. Proceed to Stage 3 with advisory notes. |
| Any HIGH-WARN | **STOP**. Show user the issue(s). Options: (a) fix and re-check, (b) user override with recorded reasoning. Max 3 re-check rounds. If still failing after 3 → user must override or abort. |

### 2c. Save and checkpoint

```
<workdir>/academic-pipeline/
  └── stage25_integrity.md
```

Present to user:
> 🔍 完整性门控检查完成。
> - 引用核查：[PASS / WARN / HIGH-WARN]
> - 方法学核查：[PASS / WARN]
> - 框架锁定核查：[PASS / WARN]
> - 数据溯源核查：[PASS / WARN]
>
> 输入「继续」进入论文写作阶段。

---

## Stage 3: Paper Writing

### 3a. Load academic-paper skill

I follow the `academic-paper` workflow, using the research report as the primary source material:

1. **Paper type confirmation** — Ask user: empirical / lit review / theoretical / case study / policy brief
2. **Target venue** — Ask user: journal / conference name, citation format, word count
3. **Outline** — Generate section outline based on paper type
4. **Title suggestions** — Offer 3-5 title options
5. **Draft section by section** — Write each section using Anti-Leakage Protocol (all claims from `stage1_research.md`)
6. **Bilingual abstract** — English 150-250 words + Chinese 200-300 chars
7. **Citation format** — APA 7th default, each citation has location anchor
8. **AI disclosure** — Append disclosure statement

### 3b. Save and checkpoint

```
<workdir>/academic-pipeline/
  ├── stage3_outline.md  (if user wants to review outline first)
  └── stage3_draft.md    (full draft)
```

Present to user:
> 📝 论文初稿完成。
> - 字数：N
> - 章节数：M
> - 引用数：K
> - 格式：[APA 7th / etc.]
>
> 已保存至：<path>
> 输入「继续」进入引用核查阶段，或输入「修改」调整论文内容。

---

## Stage 4.5: Citation Audit Gate (MANDATORY — cannot skip)

### 4a. Reference existence verification (NEW — catch fabrication before audit)

Before checking whether draft claims match the research report, run a **basic existence check** on every cited reference:

1. Extract all DOIs from the draft's reference list
2. For each DOI, resolve via OpenAlex:
   ```bash
   curl -sL 'https://api.openalex.org/works/doi:{doi}' | python3 -c '
   import json,sys; d=json.load(sys.stdin);
   print(d.get("publication_year",""), d.get("title","")[:60])
   '
   ```
3. If a DOI does not resolve: try searching by paper title via OpenAlex
4. If title search also fails: **this reference is likely fabricated**

**Fabrication indicators (any one → HIGH-WARN):**
- DOI returns 404/empty from OpenAlex AND title search finds no match
- Author names are obvious placeholders (Example: 张三, 李四, 王五, John Doe)
- Volume/issue/page numbers look invented (Example: 42(3), 45-52 for a paper that doesn't exist)
- Journal name + topic combination doesn't exist in OpenAlex source index

**Action on HIGH-WARN:**
- Flag as `[HIGH-WARN: Likely fabricated reference — removed]`
- Do NOT pass to Stage 5 for review
- Report to user: "Reference [N] appears fabricated. It has been removed. If the source is real, provide the correct DOI."

### 4b. Spot-check 5 citations from the draft

Select 5 citations from different sections of the draft. For each:

| Check | Method |
|-------|--------|
| Source exists in provided materials? | Check against the research report's reference list |
| Claim matches source? | Re-read the relevant section from the research report |
| Has location anchor? | Check for page/quote/section reference in the citation |
| No suspicious patterns? | Overly convenient citation? Looks LLM-generated? |

### 4c. Flag suspicious citations

| Pattern | Flag |
|---------|------|
| Citation claim not found in source materials | `[HIGH-WARN: Claim not supported by provided source]` |
| Citation has no location anchor | `[WARN: No location anchor]` |
| Citation looks plausible but isn't in any source | `[HIGH-WARN: Likely hallucinated citation]` |
| Citation from provided source but overclaims | `[WARN: Claim overstates what source says]` |

### 4c. Decision

| Result | Action |
|--------|--------|
| All CLEAR | Save audit report. Proceed to Stage 5. |
| WARN-only | Proceed with advisory notes. |
| Any HIGH-WARN | **STOP**. Show user the suspicious citations. Options: (a) fix and re-check, (b) user override. Max 3 re-check rounds. |

### 4d. Save and checkpoint

```
<workdir>/academic-pipeline/
  └── stage45_citation_audit.md
```

Present to user:
> 🔍 引用审计完成。
> - 抽查引用：5 个
> - 通过：N
> - 警告：M
> - 高风险：K
>
> 输入「继续」进入同行评审阶段。

---

## Stage 5: Peer Review

### 5a. Load academic-paper-reviewer skill

I follow the `academic-paper-reviewer` workflow in full mode:

1. Read the draft
2. Score across 7 dimensions with weighted total
3. Classify all issues into 🔴 must-fix / 🟡 should-fix / 🟢 nice-to-fix
4. Run citation integrity check (already done in Stage 4.5, but the reviewer does its own independent check)
5. Produce review report with recommended decision

### 5b. Decision handling

| Decision | Action |
|----------|--------|
| **Accept** | Proceed directly to Stage 6 |
| **Minor Revision** | User revises the paper → proceed to Stage 6 |
| **Major Revision** | User revises → I run a **re-review** (follow reviewer skill again on the revised draft). Max 1 re-revise round. If re-review also returns Major → force to Stage 6 with acknowledged limitations. |
| **Reject** | Discuss with user: restart from Stage 3 with new approach, or abort the pipeline. |

### 5c. Save and checkpoint

```
<workdir>/academic-pipeline/
  ├── stage5_review.md       (review report)
  ├── stage5_re_review.md    (re-review report, if applicable)
  └── stage5_revised.md      (user's revised draft)
```

Present to user:
> 🧐 同行评审完成。
> - 总分：X.X / 5.0
> - 决定：[Accept / Minor Revision / Major Revision / Reject]
> - 必须修改问题：N 个
> - 建议修改问题：M 个
>
> 已保存至：<path>
> 请根据评审意见修改论文，修改完成后输入「继续」进入最终输出阶段。

---

## Stage 6: Final Output & Process Summary

### 6a. Produce final paper

Apply all user revisions and produce a clean final version:

```
<workdir>/academic-pipeline/
  └── final_paper.md
```

### 6b. Produce process summary report

Compile a summary of the entire pipeline:

```markdown
# ARS4Hermes Pipeline Summary

**Paper**: [Title]
**Date**: [YYYY-MM-DD]
**Pipeline ID**: ars4h-[timestamp]

---

## Stage Timeline

| Stage | Status | Key Outputs |
|-------|--------|-------------|
| Stage 1: Deep Research | ✅ / ⏳ / ❌ | stage1_research.md (N sources) |
| Stage 2.5: Integrity Gate | ✅ / ⏳ / ❌ | stage25_integrity.md |
| Stage 3: Paper Writing | ✅ / ⏳ / ❌ | stage3_draft.md (N words) |
| Stage 4.5: Citation Audit | ✅ / ⏳ / ❌ | stage45_citation_audit.md |
| Stage 5: Peer Review | ✅ / ⏳ / ❌ | stage5_review.md (score X.X) |
| Stage 6: Final Output | ✅ | final_paper.md |

---

## Integrity Issues Found & Resolved

| Stage | Issue | Severity | Resolution |
|-------|-------|----------|------------|
| 2.5 | [description] | HIGH-WARN | [fixed / user override] |
| 4.5 | [description] | WARN | [fixed] |
| ... | ... | ... | ... |

---

## Citation Audit Results

- Citations checked: 5
- Passed: N
- Warnings: M
- High-risk: K

---

## Peer Review Summary

- Weighted score: X.X / 5.0
- Decision: [Accept / Minor / Major / Reject]
- Re-review rounds: N

---

## Collaboration Quality Assessment

| Dimension | Score (1-100) | Notes |
|-----------|---------------|-------|
| Direction Setting | XX | Clarity of research direction |
| Quality Gatekeeping | XX | User's role in integrity checks |
| Iteration Discipline | XX | Willingness to revise |
| Delegation Efficiency | XX | Checkpoint decision speed |
| **Overall** | **XX/100** | |

---

## All Deliverables

| File | Path |
|------|------|
| Research Report | <path>/stage1_research.md |
| Integrity Report (S2.5) | <path>/stage25_integrity.md |
| Paper Draft | <path>/stage3_draft.md |
| Citation Audit (S4.5) | <path>/stage45_citation_audit.md |
| Review Report | <path>/stage5_review.md |
| Final Paper | <path>/final_paper.md |
| This Summary | <path>/process_summary.md |
```

### 6c. Save final outputs

```
<workdir>/academic-pipeline/
  ├── final_paper.md
  └── process_summary.md
```

### 6d. Generate Researcher Action Items

Scan the final paper for all `[需研究者...]` / `[MATERIAL GAP]` / `[需人工确认]` markers and compile a standalone action-items checklist:

```markdown
# Researcher Action Items — 待你完成的实证工作

## 数据验证类

| # | 位置 | 标记 | 具体任务 | 预估耗时 |
|---|------|------|----------|----------|
| 1 | §3.2 | [需研究者补充数据] | 查教学大纲/CNKI/问卷调研统计学课程评估现状 | 1-2 周 |
| 2 | §4.1 | [需研究者补充] | 下载核实教育部政策原文号 | 1-2 天 |
| 3 | §4.2 | [需研究者补充数据] | 调研本校评估工具/CNKI案例收集 | 1-2 周 |
| 4 | §4.3 | [需研究者补充数据] | 设计问卷收集中国高校评估方式定量数据 | 2-3 周 |
| 5 | §5.2 | [需研究者分析] | 设计教学实验，收集学生反馈 | 2-4 周 |
| 6 | §5.3 | [需研究者补充] | 查校政策/CNKI/收集态度数据 | 1-2 周 |
| 7 | §6.2 | [需研究者实证] | 选试点实施三层框架+写案例研究 | 4-8 周 |
| 8 | §7 | [需研究者行动] | 将研究空白转化为课题/论文方向 | 持续 |

## 引用核实类

| # | 引用 | 当前状态 | 需你做的事 |
|---|------|----------|-----------|
| [3] | GAISE 2016 | 未通过API索引 | 从ASA官网下载核实 |
| [6] | Chiu 2023 | 已验证✅ | — |
| [8] | Gibbs 2022 | [需人工确认] | 在CNKI/Google Scholar核实 |
| [10] | Bearman 2024 | [MATERIAL GAP] | 找到并替换真实引用 |
| [11] | Bond 2021 | [需人工确认] | 在Google Scholar核实 |

## 框架验证类

- [ ] 选择一所高校统计学课程试点实施三层AI+GAISE框架
- [ ] 收集实施前后对比数据
- [ ] 写成案例研究报告

Save this as:

```
<workdir>/academic-pipeline/
  └── researcher_action_items.md
```

Present to user:
> 📋 **Researcher Action Items 已生成**
>
> 论文中标注了 N 处需要你亲自完成的工作（数据验证、引用核实、框架实证等），
> 已整理为独立清单：<path>/researcher_action_items.md
>
> 你可以按照预估耗时排序，逐步补充完成。完成后通知我，我可以帮你将
> 补充的数据整合回论文正文。
>
> 🎉 **全流程完成！**
>
> 最终论文：<path>/final_paper.md
> 流程总结：<path>/process_summary.md
>
> 如需调整或重新运行某个阶段，请告知。

---

## Failure Handling

| Problem | Handling |
|---------|----------|
| User cancels mid-pipeline | Save all completed stage outputs. Offer to resume later. |
| Stage 2.5 fails 3 times | User must override with reasoning or abort. Cannot proceed unverified. |
| Stage 4.5 fails 3 times | Same as above. |
| Review returns Reject | Discuss: restructure (back to Stage 3) or abort. |
| Re-revise also returns Major | Force proceed to Stage 6 with acknowledged limitations (no infinite loops). |
| Stage 1 finds insufficient sources | Present options to user before proceeding (accept limited scope / broaden topic / include grey lit). |

## Prohibited State Transitions

- Cannot skip Stage 2.5 (integrity gate before writing)
- Cannot skip Stage 4.5 (citation audit before review)
- Cannot go from Stage 4 directly to Stage 6 (must pass review first)
- Cannot have more than 1 re-revise round (no infinite revision loops)

---

## Version History

- **1.1.0** (2026-06-09): Strengthened Stage 4.5 with reference-existence verification via OpenAlex API. Added no-fabrication rules. Added network-fallback pitfall for Stage 1. Created openalex_verification_protocol.md ref file.
- **1.2.0** (2026-06-10): Added Stage 6d — Researcher Action Items generator. Pipeline now produces a standalone `researcher_action_items.md` listing all unverifiable citations, material gaps, and framework validation tasks that require the human researcher's own effort. All `[需研究者...]` markers in the paper are automatically scanned and compiled into a prioritized checklist.
- **1.0.0** (2026-06-09): Initial port from Imbad0202/academic-research-skills.
