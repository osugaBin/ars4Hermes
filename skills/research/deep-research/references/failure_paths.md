# Failure Paths — Research Pipeline Failure Map

## Summary

| # | Failure Scenario | Affected Modes | Severity | Handling |
|---|-----------------|----------------|----------|----------|
| F1 | Research question cannot converge | full, socratic | Medium | Offer candidate RQs, suggest lit-review first |
| F2 | Insufficient literature (< min for mode) | full, quick, lit-review | High | Expand search (synonyms, broader terms, relax date range) |
| F3 | Methodology mismatch | full | High | Offer alternative methods, adjust RQ |
| F4 | All sources below quality threshold | full, fact-check | High | Downgrade expectations, mark all findings with caveats |
| F5 | Conclusions inconsistent with evidence | full | High | Return to cross-validation phase |
| F6 | Socratic dialogue doesn't converge | socratic | Medium | Suggest full mode after 10 rounds; auto-compile at 15 |
| F7 | User abandons mid-process | all | Low | Save progress summary, offer to resume later |
| F8 | Only grey/low-quality literature found | full, lit-review | Medium | Accept as exploratory, adjust report positioning |
| F9 | Source extraction fails for key sources | all | Medium | Use browser fallback; if still fails, note "content inaccessible" |
| F10 | Cross-validation yields no consensus | full, lit-review | Medium | Report as contradictory with evidence from each side |
| F11 | Citation cannot be verified | systematic-review | Medium | Remove from report, note `[UNVERIFIED CITATION — removed]` |

## Detailed Handling

### F1: RQ Cannot Converge
- After 3+ rounds of back-and-forth with no clear direction
- Produce 3 candidate RQs with brief rationale
- If user still can't choose -> suggest lit-review mode to explore literature first

### F2: Insufficient Literature
- If < 5 usable sources found:
  1. Expand search (synonyms, broader terms, adjacent disciplines)
  2. Relax date range (5 -> 10 years)
  3. Add grey literature (reports, policy docs, working papers)
  4. If still insufficient -> tell user, offer options

### F6: Socratic Dialogue Not Converging
- At 10 rounds: suggest switching to full mode
- At 15 rounds: auto-compile INSIGHTs and end

### F7: User Abandons
- Compile a Progress Summary of what's been done
- Offer to save and resume later
- Do not push for continuation
