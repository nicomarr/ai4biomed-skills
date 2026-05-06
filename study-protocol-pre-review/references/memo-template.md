# Reviewer output template

> **How to use this file.** This is the structure of the Phase E output. Render it in the format the reviewer chose in Phase E (`.docx` via the `docx` skill, PDF via Pandoc, or Markdown). Length target: ~2 pages of executive content (Sections A–C) followed by a findings appendix (Section D) sized to the package — typically 5–15 pages for a full interventional trial protocol; shorter for a targeted ICF-only check or for an observational protocol.
>
> **Hard rules:**
> - The output states facts, quotes framework wording verbatim, and cites every primary source. It does **not** judge, recommend specific actions, characterise severity beyond what the framework itself classifies, or pronounce the package "ready" or "not ready". Those judgments belong to the human reviewer and the formal ethics review.
> - Every framework citation, regulatory item number, literature reference, and quantitative claim must be traceable to a verified primary source — cite the source by URL/DOI, not by reference to this skill's own files.
> - Section F ("Items requiring reviewer verification") must be present and must list every claim and citation Claude or any other language model/AI assistant made.
> - Section H (disclaimer) must be present and verbatim.
> - The output is not, and cannot be, a substitute for formal ethics-committee review.
> - Avoid the word "appraisal" in this user-facing output. Use "review", "framework check", or "pre-submission check".
> - Do not narrate the skill's phases (Phase A / Phase B / Phase C…) to the user. The phases are internal scaffolding.
> - **Whatever output format the reviewer chose, the content must be identical** if you produce more than one rendering. Do not ship a leaner .docx alongside a fuller .md.

---

## Required structure

```
[Reviewer's institution letterhead — applied by the reviewer when they
 download the file.]

PROTOCOL PRE-REVIEW
(For internal use ahead of formal ethics or regulatory submission. This
 output is generated with AI assistance and does not constitute ethical
 approval, regulatory clearance, or legal advice.)

To:        [Sponsor / PI / SRC Chair / Ethics Committee Chair, as
            appropriate to the institutional context captured in Phase A]
From:      [Reviewer name and title — captured in Phase A]
Date:      [Date]
Re:        [Protocol short title and version number]
Package:   [List of documents reviewed: protocol vN, ICF vN, IB vN, etc.]

A. Summary of what was checked
   2–5 sentences, factual only. State:
   - The study in one factual sentence (population, intervention or
     exposure, comparator if any, primary outcome, sample size, sites).
   - Which framework checks were run, with each named by its real
     citation (e.g., "SPIRIT 2025 (Chan et al., BMJ 2025)", "45 CFR
     §46.116 (Common Rule)") — not by reference to this skill's files.
   - Which checks were skipped (e.g., literature scan).
   - The total count of findings in Section D.
   Do NOT make a "ready to advance / not ready" call. Do NOT
   characterise the package as adequate, inadequate, well-designed, or
   otherwise. The reviewer makes those calls.

B. Items flagged (≤5)
   Highest framework-stated importance only — i.e., items that the
   framework itself classifies as mandatory or required (e.g., Common
   Rule basic elements; SPIRIT 2025 core items). Each item = one short
   paragraph stating:
   - The factual finding (what is or is not addressed in the package,
     with location).
   - The framework item identifier and the verbatim framework wording.
   - The primary-source citation (URL/DOI, document title, issuing
     organisation, access date).
   Do NOT add "why it matters" or "what needs to change" — those are
   judgment moves that belong to the reviewer.
   Apply the lay-language flexibility rule: a required disclosure is
   satisfied by any clear lay-language equivalent. Do not flag the
   absence of jargon as a finding (e.g., do not flag a consent form for
   not using the phrase "whole-genome sequencing" if it describes the
   procedure in lay terms).

C. Literature listing
   Recent literature in the indication, listed factually. For each paper:
   PMID, full citation (authors, title, journal, year), DOI, PubMed URL,
   and a brief factual summary drawn from the abstract. State the search
   query and date. Do NOT characterise relevance, alignment, or
   contradiction with the protocol — that is the reviewer's call.
   If literature search was not run, state that explicitly and skip.

D. Findings appendix (full table)
   One row per finding. Columns:
   | # | Document | Location | Finding | Framework item | Verbatim framework wording | Source | Framework-stated severity (if any) |
   - "Finding" must be a factual statement — not a judgment.
   - "Source" must be a primary-source URL/DOI, not a reference to a
     `references/` file in this skill.
   - "Framework-stated severity" is filled only when the framework
     itself classifies the item (e.g., "Common Rule basic element —
     mandatory"; "SPIRIT 2025 core item"; "TIDieR detail —
     recommended"). Where the framework does not classify, write
     "Framework does not classify; severity for the reviewer to assign."
   Sort by Document, then by Location. Do NOT sort by an invented
   severity ranking.

E. Frameworks applied (with full primary-source citations)
   For each framework or regulation applied, list:
   - Title and full citation.
   - Issuing organisation/committee/regulator.
   - URL or DOI of the primary source.
   - Version or access date.

   Default starter list (extend per Phase A scope):
   - SPIRIT 2025: Chan A-W, Boutron I, Hopewell S, et al. SPIRIT 2025
     statement: updated guideline for protocols of randomised trials.
     BMJ 2025;389:e081477. https://doi.org/10.1136/bmj-2024-081477.
     Issuing organisation: SPIRIT–CONSORT Group, BMJ Publishing Group.
     Applied only to interventional trial protocols.
   - STROBE 2007: von Elm E, Altman DG, Egger M, et al. The Strengthening
     the Reporting of Observational Studies in Epidemiology (STROBE)
     statement. Ann Intern Med 2007;147(8):573–577. PMID 17938396.
     https://doi.org/10.7326/0003-4819-147-8-200710160-00010. Issuing
     organisation: STROBE Initiative.
     Applied only to observational protocols, as a forward-looking guide.
   - 45 CFR §46.116: US Department of Health and Human Services, Office
     for Human Research Protections (OHRP). Federal Policy for the
     Protection of Human Subjects ("Common Rule"), 45 CFR Part 46
     Subpart A, post-2018 Revised Common Rule.
     https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-A/part-46/subpart-A/section-46.116.
   - WHO ERC ICF clinical-studies template: World Health Organization,
     Research Ethics Review Committee (ERC). Templates for informed
     consent forms.
     https://www.who.int/groups/research-ethics-review-committee/guidelines-on-submitting-research-proposals-for-ethics-review/templates-for-informed-consent-forms.
     Accessed [date].
   - WHO ERC Guide for Principal Investigators (6-page checklist).
     World Health Organization, Research Ethics Review Committee.
     URL as above. Accessed [date].
   - CIOMS 2016: Council for International Organizations of Medical
     Sciences in collaboration with WHO. International Ethical
     Guidelines for Health-Related Research Involving Humans. 4th ed.
     Geneva: CIOMS; 2016. https://doi.org/10.56759/rgxl7405. PDF:
     https://cioms.ch/wp-content/uploads/2017/01/WEB-CIOMS-EthicalGuidelines.pdf.
   - Declaration of Helsinki 2024: World Medical Association.
     Declaration of Helsinki: Ethical Principles for Medical Research
     Involving Human Participants. JAMA 2025;333:71–74.
     https://doi.org/10.1001/jama.2024.21972.
   - [Add national-framework references if the reviewer specified them
     in Phase A — e.g., national medicines regulator guidance, AVAREF
     for regional vaccine work, country-specific REC templates. Include
     the same fields: title, citation, issuing body, URL, access date.]

F. Items requiring reviewer verification (NON-NEGOTIABLE)
   This section must list every claim and citation made in the output.
   The reviewer must check each before acting on it. Group as:
   - Framework item numbers and verbatim wording cited.
   - Regulatory citations (eCFR sections, CIOMS guidelines, national
     regulations).
   - Literature citations (PMIDs, DOIs).
   - Quantitative claims (sample sizes, prevalence figures, effect
     sizes, prevalence numbers stated in the protocol or rationale).
   - Institution-specific or context-specific claims (project names,
     dates, prior approvals, prior publications, REC names, regulatory
     authority names).

G. Out of scope for this pre-review
   State explicitly what was NOT checked (e.g., statistical methods
   deep-dive, GCP training compliance, national regulatory submission
   readiness, AVAREF joint review, observational-protocol-specific
   deep-dive). The reviewer decides whether a separate pass is needed.

H. Disclaimer (always include verbatim)
   This output was generated with the assistance of Claude or another
   language model/AI assistant applying established framework checklists
   to the documents in the package. It is a fact-flagging and
   source-citing aid. It does not constitute ethical approval,
   regulatory clearance, or legal advice. The AI assistant is not a
   research-ethics-committee staff member, regulatory authority, or
   legal advisor. All judgments of severity, acceptability, readiness,
   and required action rest with the human reviewer and the formal
   research ethics committee and regulatory authority/authorities of
   record.
```

---

## Source citation format

Every framework item, regulation, guidance document, literature reference, and LMIC-norm cited in the output must have a full primary-source citation. The minimum fields are:

- **URL or DOI** of the primary source.
- **Title** of the document, page, or template.
- **Issuing organisation, committee, or regulatory body.**
- **Author(s)** where applicable.
- **Version or access date** where applicable.

**Cite primary sources by their real URL/DOI — not by reference to this skill's own files.** A citation like `references/icf-guidance.md §3.1` is wrong; the correct citation is `WHO ERC, Templates for informed consent forms (https://www.who.int/groups/research-ethics-review-committee/...), accessed [date]`.

If a fact cannot be cited with these details, do not state the fact.

## Tone and style

- Direct, professional, factual. The output is read by sponsors, PIs, and ethics-committee members — use the reviewer's specified terminology consistently throughout (REC / IRB / IEC / Ethics Committee, captured in Phase A). Do not use "appraisal".
- Use **participant-first language** per WHO ERC and CIOMS conventions ("the participant must…") rather than older US-IRB-flavoured idioms ("the human research subject must…"). If the reviewer's institution prefers a specific convention, follow that.
- Active voice. "The protocol does not specify X at p.7" — not "X has not been specified by the protocol."
- Quote framework wording verbatim with full primary-source citation when an item is referenced.
- Page-number references throughout: "ICF p.4 §Risks"; "Protocol p.21, lines 17–22".
- **Paraphrase principles in your own words** when explaining what you're doing — do not copy SKILL.md sentences verbatim into the output.

## What to *avoid*

- Don't make judgment calls. The output states facts; the reviewer judges severity, importance, and required action.
- Don't issue a "ready / not ready" verdict in any section.
- Don't characterise findings with words like "critical", "serious", "concerning", "inadequate", "the protocol should…" — those are judgments.
- Don't invent severity levels. Use only framework-stated severity (where the framework classifies); otherwise leave blank with "Framework does not classify; severity for the reviewer to assign."
- Don't recommend specific edits to ICF wording or protocol text. Quote what the framework requires; the reviewer drafts the edit.
- Don't summarise findings as "the protocol is well-designed overall but…" — that is filler and a judgment.
- Don't cite a framework item by paraphrase — quote it verbatim with full primary-source citation, or note that you could not verify it and skip.
- Don't cite this skill or its `references/` files as a source. Cite the *primary source*.
- Don't flag the absence of regulatory or technical jargon as a finding when a clear lay-language equivalent is present (e.g., the consent form describes "looking at your DNA" rather than using "whole-genome sequencing"). Lay language is what the regulations require.
- Don't omit Section F or Section H. The output without those sections is not safe to use.
- Don't narrate the skill's phases ("Phase A inventory… Phase B framework selection…") to the user. The phases are internal.
