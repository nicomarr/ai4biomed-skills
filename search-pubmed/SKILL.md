---
name: search-pubmed
description: >
  Search PubMed and NCBI Gene databases programmatically using the E-utilities API via
  a tested Python module (`pubmed_utils.py`). Use this skill whenever the user wants to
  search PubMed for articles, look up genes in NCBI, retrieve article metadata (titles,
  abstracts, authors, DOIs), or build literature search workflows in Python. Trigger on
  any mention of PubMed, NCBI, PMID, MeSH, E-utilities, biomedical literature search,
  gene lookup, or when the user asks to find research papers on a biomedical topic. Also
  trigger when the user uploads or references a list of PubMed IDs and wants to fetch
  article details, or when they want to construct complex PubMed queries with field tags
  and boolean operators. Even if the user doesn't mention PubMed by name, trigger this
  skill when they ask to "find papers on...", "search the literature for...", or "look up
  articles about..." any biomedical topic.
license: MIT
---

# PubMed & NCBI Search Skill (v0.0.3)

This skill provides three tested Python utility functions for querying NCBI's Entrez E-utilities API. The functions live in `scripts/pubmed_utils.py` relative to this SKILL.md, and are designed for use in Jupyter notebooks or Python scripts.

Always import and use these functions rather than writing ad-hoc API code — they handle batching, rate limiting, XML parsing edge cases (inline markup in titles/abstracts), and input validation.

## Network Access Requirement

These functions make HTTP requests to `eutils.ncbi.nlm.nih.gov`. In Claude Chat or Claude Cowork, this requires a custom egress rule.

**If requests fail with connection, proxy, or timeout errors**, tell the user immediately:

> To use PubMed search, you need to allow network access to NCBI servers.
> Go to **Settings → Code execution and file creation → Allow network egress**,
> set the domain allowlist to **"Package managers plus additional domains"**,
> and add **`*.ncbi.nlm.nih.gov`** to the additional allowed domains list.

Do not silently retry or work around connection failures — surface this instruction right away so the user can fix it in one step.

## Setup

The module requires `httpx` with SOCKS proxy support (needed in Chat or Cowork's sandboxed environment):

```bash
pip install "httpx[socks]" --break-system-packages -q
```

Run all code from the `scripts/` directory so imports resolve correctly:

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname("__file__"), "scripts"))
# Or simply: cd into the scripts/ directory before running
```

## Available Functions

### `search_pubmed(query, retmax=1000)`

Searches PubMed via the ESearch endpoint. Returns a dict with `count` (total matches as string), `idlist` (list of PMID strings), `querytranslation` (how PubMed interpreted the query), and pagination fields.

### `search_gene(query, retmax=100)`

Searches the NCBI Gene database via ESearch. Same return structure as `search_pubmed` but queries the gene database. Returns Gene IDs (not PMIDs).

### `fetch_pubmed_data(pmids, retmax_per_request=200, rate_limit_delay=0.34)`

Fetches article metadata for a list of PMIDs via the EFetch endpoint. Handles batching and NCBI rate limiting automatically. Returns a list of dicts, each containing: `pmid`, `title`, `abstract`, `authors` (list), `journal`, `pub_date`, `doi`.

Accepts a `List[str]` of PMIDs. Also tolerates comma-separated strings and stringified lists for notebook convenience.

## Writing Effective PubMed Queries

The quality of results depends heavily on query construction. PubMed doesn't do semantic search — it matches field tags and MeSH terms, so a well-crafted query is the difference between relevant results and noise.

### Plan Before You Query

Before constructing a PubMed query, think through these steps systematically (in a markdown cell or comment if working in a notebook). This planning step is what separates a query that ideally returns 20 or 30 and up to a hundred relevant papers from one that returns hundreds or thousands of tangential ones.

1. **Term variations** — List all the ways the concept/gene/disease might be referenced: official names, common aliases, abbreviations, protein names, alternative spellings. For genes especially, include the official symbol, full name, and any well-known aliases (e.g., TP53 / "tumor protein p53" / p53).

2. **MeSH mapping** — For each major concept, identify the corresponding MeSH term. MeSH terms automatically capture synonyms and are the single most effective way to improve PubMed search quality. Be aware that a common name and the canonical MeSH heading often differ (e.g., "sickle cell disease" is an entry term that maps to the heading **Anemia, Sickle Cell**; "gene therapy" maps to **Genetic Therapy**). When in doubt, verify the heading in the [MeSH Database](https://www.ncbi.nlm.nih.gov/mesh/).

3. **Boolean structure** — Plan how terms combine: OR within concept groups (synonyms), AND between concept groups. Map out the parentheses grouping before writing the query string.

4. **Filters** — Decide on date ranges, language, species, publication types. Each filter should have a reason.

5. **Precision vs recall** — A broad query finds everything but buries you in noise. A narrow query is clean but misses relevant work. Aim for the tightest query that still gives adequate coverage for the user's purpose.

### Field Tags

| Tag | Field | Use for |
|-----|-------|---------|
| `[MeSH Terms]` or `[mh]` | MeSH Heading | Controlled vocabulary — best for concepts |
| `[Title/Abstract]` or `[tiab]` | Title + Abstract | Broader keyword search |
| `[ti]` | Title only | Precise topic matching |
| `[Author]` or `[au]` | Author | Author searches |
| `[Date - Publication]` or `[dp]` | Date Published | Date filtering |
| `[Publication Type]` or `[pt]` | Publication Type | Filter by study type (Clinical Trial, Review, etc.) |
| `[Language]` or `[la]` | Language | Language filtering |
| `[sym]` | Gene Symbol | Gene database only |
| `[Organism]` | Species | Gene database only |

### PubMed Character Rules

Certain characters have special meaning in PubMed queries — using them incorrectly causes silent failures or unexpected results.

**Characters with special meaning** (use intentionally):
`( )` Boolean grouping, `[ ]` field tags, `&` AND, `|` OR, `/` MeSH/subheading combos, `:` range operator, `" "` phrase search, `#` history reference, `*` wildcard truncation

**Characters converted to spaces** (avoid in search terms):
`! # $ % + - . , ; < > = ? \ ^ _ { } ~ '`

This matters because a query containing hyphens or periods in unexpected places will silently return different results than intended. For example, `CRISPR-Cas9` is searched as `CRISPR Cas9` (two separate terms). To search it as a phrase, wrap it: `"CRISPR-Cas9"`.

**Important — quotes and `[MeSH Terms]`**: do **not** quote a MeSH term unless you know the exact canonical heading. Quoting with `[MeSH Terms]` turns off entry-term mapping, so a common-name entry term (e.g., `"sickle cell disease"[MeSH Terms]`) fails to resolve to its heading ("Anemia, Sickle Cell") and PubMed silently drops the term with the warning "The following term was ignored". The safe default is unquoted: `sickle cell disease[MeSH Terms]`.

### Query Construction Patterns

**Use MeSH terms for concepts** — they capture synonyms automatically. `sickle cell disease[MeSH Terms]` matches articles tagged with the corresponding MeSH heading (Anemia, Sickle Cell) via entry-term mapping, even if the articles use different wording:
```python
result = search_pubmed('sickle cell disease[MeSH Terms] AND gene editing[MeSH Terms]')
```

**Combine MeSH + keyword aliases for comprehensive gene searches:**
```python
# Cover the gene through MeSH, symbol, full name, and common alias
result = search_pubmed(
    '(BRCA1[MeSH Terms] OR "BRCA1"[Title/Abstract] OR "breast cancer 1"[Title/Abstract])'
    ' AND (humans[MeSH Terms])'
    ' AND ("2010"[Date - Publication] : "2024"[Date - Publication])'
)
```

**Use `[tiab]` for specific phrases** that MeSH might not cover:
```python
result = search_pubmed('"CRISPR-Cas9"[tiab] AND "sickle cell"[tiab]')
```

**Combine MeSH + keywords for precision with coverage:**
```python
# MeSH for the broad concept + keyword for the specific technique
result = search_pubmed('sickle cell disease[MeSH Terms] AND CRISPR[tiab] AND therapy[tiab]')
```

**Multi-concept query with full Boolean structure:**
```python
# Use the canonical MeSH heading (not the gene symbol) for the MeSH clause.
# "TP53[MeSH Terms]" would be silently dropped — TP53 isn't a heading.
result = search_pubmed(
    '(Tumor Suppressor Protein p53[MeSH Terms] OR "tumor protein p53"[Title/Abstract] OR p53[Title/Abstract])'
    ' AND (neoplasms[MeSH Terms] OR cancer[tiab])'
    ' AND English[Language]'
)
```

**Filter by date** to get recent work:
```python
result = search_pubmed('gene therapy[MeSH Terms] AND ("2022"[Date - Publication] : "3000"[Date - Publication])')
```

**Filter by publication type** for clinical evidence:
```python
result = search_pubmed('sickle cell disease[MeSH Terms] AND "Clinical Trial"[Publication Type]')
```

**Gene lookups** — always restrict by organism:
```python
result = search_gene('TP53[sym] AND "Homo sapiens"[Organism]')
```

### Common Pitfalls

- **Too broad**: `cancer AND treatment` → millions of results, mostly irrelevant. Add MeSH terms, field tags, and date ranges.
- **No field tags**: bare keywords get searched across all fields, pulling in tangential matches. Always use `[tiab]`, `[ti]`, or `[MeSH Terms]` for key concepts.
- **Relying on keyword search alone**: PubMed's strength is MeSH. Use it.
- **Missing aliases**: Searching only `BRCA1[tiab]` misses articles that use "breast cancer 1" or the MeSH heading. OR together all known names.
- **Quoting a MeSH term with a common name**: `"sickle cell disease"[MeSH Terms]` returns zero results and triggers "The following term was ignored" because quotes disable entry-term mapping and the actual MeSH heading is "Anemia, Sickle Cell". Drop the quotes (`sickle cell disease[MeSH Terms]`) and let PubMed's entry-term mapping handle the synonym.
- **Escape sequences in queries**: Never include `\n`, `\t`, or other escape sequences in the query string. These can silently break Boolean operators (e.g., `\nOR` becomes `nOR` and is ignored).

## Typical Workflow

A common pattern is search → fetch → analyze:

```python
from pubmed_utils import search_pubmed, fetch_pubmed_data

# 1. Search — use MeSH + keywords for best results
result = search_pubmed('sickle cell disease[mh] AND CRISPR[tiab] AND ("2022"[dp] : "3000"[dp])')
pmids = result['idlist']
print(f"Found {result['count']} articles, retrieved {len(pmids)} IDs")

# 2. Fetch metadata
articles = fetch_pubmed_data(pmids)

# 3. Work with the data
for a in articles[:5]:
    print(f"• {a['title']}")
    print(f"  {a['authors'][0]} et al. — {a['journal']} ({a['pub_date']})")
    print(f"  DOI: {a['doi']}\n")
```

## Rate Limiting

NCBI allows 3 requests/second without an API key. `fetch_pubmed_data` handles this with a default 0.34s delay between batches. For large-scale work, register for an NCBI API key to get 10 requests/second.

## Running Tests

```bash
cd scripts/
python -m pytest test_pubmed_utils.py -v -p no:cacheprovider
```

Use `-p no:cacheprovider` to avoid permission issues with pytest's cache directory in restricted environments.

## Version & Changelog

Current version: **v0.0.3**. Full version history lives in [`references/CHANGELOG.md`](references/CHANGELOG.md). Versioning follows semver — patch for doc/example fixes, minor for new functions or SKILL.md sections, major for breaking changes to `pubmed_utils.py`. The version appears in the H1 above; the skill frontmatter does not carry a `version` field because Anthropic's skill validator only accepts `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`. To bump the version, add a new entry to `references/CHANGELOG.md` and update the suffix on the H1.

## License

MIT — see [LICENSE](LICENSE) shipped with this skill, or the top-level [`LICENSE`](../LICENSE) in the repository. Copyright (c) 2026 Nico Marr.
