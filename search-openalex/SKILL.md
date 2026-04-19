---
name: search-openalex
description: >
  Query the OpenAlex API for scholarly work metadata using DOIs or PMIDs via a
  tested Python module (`openalex_utils.py`). Use this skill whenever the user
  wants citation counts, open-access status, related works, or decoded abstracts
  from OpenAlex. Trigger on any mention of OpenAlex, citation metrics,
  "cited by count", open access metadata, or when the user has DOIs or PMIDs and
  wants bibliometric data beyond what PubMed provides. Also trigger when the user
  asks "how many times has this paper been cited?", "find related works", or
  wants to enrich PubMed results with citation data. Works well alongside the
  `search-pubmed` skill — use PubMed for literature search and OpenAlex for
  citation metrics and enrichment.
license: MIT
---

# OpenAlex Search Skill (v0.0.3)

This skill provides tested Python utility functions for querying the OpenAlex API. The functions live in `scripts/openalex_utils.py` relative to this SKILL.md and are designed for use in Jupyter notebooks or Python scripts.

Always import and use these functions rather than writing ad-hoc API code — they handle identifier normalization (bare DOIs, DOI URLs, PMIDs), batching for large sets, and error handling.

## Network Access Requirement

These functions make HTTP requests to `api.openalex.org`. In Cowork, this requires a custom egress rule.

**If requests fail with connection, proxy, or timeout errors**, tell the user immediately:

> To use OpenAlex search, you need to allow network access to OpenAlex servers.
> Go to **Settings → Code execution and file creation → Allow network egress**,
> set the domain allowlist to **"Package managers plus additional domains"**,
> and add **`*.openalex.org`** to the additional allowed domains list.

Do not silently retry or work around connection failures — surface this instruction right away so the user can fix it in one step.

## Setup

The module requires `httpx` with SOCKS proxy support (needed in Cowork's sandboxed environment):

```bash
pip install "httpx[socks]" --break-system-packages -q
```

Run all code from the `scripts/` directory so imports resolve correctly:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))
# Or simply: cd into the scripts/ directory before running
```

## Available Functions

### `search_works(identifiers, mailto=None)`

Retrieves OpenAlex work records for one or more identifiers. Each identifier can be:

- A **bare DOI**: `"10.1016/S0140-6736(24)00004-7"`
- A **DOI URL**: `"https://doi.org/10.1016/S0140-6736(24)00004-7"`
- A **PMID** (numeric string): `"35486828"`

The function automatically classifies each identifier, groups DOIs and PMIDs into separate batched API calls (respecting OpenAlex's 200-per-page limit), and merges the results.

Accepts a single string or a list of strings. Returns a list of OpenAlex work dicts. Raises `ValueError` on empty input.

The optional `mailto` parameter sets your email to identify the caller to OpenAlex. Historically this opted calls into the "polite pool" for faster rate limits; under OpenAlex's current credit-based rate-limit system it still works and is still recommended as a courtesy, but higher quotas now come from registering for an API key (see "API Notes" below).

### `decode_abstract(inverted_index)`

Decodes an OpenAlex inverted-index abstract into a plain-text string. OpenAlex stores abstracts as `{word: [positions]}` dicts — this function reassembles them. Returns `None` if the input is `None` or empty.

### `doi_is_valid(doi)`

Validates whether a string looks like a DOI. Accepts both bare DOIs and full `https://doi.org/` URLs. Returns a boolean.

## What OpenAlex Returns

Each work dict from `search_works()` contains rich metadata. Key fields include:

| Field | Description |
|-------|-------------|
| `id` | OpenAlex ID (e.g., `https://openalex.org/W12345`) |
| `title` | Work title |
| `doi` | DOI URL |
| `cited_by_count` | Total citation count |
| `counts_by_year` | List of `{year, cited_by_count}` dicts |
| `abstract_inverted_index` | Inverted index — pass to `decode_abstract()` |
| `related_works` | List of OpenAlex IDs for related works |
| `open_access` | Dict with `is_oa`, `oa_status`, `oa_url` |
| `authorships` | List of author dicts with affiliations |
| `publication_date` | ISO date string |
| `primary_location` | Journal/source info |
| `referenced_works` | List of OpenAlex IDs this work cites |
| `ids` | Dict with `openalex`, `doi`, `pmid`, `pmcid` mappings |

## Typical Workflows

### Get citation data for DOIs

```python
from openalex_utils import search_works, decode_abstract

works = search_works([
    "10.1016/S0140-6736(24)00004-7",
    "10.1111/tmi.14062",
])

for w in works:
    print(f"{w['title']}")
    print(f"  Citations: {w['cited_by_count']}")
    print(f"  OA: {w['open_access']['oa_status']}")
    abstract = decode_abstract(w.get("abstract_inverted_index"))
    if abstract:
        print(f"  Abstract: {abstract[:150]}...")
    print()
```

### Enrich PubMed results with citation metrics

This is the most common pattern — search PubMed for articles, then enrich with OpenAlex data:

```python
from pubmed_utils import search_pubmed, fetch_pubmed_data
from openalex_utils import search_works

# 1. Search PubMed
result = search_pubmed('"sickle cell disease"[mh] AND CRISPR[tiab]')
pmids = result['idlist'][:10]

# 2. Fetch PubMed metadata
articles = fetch_pubmed_data(pmids)

# 3. Enrich with OpenAlex citation data (using DOIs from PubMed)
dois = [a['doi'] for a in articles if a.get('doi')]
oa_works = search_works(dois)

# 4. Build a lookup by DOI
oa_by_doi = {w['doi']: w for w in oa_works}

for a in articles:
    doi_url = f"https://doi.org/{a['doi']}" if a.get('doi') else None
    oa = oa_by_doi.get(doi_url, {})
    print(f"{a['title']}")
    print(f"  Citations: {oa.get('cited_by_count', 'N/A')}")
```

### Look up works by PMID

If you have PMIDs and want OpenAlex data without going through PubMed first:

```python
from openalex_utils import search_works

works = search_works(["35486828", "33264437"])
for w in works:
    print(f"{w['title']} — {w['cited_by_count']} citations")
```

### Citation trends over time

```python
from openalex_utils import search_works

works = search_works(["10.1016/S0140-6736(24)00004-7"])
if works:
    w = works[0]
    print(f"{w['title']}")
    for yr in sorted(w.get("counts_by_year", []), key=lambda x: x["year"]):
        print(f"  {yr['year']}: {yr['cited_by_count']} citations")
```

## API Notes

- **Rate limits**: OpenAlex now uses a credit-based rate-limit system. Anonymous calls still succeed and return real data (responses include `x-ratelimit-limit`, `x-ratelimit-remaining`, and `x-ratelimit-cost-usd` headers, with each `/works` filter call costing roughly $0.0001 against a ~$1/day anonymous budget). Passing `mailto=` still works as a courtesy identifier. For production or high-volume use, register for an API key at https://openalex.org/ and pass it via OpenAlex's authenticated request pattern (see their docs) for higher quotas.
- **Batching**: The function automatically batches requests when more than 200 identifiers are provided (OpenAlex's `per-page` maximum).
- **Missing works**: Works not found in OpenAlex are silently omitted — the filter endpoint returns HTTP 200 with zero results for unresolvable IDs rather than an error. Compare `len(results)` to your input count to detect missing entries.
- **PMIDs**: Internally this module resolves PMIDs via the `ids.pmid:https://pubmed.ncbi.nlm.nih.gov/<PMID>` filter URL form. OpenAlex also accepts the shorter `pmid:<PMID>` URN form for single-ID lookups. Not all PMIDs have corresponding OpenAlex records.

## Running Tests

```bash
cd scripts/
python -m pytest test_openalex_utils.py -v -p no:cacheprovider
```

26 tests covering DOI validation, abstract decoding, DOI lookups, PMID lookups, mixed-identifier queries, and edge cases. All require network access to `api.openalex.org`.

## Version & Changelog

Current version: **v0.0.3**. Full version history lives in [`references/CHANGELOG.md`](references/CHANGELOG.md). Versioning follows semver — patch for doc/example fixes, minor for new functions or SKILL.md sections, major for breaking changes to `openalex_utils.py`. The version appears in the H1 above; the skill frontmatter does not carry a `version` field because Anthropic's skill validator only accepts `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. To bump the version, add a new entry to `references/CHANGELOG.md` and update the suffix on the H1.

## License

MIT — see [LICENSE](LICENSE) shipped with this skill, or the top-level [`LICENSE`](../LICENSE) in the repository. Copyright (c) 2026 Nico Marr.
