# AI for Biomedical Research — Agent Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/nicomarr/ai4biomed-skills)

A small collection of [Agent Skills](https://agentskills.io/) for biomedical literature research. Developed alongside the *LLMs for Biomedical Research* course run in partnership with [Kintampo Health Research Centre](https://kintampo-hrc.org/) and the [Immune Resilience research team](https://immuneresilience.github.io/) at Dalhousie University.

Each skill is a self-contained folder with a `SKILL.md`, a tested Python utility module under `scripts/`, and a pytest suite. Each skill installs into any [Agent Skills-compatible agent product](https://agentskills.io/clients).

## Skills

### [`search-pubmed`](search-pubmed/)

Search NCBI's PubMed and Gene databases via the E-utilities API. Provides `search_pubmed`, `search_gene`, and `fetch_pubmed_data` — with batching, rate limiting, and XML parsing handled for you. The SKILL.md documents query construction patterns (MeSH vs. keyword, field tags, Boolean structure) and the common pitfalls (notably the quoted-MeSH-term trap that silently drops terms).

### [`search-openalex`](search-openalex/)

Query the OpenAlex API for citation counts, open-access status, related works, and decoded abstracts. Provides `search_works`, `decode_abstract`, and `doi_is_valid` — accepts bare DOIs, DOI URLs, and PMIDs interchangeably.

The two skills compose naturally: use `search-pubmed` to find relevant literature, then enrich with citation metrics from `search-openalex`. A worked example lives in the OpenAlex SKILL.md under "Enrich PubMed results with citation metrics."

## Using in GitHub Codespaces

Click the badge above to launch a ready-to-use cloud environment with everything pre-installed — no setup required.

What's included out of the box:
- **`llm`** — a command-line tool to chat with AI models. Comes pre-configured with access to GPT-4.1 at no cost via your GitHub account
- **Claude Code** — an AI coding assistant you can use directly in the terminal
- **Both skills** — available to `llm` and Claude Code automatically via `.claude/skills/` and `.agents/skills/`

To get started with Claude Code, run `claude` in the terminal and follow the login prompt.

## Installing a skill

To use a skill with Claude, the skill folder needs to be packaged as a zip archive (conventionally with a `.skill` extension) and loaded into your Claude runtime. Two paths, depending on whether you want a pre-built file or to build it yourself.

**Download a pre-built archive.** Once releases are published, grab the `.skill` file for the version you want from the repo's [Releases page](https://github.com/nicomarr/ai4biomed-skills/releases). This is the same content as the folder in the repo, pre-zipped and version-tagged.

**Zip the folder yourself.** If you've cloned the repo or downloaded it as a ZIP from GitHub, compress the skill folder you want and give it a `.skill` extension:

```bash
cd ai4biomed-skills
zip -r search-pubmed.skill search-pubmed -x "*/__pycache__/*" "*/.DS_Store"
zip -r search-openalex.skill search-openalex -x "*/__pycache__/*" "*/.DS_Store"
```

On macOS you can also right-click the skill folder in Finder → **Compress "search-pubmed"** → then rename the resulting `.zip` to `.skill`.

Then install the `.skill` file in your Claude runtime — see the [Agent Skills documentation](https://agentskills.io/) for the current install path in the desktop app, Claude Code, Claude Cowork, etc.

**Using the Python module directly.** If you want the utility module without the skill wrapper, copy `search-pubmed/scripts/pubmed_utils.py` or `search-openalex/scripts/openalex_utils.py` into your own project and `import` it. Each skill's `SKILL.md` is the reference for query patterns and function signatures.

Both skills require `httpx` with SOCKS support and network access to `eutils.ncbi.nlm.nih.gov` and/or `api.openalex.org` respectively — details in each SKILL.md.

## Creating and improving skills

Inside your Codespace, you can improve an existing skill, create a new one, or install additional skills from the community using the `skill-creator` tool.

Install it with:

```bash
npx skills add https://github.com/anthropics/skills --skill skill-creator
```

Once installed, just describe what you want to Claude Code — for example, "create a skill to search ClinicalTrials.gov" or "improve the search-pubmed skill" — and it will guide you through the full process, including testing and evaluation.

## Citation

If these skills contribute to published work, a citation is appreciated but not required — the MIT license does not mandate attribution.

> Marr, N. (2026). *AI for Biomedical Research — Agent Skills* [Software]. GitHub. https://github.com/nicomarr/ai4biomed-skills

Developed alongside the [*LLMs for Biomedical Research*](https://github.com/nicomarr/ai4biomed-khrc) course (KHRC).

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Nico Marr.

Each skill folder also contains a copy of the license so the `LICENSE` file travels inside the packaged `.skill` archive. The MIT license allows commercial use, modification, and redistribution with attribution; in practice this means you're free to build on these utilities in your own research or tooling, with or without affiliation to the course.