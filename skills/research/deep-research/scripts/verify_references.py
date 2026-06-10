#!/usr/bin/env python3
"""
verify_references.py — Batch reference verification via OpenAlex API

Usage:
    python3 verify_references.py < input.txt
    python3 verify_references.py --dois "10.1186/s41239-019-0171-0,10.1016/j.caeai.2020.100001"

Input format (stdin or --dois):
    One DOI per line, OR comma-separated list with --dois

Output:
    For each DOI, prints:
    VERIFIED | year | title | cited_by | doi
    NOT_FOUND | doi | [reason]

Requires: curl, Python 3
"""
import sys, subprocess, json, re

OPENALEX_BASE = "https://api.openalex.org/works"

def verify_doi(doi):
    """Verify a single DOI via OpenAlex."""
    doi = doi.strip().rstrip(".")
    if not doi:
        return None
    # Normalize: strip URL prefix if present
    doi = re.sub(r"^https?://doi\.org/", "", doi)
    url = f"{OPENALEX_BASE}/doi:{doi}"
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if r.returncode != 0 or not r.stdout.strip():
            return ("API_ERROR", doi, "curl failed or empty response")
        d = json.loads(r.stdout)
        year = d.get("publication_year", "?")
        title = d.get("title", "")[:80]
        cited = d.get("cited_by_count", 0)
        return ("VERIFIED", year, title, cited, doi)
    except json.JSONDecodeError:
        return ("NOT_FOUND", doi, "DOI does not resolve in OpenAlex")
    except Exception as e:
        return ("API_ERROR", doi, str(e)[:60])

def search_by_title(title_keywords):
    """Search OpenAlex by title keywords when DOI fails."""
    url = f"{OPENALEX_BASE}?search={title_keywords}&per_page=3&sort=relevance"
    try:
        r = subprocess.run(
            ["curl", "-sL", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        d = json.loads(r.stdout)
        results = d.get("results", [])
        if not results:
            return None
        out = []
        for res in results[:3]:
            year = res.get("publication_year", "?")
            title = res.get("title", "")[:80]
            doi = res.get("doi", "") or ""
            cited = res.get("cited_by_count", 0)
            out.append((year, title, cited, doi))
        return out
    except:
        return None

def main():
    dois = []
    if "--dois" in sys.argv:
        idx = sys.argv.index("--dois")
        raw = sys.argv[idx + 1]
        dois = [d.strip() for d in raw.split(",") if d.strip()]
    else:
        for line in sys.stdin:
            line = line.strip()
            if line:
                dois.append(line)

    if not dois:
        print("No DOIs provided. Pass via stdin (one per line) or --dois 'doi1,doi2'")
        sys.exit(1)

    print(f"Verifying {len(dois)} references via OpenAlex...")
    print()
    verified_count = 0
    not_found_count = 0

    for doi in dois:
        result = verify_doi(doi)
        if result and result[0] == "VERIFIED":
            _, year, title, cited, d = result
            print(f"  ✅ {doi}")
            print(f"     [{year}] {title}")
            print(f"     Cited: {cited}")
            verified_count += 1
        elif result and result[0] == "NOT_FOUND":
            _, d, reason = result
            print(f"  ❌ {d}")
            print(f"     {reason}")
            print(f"     → Try title search via the deep-research skill's OpenAlex protocol")
            not_found_count += 1
        else:
            print(f"  ⚠️  {doi}")
            if result:
                print(f"     {result[2]}")
            not_found_count += 1
        print()

    print(f"=== Summary ===")
    print(f"Verified: {verified_count}/{len(dois)}")
    print(f"Not found / Error: {not_found_count}/{len(dois)}")
    if not_found_count > 0:
        print(f"ACTION REQUIRED: {not_found_count} reference(s) could not be verified.")
        print(f"Mark them with [需人工确认] in the draft. Do NOT silently remove or fabricate details.")

if __name__ == "__main__":
    main()
