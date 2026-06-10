# Citation Verification Protocol

Use academic database APIs to verify that cited papers actually exist. This is database lookup, not general web search — permitted even in "redacted" data access mode.

## OpenAlex API

### DOI resolution (preferred)

```bash
curl -sL 'https://api.openalex.org/works/doi:10.1186/s41239-019-0171-0' | python3 -c '
import json,sys
d=json.load(sys.stdin)
print("Year:", d["publication_year"])
print("Title:", d["title"][:80])
print("Cited:", d["cited_by_count"])
'
```

### Title search (fallback if DOI fails)

```bash
curl -sL 'https://api.openalex.org/works?search={keywords}&per_page=5' | python3 -c '
import json,sys
d=json.load(sys.stdin)
for r in d["results"][:5]:
    print(r["publication_year"], r["title"][:70], r.get("doi","")[:30])
'
```

## Citation verification workflow

```
For each citation in the spot-check:
  1. Extract DOI if present
  2. Try OpenAlex DOI resolution
  3. If DOI fails, try title search with author + year + keywords
  4. Evaluate results:
     - Exact match (title + year + author match)  → VERIFIED ✅
     - Close match (same topic, same year, similar title) → LIKELY REAL ✅
     - No match at all → check other signals before flagging

Other signals to check before calling HIGH-RISK:
  - Is the journal name real? Verify it publishes on that topic
  - Are the author names real names (not "张三", "John Doe", placeholder names)?
  - Is the year plausible for the claimed contribution?
  - Does the citation have a resolvable DOI pattern (e.g., 10.xxxx/xxxxx)?
```

## Rate limits

- OpenAlex: ~10 req/s, no key required
- If hitting 429, add a 1-second gap between calls

## Limitations

- Not all papers are indexed (some journals, older papers, grey literature)
- Chinese-language papers are underrepresented
- A failed lookup is NOT proof of fabrication — always check other signals
