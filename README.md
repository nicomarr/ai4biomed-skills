# AI for Biomedical Research — Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A small collection of [Claude agent skills](https://docs.claude.com/) for biomedical literature research. Developed alongside the *LLMs for Biomedical Research* course run in partnership with [Kintampo Health Research Centre (KHRC)](https://kintampo-hrc.org/) and the [Immune Resilience research team](https://immuneresilience.github.io/) at Dalhousie University.

Each skill is a self-contained folder with a `SKILL.md`, a tested Python utility module under `scripts/`, and a pytest suite. Skills are distributed as `.skill` archives (zip files you can install into Claude Code, Claude Cowork, or any compatible runtime).

## Skills

### [`search-pubmed`](search-pubmed/)

Search NCBI's PubMed and Gene databases via the E-utilities API. Provides `search_pubmed`, `search_gene`, and `fetch_pubmed_data` — with batching, rate limiting, and XML parsing handled for you. The SKILL.md documents query construction patterns (MeSH vs. keyword, field tags, Boolean structure) and the common pitfalls (notably the quoted-MeSH-term trap that silently drops terms).

### [`search-openalex`](search-openalex/)

Query the OpenAlex API for citation counts, open-access status, related works, and decoded abstracts. Provides `search_works`, `decode_abstract`, and `doi_is_valid` — accepts bare DOIs, DOI URLs, and PMIDs interchangeably.

The two skills compose naturally: use `search-pubmed` to find relevant literature, then enrich with citation metrics from `search-openalex`. A worked example lives in the OpenAlex SKILL.md under "Enrich PubMed results with citation metrics."

## Using a skill

Each skill ships as a `.skill` archive at the root of this repo. How you load it depends on your runtime:

- **Claude Code / Claude Cowork:** install via your plugin or skill manager (see the Anthropic docs for the current mechanism in your environment).
- **Directly in Python / Jupyter:** extract the archive, `cd` into the `scripts/` directory, and `import pubmed_utils` or `import openalex_utils`. The SKILL.md inside each archive is the reference.

Both skills require `httpx` with SOCKS support and network access to `eutils.ncbi.nlm.nih.gov` and/or `api.openalex.org` respectively. Install notes live in each SKILL.md.

## Development

To run the test suites locally:

```bash
pip install "httpx[socks]" pytest --break-system-packages -q
cd search-pubmed/scripts && python -m pytest -v -p no:cacheprovider
cd ../../search-openalex/scripts && python -m pytest -v -p no:cacheprovider
```

Both suites hit live APIs, so network access is required.

Version history for each skill lives in its own `references/CHANGELOG.md`. Versioning follows semver: patch for doc fixes, minor for new functions or SKILL.md sections, major for breaking API changes.

## Citation

If these skills contribute to published work, please cite:

> Marr, N. (2026). *AI for Biomedical Research — Agent Skills* [Software]. GitHub. https://github.com/nicomarr/ai4biomed-skills

Developed alongside the [*LLMs for Biomedical Research*](https://github.com/nicomarr/ai4biomed-khrc) course (KHRC).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Nico Marr.

Each skill folder also contains a copy of the license so the `LICENSE` file travels inside the packaged `.skill` archive. The MIT license allows commercial use, modification, and redistribution with attribution; in practice this means you're free to build on these utilities in your own research or tooling, with or without affiliation to the course.
