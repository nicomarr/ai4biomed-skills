# Assets

This folder contains files the skill may hand to users via `present_files` — not files the skill reads into context. The verbatim section structure of each ICF template variant is summarised in `references/icf-guidance.md` §3.1 and §3.1A; the Word files here are for handoff so a reviewer can give a PI a clean starting point.

## `who-erc-icf-templates/`

Five WHO Research Ethics Review Committee (WHO ERC) Informed Consent Form template variants, downloaded from the WHO ERC templates page on 30 April 2026.

| File | Use | Skill section that references it |
|---|---|---|
| `ethics-informedconsent-clinicalstudies.doc` | Adult ICF for clinical trials and clinical research | `references/icf-guidance.md` §3.1 |
| `informed-assent-for-children-minors.doc` | Paediatric assent (template targets ages 12–16; adapt language for younger children) | §3.1A.1 |
| `consent-for-storage-and-future-use-of-unused-samples.doc` | Layered additional consent for storage/future use of biological samples | §3.1A.2 |
| `informed-consent-for-qualitative-studies.doc` | Adult ICF for questionnaires, interviews, and focus groups | §3.1A.3 |
| `informed-parental-consent-for-research-involving-children-(qualitative).doc` | Parental consent for qualitative research involving children | §3.1A.4 |

Source for all five: World Health Organization, Research Ethics Review Committee. *Templates for informed consent forms.* `https://www.who.int/groups/research-ethics-review-committee/guidelines-on-submitting-research-proposals-for-ethics-review/templates-for-informed-consent-forms`. Open access.

A sixth variant — *parental consent for clinical research with children* — exists on the WHO ERC page but is **not bundled** in v1. The reviewer should download it directly from the WHO ERC page when needed; it will be added in v1.5.

## When the skill should hand these to the user

When a finding indicates that a particular ICF variant should exist in the package but does not, surface the corresponding template via `present_files` so the reviewer can pass it on to the PI. Examples:

- Package contains paediatric clinical research but no assent form → offer `informed-assent-for-children-minors.doc`.
- Protocol mentions storage or future use of biological samples but no separate sample-storage consent → offer `consent-for-storage-and-future-use-of-unused-samples.doc`.
- Package contains qualitative research with children but no parental consent → offer `informed-parental-consent-for-research-involving-children-(qualitative).doc`.

Do not hand out templates speculatively; only when a finding identifies a missing ICF variant.
