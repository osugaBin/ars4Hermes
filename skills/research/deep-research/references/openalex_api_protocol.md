# OpenAlex API Protocol

Fallback retrieval method when `web_search` (DuckDuckGo backend) times out. OpenAlex is the most reliable academic API from networks that block international search engines.

## Basic search

```bash
curl -sL 'https://api.openalex.org/works?search={query}&per_page=10'
```

Returns JSON with `results` array. Each result contains:
- `title` — paper title
- `publication_year` — year
- `doi` — DOI URL (if available)
- `cited_by_count` — citation count
- `primary_location.source.display_name` — journal/venue name
- `primary_location.landing_page_url` — paper URL
- `open_access.oa_url` — open access URL

## Python parsing template

```bash
curl -sL 'https://api.openalex.org/works?search={query}&per_page=10' | python3 -c '
import json,sys
d=json.load(sys.stdin)
for r in d["results"]:
    title = r.get("title") or ""
    year = r.get("publication_year")
    doi = r.get("doi") or ""
    cited = r.get("cited_by_count", 0)
    print(f"[{year}] {title[:90]}")
    if doi: print(f"  DOI: {doi}")
    print(f"  Cited: {cited}")
'
```

## Search by DOI (exact match)

```bash
curl -sL 'https://api.openalex.org/works/doi:10.1186/s41239-019-0171-0'
```

Use this for citation verification in Stage 2.5 integrity gates.

## Filter by year range

```bash
curl -sL 'https://api.openalex.org/works?search={query}&filter=publication_year:2020-2025&per_page=10'
```

## Filter by concept

```bash
curl -sL 'https://api.openalex.org/works?filter=concepts.display_name:Statistics+education&search={query}'
```

## Rate limits

- No API key required
- Rate limit: ~10 requests per second (very generous)
- If you get 429 (Too Many Requests), add a 1-second delay between calls

## When to use

- `web_search` fails (network blocks DuckDuckGo/Google/Brave) — switch after 2-3 attempts
- Need verified citation metadata for integrity gate
- Need citation counts for evidence strength grading

## Limitations

- Returns paper metadata, not full text — cannot verify individual claims
- Coverage is strongest in English-language journals; Chinese-language sources may be underrepresented
- Abstracts are truncated in the returned JSON; use `&select=title,publication_year,abstract_inverted_index,cited_by_count,doi` to get specific fields
