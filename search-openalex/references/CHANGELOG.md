# Changelog — search-openalex skill

All notable changes to this skill are recorded here. Versioning follows semver:

- **Patch** (`0.0.x`) — documentation fixes, example corrections, non-breaking clarifications.
- **Minor** (`0.x.0`) — new utility functions, new SKILL.md sections, or new query patterns.
- **Major** (`x.0.0`) — breaking changes to the public API of `openalex_utils.py` (function signatures, return shapes).

## 0.0.3 — 2026-04-19

### Added

- **MIT license.** The skill is now explicitly licensed under MIT. `license: MIT` (SPDX identifier) has been added to the frontmatter — this is an Anthropic-recognized validator key, not a free-form addition. A `LICENSE` file has been dropped into the skill folder so it travels inside the `.skill` archive, and the top-level repository `LICENSE` (identical text) is the canonical source.
- **SPDX + copyright headers on Python files.** `openalex_utils.py` and `test_openalex_utils.py` now carry a two-line SPDX header (`# SPDX-License-Identifier: MIT` + `# Copyright (c) 2026 Nico Marr`) at the top. This is belt-and-braces for users who extract individual files from the `.skill` archive and drop them into their own projects.
- **`## License` section at the end of SKILL.md**, pointing at the bundled `LICENSE` and the repo-root `LICENSE` and naming the copyright holder.

### Rationale

MIT was chosen over CC BY-NC (the course materials license) because Creative Commons explicitly advises against using CC licenses for software, and "NonCommercial" creates real friction for reusable utility code (industry researchers, CI pipelines, plugin marketplaces). MIT over Apache-2.0 because the skills are thin wrappers around public APIs with no patentable novelty, the scientific Python ecosystem leans MIT/BSD, and Apache's NOTICE-file overhead isn't justified for this scope.

## 0.0.2 — 2026-04-19

### Fixed

- **`MAX_PER_PAGE` raised from 50 to 200.** The previous value understated OpenAlex's actual per-page ceiling. Direct testing against the live `/works` endpoint confirms that `per-page=200` returns HTTP 200 with full results, while `per-page=201` returns HTTP 400. Setting the constant to 200 cuts the number of API calls (and therefore the rate-limit credits consumed) by 4× for large identifier sets. The constant is also the batch size used by `search_works`, so batching now chunks identifiers in groups of 200 instead of 50.
- **"50-per-page limit" references corrected to 200.** Both the docstring on `search_works` (in `openalex_utils.py`) and the two mentions in SKILL.md ("respecting OpenAlex's 50-per-page limit" and "batches requests when more than 50 identifiers are provided") now state 200.

### Changed

- **Rate-limits section rewritten.** The previous note described a simple "polite pool via `mailto`" model, which no longer reflects OpenAlex's current behavior. The live API now returns credit-based rate-limit headers (`x-ratelimit-limit`, `x-ratelimit-remaining`, `x-ratelimit-cost-usd`) on every response, with anonymous calls drawing from a shared daily budget (~$1/day, at ~$0.0001 per filter call). `mailto` still works as a courtesy identifier, but higher quotas now come from registering an API key. The SKILL.md now describes this accurately and points users at https://openalex.org/ for key registration rather than implying that `mailto` alone grants "faster limits".
- **`mailto` parameter description in `search_works` section softened.** It no longer claims the polite pool "provides faster rate limits" — that was true under the old policy but is now misleading. The description now says `mailto` still works and is still recommended as a courtesy, while directing users to the API Notes section for the current picture.
- **PMID filter note clarified.** The previous note said OpenAlex "resolves PMIDs via `https://pubmed.ncbi.nlm.nih.gov/<PMID>` format internally" — which is what the module does. It now additionally notes that the shorter `pmid:<PMID>` URN form also works for single-ID lookups, so users writing their own queries aren't forced to construct PubMed URLs.
- **Missing-works behavior described more precisely.** The previous note said missing works are "silently omitted" — correct, but vague. The updated note explains *why*: the filter endpoint returns HTTP 200 with zero results for unresolvable IDs rather than a 404 or error, so the silent omission is the API's behavior, not a bug in the module.

### Added

- **Version suffix on the H1 title** (`# OpenAlex Search Skill (v0.0.2)`) so the version is visible at a glance when opening the file. The frontmatter intentionally does **not** carry a `version` key — Anthropic's skill validator (`skill-creator/scripts/quick_validate.py`) only accepts `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`, and would reject any unknown key.
- **"Version & Changelog" section** at the end of SKILL.md, mirroring the pattern used in the sibling `search-pubmed` skill, pointing at `references/CHANGELOG.md`.
- **This CHANGELOG.md as a reference file** so version history has a paper trail.

### Verified

Direct testing against the live OpenAlex `/works` endpoint confirmed:

| Check | Result |
|---|---|
| `per-page=50` | HTTP 200, 50 results per page |
| `per-page=200` | HTTP 200, 200 results per page |
| `per-page=201` | HTTP 400 (over the cap) |
| Anonymous call without `mailto` | HTTP 200, full data, rate-limit headers present |
| Call with `mailto=` | HTTP 200, same data |
| Unresolvable DOI (`10.9999/...`) via filter | HTTP 200, empty `results` |
| Unresolvable PMID (`9999999999`) via filter | HTTP 200, empty `results` |
| `pmid:35486828` URN filter | HTTP 200, 1 result (same as URL form) |
| `ids.pmid:https://pubmed.ncbi.nlm.nih.gov/35486828` filter | HTTP 200, 1 result |

Rate-limit response headers observed on anonymous calls: `x-ratelimit-limit: 10000`, `x-ratelimit-remaining: 9963`, `x-ratelimit-cost-usd: 0.0001`, `x-ratelimit-remaining-usd: 0.9963`.

## 0.0.1 — Initial release

Initial version of the `search-openalex` skill providing three tested Python utilities in `scripts/openalex_utils.py`:

- `search_works(identifiers, mailto=None)` — retrieves OpenAlex work records by DOI or PMID, with automatic identifier classification, batching, and error handling.
- `decode_abstract(inverted_index)` — reassembles OpenAlex inverted-index abstracts into plain text.
- `doi_is_valid(doi)` — validates DOI strings (accepts bare DOIs and `https://doi.org/` URLs).

SKILL.md documented the three functions, returned fields, and typical workflows: citation lookups by DOI, enriching PubMed results with citation metrics, PMID-based lookups, and citation trends over time. 26 tests in `scripts/test_openalex_utils.py` cover DOI validation, abstract decoding, DOI lookups, PMID lookups, mixed-identifier queries, and edge cases.
