# Changelog — search-pubmed skill

All notable changes to this skill are recorded here. Versioning follows semver:

- **Patch** (`0.0.x`) — documentation fixes, example corrections, non-breaking clarifications.
- **Minor** (`0.x.0`) — new utility functions, new SKILL.md sections, or new query patterns.
- **Major** (`x.0.0`) — breaking changes to the public API of `pubmed_utils.py` (function signatures, return shapes).

## 0.0.3 — 2026-04-19

### Added

- **MIT license.** The skill is now explicitly licensed under MIT. `license: MIT` (SPDX identifier) has been added to the frontmatter — this is an Anthropic-recognized validator key, not a free-form addition. A `LICENSE` file has been dropped into the skill folder so it travels inside the `.skill` archive, and the top-level repository `LICENSE` (identical text) is the canonical source.
- **SPDX + copyright headers on Python files.** `pubmed_utils.py` and `test_pubmed_utils.py` now carry a two-line SPDX header (`# SPDX-License-Identifier: MIT` + `# Copyright (c) 2026 Nico Marr`) at the top. This is belt-and-braces for users who extract individual files from the `.skill` archive and drop them into their own projects.
- **`## License` section at the end of SKILL.md**, pointing at the bundled `LICENSE` and the repo-root `LICENSE` and naming the copyright holder.

### Rationale

MIT was chosen over CC BY-NC (the course materials license) because Creative Commons explicitly advises against using CC licenses for software, and "NonCommercial" creates real friction for reusable utility code (industry researchers, CI pipelines, plugin marketplaces). MIT over Apache-2.0 because the skills are thin wrappers around public APIs with no patentable novelty, the scientific Python ecosystem leans MIT/BSD, and Apache's NOTICE-file overhead isn't justified for this scope.

## 0.0.2 — 2026-04-19

### Fixed

- **Quoted MeSH terms no longer used in examples.** Wrapping a common-name entry term in double quotes before `[MeSH Terms]` disables PubMed's entry-term mapping and causes the term to be silently dropped (PubMed surfaces a "The following term was ignored" warning and returns zero results). The previous examples using `"sickle cell disease"[MeSH Terms]`, `"gene therapy"[MeSH Terms]`, and `"sickle cell"[MeSH Terms]` all fell into this trap because the actual MeSH headings are "Anemia, Sickle Cell" and "Genetic Therapy", not the common names. All MeSH examples are now unquoted so entry-term mapping resolves them correctly.
- **Multi-concept Boolean example no longer silently drops the gene MeSH clause.** The previous example used `TP53[MeSH Terms]`, which PubMed's API reports under `errorlist.phrasesnotfound` — the MeSH part was dropped and only the `[tiab]` aliases were doing work. The canonical MeSH heading is "Tumor Suppressor Protein p53"; the example now uses that and returns a clean translation with no dropped phrases.
- **Redundant MeSH clause removed.** `cancer[MeSH Terms] OR neoplasm[MeSH Terms]` both mapped to the same heading ("Neoplasms"); the example now uses `neoplasms[MeSH Terms] OR cancer[tiab]` to demonstrate a MeSH + tiab OR pattern with actually distinct search coverage.

### Added

- **"Important — quotes and `[MeSH Terms]`" callout** in the Character Rules section, explaining the entry-term mapping behavior and the failure mode.
- **New "Common Pitfalls" bullet** describing the quoted-MeSH-term trap with the exact "The following term was ignored" warning text.
- **Note on canonical MeSH headings** in the "MeSH mapping" planning bullet, with a link to the NLM MeSH Database.
- **Version suffix on the H1 title** (`# PubMed & NCBI Search Skill (v0.0.2)`) so the version is visible at a glance when opening the file. The frontmatter intentionally does **not** carry a `version` key — Anthropic's skill validator (`skill-creator/scripts/quick_validate.py`) only accepts `name`, `description`, `license`, `allowed-tools`, `metadata`, and `compatibility`, and would reject any unknown key.
- **This CHANGELOG.md as a reference file** so version history has a paper trail.

### Verified

All example queries were run against the live E-utilities ESearch endpoint. Result counts and translations confirmed:

| Example | Count | Notes |
|---|---:|---|
| `sickle cell disease[MeSH Terms] AND gene editing[MeSH Terms]` | 178 | Translates via entry-term mapping to `"anemia, sickle cell"[MeSH Terms]` |
| BRCA1 + aliases + humans + 2010–2024 | 12,530 | `BRCA1[MeSH Terms]` → `"genes, brca1"[MeSH Terms]` |
| `"CRISPR-Cas9"[tiab] AND "sickle cell"[tiab]` | 187 | Clean |
| sickle cell + CRISPR + therapy | 76 | Clean |
| Tumor Suppressor Protein p53 + aliases + neoplasms/cancer + English | 82,791 | No dropped phrases (previously `TP53[MeSH Terms]` was dropped) |
| gene therapy + 2022–3000 | 5,957 | Translates to `"genetic therapy"[MeSH Terms]` |
| sickle cell + Clinical Trial | 1,148 | Clean |
| `TP53[sym] AND "Homo sapiens"[Organism]` (gene DB) | 1 | Human TP53 record |
| Typical workflow (sickle cell + CRISPR + 2022–3000) | 77 | Clean |

## 0.0.1 — Initial release

Initial version of the `search-pubmed` skill providing three tested Python utilities in `scripts/pubmed_utils.py`:

- `search_pubmed(query, retmax=1000)` — ESearch wrapper for PubMed.
- `search_gene(query, retmax=100)` — ESearch wrapper for NCBI Gene.
- `fetch_pubmed_data(pmids, retmax_per_request=200, rate_limit_delay=0.34)` — EFetch wrapper with batching, rate limiting, and XML parsing.

SKILL.md documented query construction patterns, field tags, character rules, and a typical search → fetch → analyze workflow.
