# Anti-Leakage Protocol (Knowledge Isolation)

## Purpose

Prevent the LLM from fabricating content (methodology, citations, data) that is not in the user's provided materials.

## When to activate

Activate when ALL of these are true:
- User has provided research materials (deep-research report, bibliography, experimental data)
- Paper mode is `full` or `revision`
- Materials are substantive (not placeholder stubs)

## Do NOT activate when:
- Mode is `outline-only` or `abstract-only`
- User explicitly requests LLM to supplement with its own knowledge
- Materials are too minimal to write from

## Core rules

1. **PREFER** session materials over parametric knowledge for ALL factual claims
2. Every claim MUST be traceable to a source in the provided bibliography
3. If materials don't cover a required topic → flag `[MATERIAL GAP]` — do NOT fill from memory
4. Do NOT introduce references not present in the provided bibliography
5. Methods section must describe ONLY what is documented — do not infer or interpolate

## [MATERIAL GAP] handling

1. Flag the gap at the point it occurs in the draft
2. Surface all gaps at the next checkpoint
3. User can provide additional material OR authorize LLM supplementation
4. If supplemented: tag as `[LLM-SUPPLEMENTED]`

The Methods section gets special treatment — do NOT supplement methodology from memory. If the user didn't provide their methodology, they must write it or provide data.
