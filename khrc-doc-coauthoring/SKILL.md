---
name: khrc-doc-coauthoring
description: Guide Kintampo Health Research Centre (KHRC) staff through a rigorous workflow for co-authoring grant proposals, letters of intent, concept notes, fundraising strategy documents, funder shortlists, progress reports, policy briefs, and research summaries — with every claim grounded in the bundled KHRC reference library or web-verified at the time of writing (no invented findings, statistics, citations, DOIs, deadlines, or funder mandates). Trigger when the user mentions KHRC, Kintampo Health Research Centre, a KHRC project (EPI-MAL-003, RTS,S/AS01E, ReMIND, GasPay, CLEAR, KHDSS, TASSH, PRISMA), a KHRC research area (malaria/NTDs, Ghanaian clinical trials, household air pollution, climate and health, maternal/neonatal/child health, NCDs, operational/implementation research, health policy), or wants to draft a grant proposal, concept note, fundraising strategy, progress report, or policy brief for KHRC or sub-Saharan African health research. Use in preference to generic doc-coauthoring whenever KHRC is in scope.
---

# KHRC Doc Co-Authoring Workflow

Kintampo Health Research Centre (KHRC) is an African-based, African-led health research centre in Ghana with a portfolio spanning seven research areas, 540,000+ residents under demographic surveillance (KHDSS), 230+ completed projects, and 3,260+ publications. KHRC's funder-facing documents — proposals, concept notes, strategy memos, progress reports — must reflect that scale with precise, evidence-based scientific language, and must survive review by highly specialized panels: EDCTP3 committees, NIH study sections, Wellcome Trust panels, Gates/Grand Challenges Africa programme officers, SFA Foundation reviewers, NIHR Global Health Research boards.

This skill guides the user through four stages — **Orientation → Context Gathering → Refinement & Structure → Reader Testing & Rigor Review** — tailored to that audience. It extends the generic doc-coauthoring workflow with funder identification, evidence-grounding rules, and a scientific rigor audit that catches unsupported claims before a reviewer does.

## Before you begin: read the reference folder

The skill ships with a `references/` folder containing ten Markdown files. **Read them at the start of every engagement.** This is the single most important thing you do — it's what keeps the output grounded in what KHRC actually does rather than plausible-sounding fabrication.

Priority order:

1. **`2026-04-23_KHRC_Funding_Organizations_Report.md`** — the funding landscape (~25 funders across international, US, European, and African regional categories; 2026 calls; funder-to-research-area alignment matrix; strategic recommendations; URL accessibility appendix flagging stale links and the 2025 USAID retrenchment). Read in full for any grant or fundraising document.
2. **`01-kintampo-hrc-home.md`** — institutional identity, headline metrics, active projects, recent news. Read for any document.
3. **`02-` through `08-kintampo-hrc-*.md`** — one file per research area (clinical trials, environmental health, family health, health policy, non-communicable diseases, operational/implementation, malaria/NTDs). Read the ones relevant to the user's project.
4. **`09-kintampo-hrc-scientific-articles.md`** — publication index spanning 2016–2026. Use when citing KHRC's prior work or building a Preliminary Data section.

### Provenance: where these files came from

The reference library is a *snapshot*, not a live mirror. Treat the upstream sources as authoritative whenever there is any chance they have moved on:

- **Files `01-` through `09-kintampo-hrc-*.md`** contain content scraped from the Kintampo Health Research Centre website (kintampo-hrc.org) at the time the skill was packaged. The live website — not the Markdown — is the source of truth. KHRC updates its site (new projects, new publications, leadership changes), so for any claim that will appear in a funder-facing document, re-fetch the relevant page with `web_fetch` (or have the user check the page) before citing.
- **`2026-04-23_KHRC_Funding_Organizations_Report.md`** was generated using Claude's research mode (Opus 4.7) on 2026-04-23. URL accessibility was tested at generation time and a URL accessibility report is appended to the file. The funder websites — not the Markdown — are the source of truth: budget envelopes, deadlines, eligibility rules, and call status all change frequently and need web verification before they appear in a draft.

If a Markdown file disagrees with the live source, the live source wins.

After reading, give the user a brief orientation summary that proves you absorbed the material — e.g., "I've read the references. For a 2026 malaria proposal, KHRC's most relevant active studies are ERASE, MalVac-PMC, and EPI-MAL-003, and the best-fit funders given the post-USAID landscape are EDCTP3 (2026 TB/LRTI/climate calls, €147M envelope), Gates/Grand Challenges Africa, and NIHR Global Health Research Researcher-led. Shall we proceed?" — then move to Stage 1.

If the `references/` folder is missing or incomplete, tell the user, ask whether to continue in degraded mode or pause, and be explicit about what grounding you'll be missing.

## When to offer the workflow

Offer the full four-stage workflow when the user wants to produce a substantive document (more than ~300 words, or anything a funder or external reviewer will see). For shorter outputs (a figure caption, an internal email), work freeform.

Open with a brief explanation of the stages and ask whether the user wants to proceed structured or freeform. Use `AskUserQuestion` to make this a one-click choice (see the next section). If freeform, still respect the reference-grounding and anti-hallucination rules below — they are non-negotiable regardless of workflow mode.

## Using structured-input prompts (`AskUserQuestion`)

Many decision points in this workflow are inherently multiple-choice — document type, audience, research area, which funder to target, which section to start with, whether to advance to the next stage. When the `AskUserQuestion` tool is available, prefer it at these points over free-text questions. Structured prompts (a) reduce cognitive load on busy researchers and programme managers, (b) make the workflow feel faster and more deliberate, and (c) produce cleaner decision records that are easy to refer back to.

**Use `AskUserQuestion` at these specific points:**

1. **Workflow mode choice** (top of every engagement) — "structured four-stage workflow" vs. "freeform, I'll steer".
2. **Stage 1 Q1** — document type (11 options below).
3. **Stage 1 Q2** — primary audience (7 options below).
4. **Stage 1 Q3** — KHRC research area(s), multi-select.
5. **Funder shortlist** — after you present 5–8 verified candidate funders, use `AskUserQuestion` with the shortlist as options so the user can pick the primary target (and, for fundraising strategy docs, flag secondary/tertiary targets) in one click rather than typing names back.
6. **Section ordering at the start of Stage 2** — which section to draft first, given the section list you've agreed on.
7. **Structure approval at the start of Stage 2** — "use the default section structure for [doc type]" vs. "adjust it" vs. "start from scratch".
8. **Stage transition gates** — whenever you reach the boundary between stages (→ Stage 2 drafting, → Stage 3 testing, → Final Review), offer "proceed", "add more context / refine more first", or "pause".
9. **Skip-a-stage confirmations** — if the user signals they want to bypass info-dumping, section-by-section discipline, or Reader Testing, present the skip as a structured choice with the trade-off spelled out in the option label (e.g., "Skip funder identification — I'll lose call-specific tailoring").
10. **Exit points** — "document is done", "one more review pass", or "fix specific issues first".

**Do not use `AskUserQuestion` for these:**

- The info-dump in Stage 1 (free-text is the point).
- The 5–10 clarifying questions at the end of Stage 1 context gathering (numbered list with shorthand replies is fine).
- Brainstorm curation in Stage 2 Step 3 (keep/remove/combine is too nuanced for canned options — let the user reply in shorthand like "keep 1, 4, 7; drop 3; combine 2+5").
- The refinement feedback loop in Stage 2 Step 6 (the user's edits are inherently free-form prose).
- Any question that is genuinely open-ended (why, how, what else).

If `AskUserQuestion` isn't available in the session, fall back to numbered options the user can reference by number.

## Stage 1: Context Gathering

**Goal:** close the gap between what the user knows and what you know, and commit to a specific document type, audience, and (for grant work) target funder.

### Always ask before drafting (even when the user gave a detailed brief)

Even when the user supplies what looks like a complete spec — document type, length, funder, deadline — **do not skip the clarifying loop**. KHRC researchers often hand off a one-line ask that hides important context (which co-investigators are involved, which preliminary findings to lead with, which prior submission to mirror or distance the new draft from). Producing a polished first draft against an under-specified brief usually wastes more of the user's time than asking 2–3 questions up front.

The minimum bar before you generate any draft text:

1. Run **Q1, Q2, and Q3 below** (document type, audience, research area) — even if the user already mentioned them, confirm them via `AskUserQuestion` or restate them and ask "is this right?"
2. Ask **at least one targeted question** that draws on KHRC-specific context the model can't know — e.g., "Which co-investigators should be named on this LOI? Anyone we should *not* include?", "Which of your prior TASSH outputs should this brief lead with?", "Is the SFA Foundation programme officer at KHRC currently the same as in the funder report (Dr X), or has that changed?"
3. If the user explicitly says *"just draft it, I'll edit"*, honour that — but at the top of the draft include a short `## Open questions for the user` block listing the 2–3 questions you would otherwise have asked, so the user can answer them inline during review.

### Initial questions

Ask these early. When the `AskUserQuestion` tool is available, use it for Q1 and Q2 so the user can pick from options quickly; use free-text for the rest.

**Q1. What type of document are we producing?**

- Grant proposal narrative (full application)
- Letter of intent / concept note / expression of interest
- Research summary or project brief (short, stakeholder-facing)
- Fundraising strategy document ("top funders to approach for project X")
- Funder-matching / opportunity shortlist (the deliverable itself is the shortlist)
- Progress / interim report to a current funder
- Final / end-of-grant report
- Scientific manuscript, abstract, or conference poster
- Policy brief or briefing note for Ghana Health Service / Ministry of Health
- Press release, blog post, or newsletter article (e.g., *KHRC Focus*)
- Annual report section or institutional profile
- Other (user specifies)

**Q2. Who is the primary audience?**

- A specific named funder (ask which — e.g., EDCTP3, NIH Fogarty, Wellcome, Gates/Grand Challenges Africa, NIHR, SFA Foundation, IDRC, WHO/TDR, CIFF, Africa CDC)
- A generic funder (no specific call yet — funder identification happens below)
- Academic peers / research collaborators (conference, journal, consortium)
- Ghana Health Service, Ministry of Health, or Parliament
- Internal KHRC leadership / Board of Trustees
- Community, media, or general public
- Other (user specifies)

**Q3. Which KHRC research area(s) does this cover?** (multi-select is fine)

Clinical trials & intervention · Environmental health · Family health / MNCH · Health policy & programme evaluation · Non-communicable diseases · Operational & implementation research · Malaria & neglected tropical diseases · Cross-cutting

**Q4. Is there a specific project, study, or finding this document centres on?**
(e.g., "ReMIND — maternal anaemia and infant brain development", "EPI-MAL-003 one-year safety data", "GasPay LPG adoption at scale", "TASSH task-shifting for hypertension"). If yes, note the name — you will ground claims in the relevant reference file and, where needed, web-verify published outputs.

**Q5. Deadline, word/page limit, and any template the funder provides?**

**Q6. What is the desired impact when someone reads this?**
(e.g., "get invited to submit a full proposal", "secure renewal funding through 2029", "shift Ghana's malaria vaccine roll-out policy", "convince a new philanthropist to partner with KHRC")

### Funder identification (mandatory for grant-related documents)

If Q1 is a grant proposal, letter of intent, concept note, fundraising strategy, or funder-matching document, **and** Q2 did not lock a specific funder, identify candidate funders before drafting anything. This is the step that most distinguishes useful KHRC documents from generic ones.

Process:

1. From the **Funding Organizations Report**, shortlist 5–8 funders whose mandate, geography, and funding envelope align with the research area(s) in Q3 and the work type (clinical trial, implementation research, capacity building, environmental health, etc.). The report's alignment matrix at the end is the starting point.
2. For each shortlisted funder, use `web_search` and/or `web_fetch` (e.g. `mcp__workspace__web_fetch` in Cowork) to verify:
   - The funder is still active and their Africa/LMIC mandate is intact (the post-January-2025 USAID retrenchment cancelled ~90% of USAID global projects — several previously-major pipelines are paused or restructured).
   - The specific call or mechanism cited in the reference is currently open or has an announced 2026/2027 cycle.
   - Current budget caps, eligibility changes, and deadlines (these shift frequently; references dated 2026-04-23 should not be trusted for these details without re-verification).
3. Present the verified shortlist to the user with a one-line rationale per funder, the live URL, the current call status, and the approximate budget/duration. Let the user pick the primary target (and, for fundraising strategy documents, secondary and tertiary).
4. For the chosen primary funder, fetch the current call text and distil it: scope, eligibility, budget cap, deadline, required document format, mandatory partnerships, submission portal. This distillation becomes the structural spine for Stage 2.

For a funder-matching or fundraising strategy document, this step **is** the deliverable — Stage 2 will then produce the strategy write-up rather than a full proposal.

### Info dumping

Once Q1–Q6 are answered (and, where relevant, the funder is locked), invite the user to dump everything else they have: project concept notes, prior proposals (successful or not), draft aims, PI and co-I CVs, preliminary data tables, collaborator letters, community engagement notes, ethical approval correspondence, Slack threads, meeting minutes. Ask them not to worry about organisation.

When the dump slows, ask 5–10 numbered clarifying questions to fill gaps. Let the user answer in shorthand.

**Exit condition:** edge cases and trade-offs can be discussed without needing basics re-explained. Target funder is locked (if grant work). The scientific question, methods, and specific KHRC role are clear. Proceed to Stage 2.

## Stage 2: Refinement & Structure

**Goal:** build the document section by section, with every substantive claim grounded in a reference file or a web-verified source.

### Tone and language guidelines

KHRC documents should read as the output of a seasoned, African-led research institution — not as generic grant boilerplate, and not as academic prose that buries the lede. Hold to these standards for every paragraph:

- **Precise, evidence-based language.** Cite specific findings, study names, sample sizes, effect sizes, and publication years rather than vague gestures. Replace *"KHRC has extensive experience with malaria vaccines"* with *"KHRC led the Ghanaian arm of the EPI-MAL-003 Phase 4 cohort-event monitoring study, contributing safety and effectiveness data on the RTS,S/AS01E vaccine across Ghana, Kenya, and Malawi; the 2025 interim analysis reported effectiveness over one year of follow-up after the three-dose primary schedule"* (ref: `09-kintampo-hrc-scientific-articles.md`).
- **Quantitative specificity.** Use actual numbers from the references — 540,000+ KHDSS residents, 230+ completed projects, 3,260+ publications, 13,000+ people screened and 300 community health workers trained through TASSH, 3,950+ households reached by GasPay — rather than adjectives like "extensive", "substantial", or "considerable". If a number is not in the references and cannot be web-verified, do not invent one; either describe the work qualitatively or leave a `[NEEDS SOURCING]` placeholder.
- **African-led framing.** KHRC's tagline is "African solutions to African health challenges". Avoid phrasing that casts African institutions as passive recipients of Northern science or funding. Lead with KHRC's scientific leadership, its community partnerships in the Bono East region, and its capacity-building role (NEST programme, CLEAN-Air(Africa) partnership, DELTAS Africa II consortia).
- **Funder-native vocabulary, when it fits.** Mirror the target funder's language where it's accurate, not performative. EDCTP3: "sub-Saharan African partnerships", "capacity strengthening", "Global Health EDCTP3 2026 work programme". NIH Fogarty: "LMIC-based", "Emerging Global Leader Award (K43)", "research capacity building". Wellcome: "discovery research", "ODA-eligible countries", "climate and health". Gates / Grand Challenges Africa: "African innovators", "Grand Challenges", "equitable global health". Use these phrases when they're accurate to the call; don't force them.
- **No slop.** Every sentence should carry weight. If a sentence could be deleted without the paragraph changing meaning, delete it. Generic aspirational language ("transformative impact", "paradigm-shifting") is a red flag unless you can immediately back it up with an outcome.

### Evidence-grounding rules (anti-hallucination — non-negotiable)

These are the single most important rules in this skill. A KHRC document that invents a statistic or a citation does more harm than a document that never gets written.

1. **Only reference findings, methods, statistics, study names, funder mandates, budget figures, deadlines, eligibility criteria, publication details, or conclusions that are (a) described in the `references/` folder, or (b) retrievable via `web_search` / `web_fetch` at the time of writing.** Do not invent study results, sample sizes, p-values, author lists, publication years, DOIs, trial registration numbers, funder budget caps, deadlines, or eligibility rules.
2. **Verify before citing — references can be stale.** Funder calls close, budget envelopes change, projects end, URLs move. For any claim that will influence a reviewer's decision (current deadlines, current budget caps, current eligibility, current trial status, current DOIs), web-verify *before* putting it in the draft. The Funding Organizations Report contains a URL accessibility appendix — it already flags several broken or changed links; treat all of them as requiring re-verification.
3. **When sourcing is uncertain, flag — don't fabricate.** If you can't ground a claim, either drop it or draft it with a `[NEEDS SOURCING: <specific claim>]` placeholder and surface it to the user for verification. Never guess a number to fill a gap.
4. **When KHRC-specific context is needed (and only the user knows it), use a `[USER INPUT NEEDED: …]` placeholder.** The reference library covers public KHRC outputs; it does not know which co-investigator should sign a letter, which internal preliminary data is shareable, what the Director of the NCD Control Programme said in last week's meeting, or which related Ghana Health Service policy documents should be cited. For each such gap, write a placeholder like `[USER INPUT NEEDED: name and affiliation of the lead co-investigator from KCCR Kumasi]` or `[USER INPUT NEEDED: most recent Ghana NCD Strategy document this brief should reference]`. Surface a list of these placeholders at the top of the draft.
5. **Cite inline while drafting, with verifiable links wherever possible.** Every substantive claim gets a short source tag in the working draft. Three forms, in order of preference:
   - `(web: <publication title>, PMID 12345678)` or `(web: DOI 10.xxxx/yyyy)` for scholarly outputs — preferred whenever the cited work is in PubMed or has a DOI. The companion *skills* `search-pubmed` (wraps the NCBI E-utilities API) and `search-openalex` (wraps the OpenAlex API) are the right way to confirm titles, authors, PMIDs, DOIs, and citation counts before citing — invoke them via the host's skill-invocation mechanism (the `Skill` tool in Cowork / Claude Code) rather than by calling any underlying tool directly. If neither skill is available in the session, fall back to `web_search` / `web_fetch`.
   - `(web: <funder programme name>, <https://…>, verified YYYY-MM-DD)` for funder calls, KHRC website pages, or news items — always include the live URL.
   - `(ref: <filename>.md)` or `(ref: <filename>.md → <section>)` as the *fallback* when no web-verifiable source exists — for example, internal-only context from a reference summary. A document that cites only `ref:` markers is harder for a funder reviewer to verify than one that cites PubMed/DOI/URLs, so prefer the `web:` forms wherever the underlying source is publicly accessible.

   These tags stay in the working draft so the user and the Reader Claude pass in Stage 3 (a fresh, context-free reader — sub-agent or fresh Claude.ai chat; defined at the top of Stage 3) can audit the evidence chain; they get converted to the funder's required citation format only in the final pass.
6. **Always end with a verifiable References section.** Every grant, concept note, fundraising strategy, and policy brief should close with a `## References` block that lists each cited source as a clickable URL, DOI, or PMID — never as a bare `(ref: 08-…)` marker alone. This is what lets the user (and the eventual funder reviewer) confirm the document in five minutes rather than five hours.

### Default length when the user didn't specify

If the user supplied a length, follow it. Otherwise default a *first* draft to the lower end of what the document type can carry, and offer to expand:

- Letter of intent / concept note: 1 page.
- Fundraising strategy: 1 page (single-pager that the user can share with leadership). Offer to expand to a longer pipeline document if the user wants it.
- Policy brief: 1 page.
- Progress / interim report, research summary: 1–2 pages.
- Grant proposal narrative: scope to the funder's word/page limit; if no limit, 6–10 pages.

A leaner first draft is easier to react to than a long one. Once the user has reviewed, ask whether to expand specific sections rather than expanding everything.

### Section structure by document type

If the funder provides a template, use it exactly — funder templates are non-negotiable. Otherwise, use these defaults and confirm with the user before drafting. The bracketed `[…]` items mark sections that almost always require user input KHRC-specific knowledge — leave them as `[USER INPUT NEEDED: …]` placeholders if not supplied.

- **Grant proposal narrative:** Specific Aims → Background & Significance → Preliminary Data → Research Design & Methods → KHRC Capacity & Research Environment → Team, Collaborations & Community Engagement → Timeline & Milestones → Risk Analysis & Mitigation → Budget Justification → References.
- **Letter of intent / concept note:** Project title → Problem statement → Proposed approach (aims in one paragraph) → Expected impact and alignment with funder priorities → KHRC & partner capacity → Budget envelope → Next steps → References (with PubMed / DOI / URL links to KHRC's prior work on the topic).
- **Fundraising strategy document:** Executive summary → KHRC research priorities (mapped to the seven research areas) → Funder landscape (top 5–8 funders with verified 2026 status, rationale, and budget) → Proposal pipeline → Submission calendar → Risk factors (e.g., USAID retrenchment, shifting European ODA commitments) → **Action items & key decisions** (a short, sequenced list of what leadership needs to decide and who owns each — this is what makes the doc useful in a meeting) → References / live funder URLs.
- **Funder-matching shortlist:** For each shortlisted funder: name, mechanism, URL, verified call status, budget envelope, deadline, eligibility, fit rationale, KHRC PI candidate, required partnerships.
- **Progress / interim report:** Original aims → Progress against each aim → Milestones achieved vs. planned → Publications and other outputs → Budget status → Variances and deviations (with explanations) → Forward plan → Requests to funder.
- **Policy brief:** Issue in two sentences → Evidence base (cite KHRC studies via PubMed / DOI / URL) → **Related policies and current Ghana context** (recent Ghana MoH / GHS strategies, the relevant section of the Ghana NCD Strategy, any active CHPS programme directives — usually a `[USER INPUT NEEDED: most relevant current Ghana MoH/GHS document and date]` placeholder, since the model cannot know which internal policy document the brief should align to) → Policy options (usually 2–3) → Recommended option → Implementation considerations → Key references.
- **Scientific manuscript / abstract:** Follow target journal or conference format exactly.

### Section-by-section workflow

For each section, follow the base loop:

1. **Clarifying questions** — ask 5–10 specific questions about what the section should cover.
2. **Brainstorming** — generate 5–20 numbered options (more for complex sections like Aims or Methods, fewer for short sections like Budget Justification).
3. **Curation** — ask the user which to keep/remove/combine. Accept shorthand ("keep 1, 3, 7; drop 4 (already covered); combine 2+5").
4. **Gap check** — ask if anything important is missing.
5. **Draft** — use `Write` (for new sections) or `Edit` / `str_replace` (for revisions). While drafting, apply the evidence-grounding rules above — every substantive claim gets a source tag or a `[NEEDS SOURCING]` flag.
6. **Iterative refinement** — the user indicates changes; you apply them with Edit. After 3 consecutive iterations with no substantial changes, ask whether anything can be cut without losing information.

Never rewrite whole sections when a surgical edit will do — it wastes tokens and loses earlier refinements.

### Near-completion pass

When 80%+ of sections are drafted, re-read the full document and check:

- Flow and consistency across sections
- Numerical contradictions (e.g., sample size stated differently in Methods vs. Preliminary Data)
- Any open `[NEEDS SOURCING]` flags
- Alignment with the target funder's scope, priorities, and format
- Word/page limit compliance
- Any generic or promotional language that slipped in

Surface issues to the user before moving to Stage 3.

## Stage 3: Reader Testing & Scientific Rigor Review

**Goal:** stress-test the document with a fresh-eyes reviewer pass and audit its scientific and funder-fit integrity.

> **What "Reader Claude" means here.** "Reader Claude" is shorthand for a Claude instance reading the document with **no conversation context** — only the document itself plus a question. The point is to simulate how an actual funder reviewer or Ministry of Health reader will encounter the doc: with none of the context built up in this chat. How you run it depends on the client:
> - **Agentic clients with sub-agents** (Claude Code, Cowork, the Claude Agent SDK): spawn a sub-agent via the `Agent` tool with only the document and the question.
> - **Chat-only clients without sub-agents** (e.g., plain Claude.ai): ask the user to open a fresh Claude.ai conversation, paste the document, and ask the reviewer-style questions there. Have them paste the answers back so you can analyse them together.
>
> Either way, missed answers point to gaps in the document, not to limits of the reader.

### Step 1: Predict reviewer questions

Generate 5–10 questions a reviewer at the target funder would realistically ask when reading the document cold. Examples, tailored by funder:

- EDCTP3: "How does this strengthen sub-Saharan African research capacity? Who is the African lead PI?"
- NIH Fogarty: "What specific capacity gap does this close, and what is the mentorship plan for the LMIC scholar?"
- Wellcome: "What makes this discovery research rather than implementation? Where is the novelty?"
- Gates / Grand Challenges Africa: "What's the path to scale? How is this different from existing interventions?"
- NIHR GHR: "How is this equitably partnered, and how will findings inform UK and LMIC policy?"
- Generic: "Why KHRC? Why now? What's novel? What's the risk and mitigation?"

### Step 2: Run the Reader Claude pass

Run the reader pass for each predicted question, using whichever path fits the client (see the note at the top of this stage). In an agentic client, spawn a sub-agent via the `Agent` tool with **only** the document and the question. In a chat-only client, walk the user through running the question in a fresh Claude.ai conversation. Either way, summarise for the user what Reader Claude got right, what it misinterpreted, and what it couldn't answer.

### Step 3: Scientific rigor audit (KHRC-specific addition)

In addition to the standard Reader Claude checks, run a separate rigor-audit pass (sub-agent or fresh chat, same dual-path pattern). Give it the document and ask it to report:

1. **Unsupported claims.** Every statement that reads as a factual claim (a number, a finding, a funder mandate, a trial result, an eligibility rule, a deadline) without a source tag or citation. List each verbatim.
2. **Tone lapses.** Sentences that read as vague, promotional, or generic rather than precise and evidence-based ("transformative", "cutting-edge", "leading"). Flag with a tighter rewording.
3. **Funder-fit mismatches.** Anything in the document that doesn't match the target funder's priorities, eligibility, required format, word limit, or mandatory partnership structure. Flag with the specific funder requirement being missed.
4. **Internal contradictions.** Numbers that differ across sections, aims that don't match methods, budget items not reflected in the narrative, timelines that don't add up.

### Step 4: Ambiguity and assumptions check

Run the standard sub-agent pass for ambiguity, implicit assumptions, and contradictions from the base doc-coauthoring workflow.

### Step 5: Report and fix

Report all issues found. For each, propose a fix. Loop back to Stage 2 for any section with open issues. Do not advance while any `[NEEDS SOURCING]` flag is still open.

**Exit condition:** Reader Claude answers the reviewer-style questions correctly, the rigor audit reports zero unsupported claims and zero funder-fit mismatches, the ambiguity pass is clean, and the user is satisfied.

## Final review

Before declaring the document done:

1. Remind the user they own this document — ask them to do a final read-through themselves.
2. Encourage them to verify every URL, DOI, trial registration number, and funder-specific figure one more time, especially anything near the submission deadline.
3. Confirm the document achieves the impact stated in Q6 of Stage 1.
4. For grant submissions: confirm the funder's submission-portal requirements (file format, cover letter, mandatory annexes, required attachments like CVs in NIH biosketch format or EU participant portal PIC codes) with the user — references can't be authoritative about portal mechanics.
5. Offer to save the final document to the user's workspace folder via computer:// link and present it with the `mcp__cowork__present_files` tool so they can open it directly.

## Tips for effective guidance

- **Be direct and procedural.** KHRC researchers are busy scientists and programme managers; don't oversell the process, just run it.
- **Explain the "why" when it shapes behaviour.** If you're pushing back on a claim for lack of a source, say so — don't just ask for a rewrite. If a sentence is too promotional, explain which funder convention it violates.
- **Respect the user's agency.** If they want to skip a stage, let them, but flag the specific risk ("skipping funder identification means I can't tailor the narrative to a specific call — fine to proceed?").
- **Never let unsupported claims into the final draft.** This is the single biggest quality risk and the easiest thing for a reviewer to catch.
- **Offer to update the references.** The Funding Organizations Report is dated 2026-04-23 and will age. If the user learns of a new call, a closed mechanism, or a new partner organisation, offer to note it and, with permission, append a supplement file to `references/`.

## How this skill differs from generic doc-coauthoring

1. It grounds every engagement in a bundled KHRC reference library before drafting.
2. It treats funder identification as a mandatory early step for grant-related work.
3. It enforces evidence-grounding rules that prohibit invented findings, citations, numbers, or deadlines — and requires inline source tags during drafting.
4. It adds a scientific rigor audit to Reader Testing that catches unsupported claims, tone lapses, funder-fit mismatches, and numerical contradictions.
5. It writes in KHRC's institutional voice: African-led, evidence-dense, quantitatively specific, funder-native but never generic.
