# Changelog — khrc-doc-coauthoring

All notable changes to this skill are recorded here.
The format follows [Keep a Changelog](https://keepachangelog.com/),
and the project follows [Semantic Versioning](https://semver.org/).

## [v0.0.1] — 2026-04-26

Initial public release.

### Overview

`khrc-doc-coauthoring` is a workflow skill that guides authors through
producing funder-facing documents — grant proposals, letters of intent,
concept notes, fundraising strategies, progress reports, and policy
briefs — for the Kintampo Health Research Centre (KHRC). It extends
the generic doc-coauthoring workflow with KHRC-specific reference
grounding, mandatory funder identification for grant work, anti-
hallucination evidence rules, and a scientific rigor audit.

### Included

- A four-stage workflow (Orientation → Context Gathering →
  Refinement & Structure → Reader Testing & Rigor Review).
- A bundled `references/` library: nine pages scraped from
  [kintampo-hrc.org](https://kintampo-hrc.org) and one funder-landscape
  research report (`2026-04-23_KHRC_Funding_Organizations_Report.md`).
- Evidence-grounding rules that prefer verifiable PubMed / DOI / URL
  citations and surface `[NEEDS SOURCING]` and `[USER INPUT NEEDED]`
  placeholders for any claim that cannot be sourced.
- Recommended companion skills for citation grounding:
  [`search-pubmed`](https://github.com/nicomarr/ai4biomed-skills/tree/main/search-pubmed)
  and [`search-openalex`](https://github.com/nicomarr/ai4biomed-skills/tree/main/search-openalex).

### Provenance

The skill was developed using
[`skill-creator`](https://github.com/anthropics/skills/tree/main/skill-creator)
through several rounds of evals against representative KHRC document
prompts (concept note, fundraising strategy, policy brief). The bundled
funding-organisations report was produced with Claude's research mode
on 2026-04-23 and includes a URL accessibility appendix.

### Notes

The reference library is a *snapshot*, not a live mirror — the live
KHRC website and live funder pages are the source of truth. See the
"Provenance" subsection inside `SKILL.md` for the verification policy.