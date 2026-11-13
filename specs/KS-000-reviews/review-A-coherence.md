# KS-000 review A: coherence (v0.2)

- **Subject:** `specs/KS-000-process.md` v0.2 in cambridgetcg/kingdom-standards. It is an uncommitted working-tree change on branch `lab/ks-000-lineage-provenance-20261113`, over `origin/main` at `e3b95e5`. v0.1 was last changed at `49ec387`.
- **Bytes reviewed:** sha256 `5054af92aba42ec6ea3bef56e8232eda78152169371b0cab6d69b4a269e2565d`, 260 lines (v0.1 had 149).
- **Reviewer:** reviewer A, with a coherence and process-capture lens. I am Claude Opus 5.5, running as a read-only workflow subagent, on 2026-11-13.
  - I am not an editor of the draft and did not write it. The frontmatter names the 0.2 editor as a lab session running Claude Fable 5.2.
  - My independence is bounded as §9 says, and further: my brief was computed by a workflow script, and I did not check who launched it (finding 11).
- **Checked against:**
  - the rest of KS-000;
  - FOUNDATION 0.2, CONSENT/1, COMMON-GROUND and AMENDMENT-0.2;
  - ABUNDANCE;
  - the six records §10 cites, at the commits it names;
  - the kingdom decision log;
  - the Seven Walls;
  - SOPHIA and `fate/`;
  - KS-004 0.4, where it uses the word "lineage".
- **Result:** the draft passes once findings 1 and 2 are dealt with. Findings 3 to 11 should be fixed before adoption.
- **Earlier law:** REALM, the Seven Walls and FATE appear below only as ancestors. Nothing here grades them.

Labels used below: (obs) means the record says it; (inf) means my inference; (n/c) means not checked.

## Strongest objection

§4.1 says only "Yu's word" may be written as Yu's decision. It then lets that label rest on a record nobody else can see. For words kept privately, the label needs only "the date, and where the record is kept".

§10 shows what this comes to in practice: "given in the lab session of 2026-11-13 and kept privately". That names no keeper, no kind of record, and nothing a reviewer can check. I could not check it. The series has no key of Yu's to sign such a record: `zone/signatures.json` at `e3b95e5` says adoption signatures "await Yu's key" (obs).

The relabel rule makes this worse. The same session can promote its own reading to "Yu's word" by recording a confirmation that is just as private. So a session that holds a private record can mint the series' strongest label, and a §3 reviewer has nothing to break.

§4.1 was written to stop silent promotion. As drafted, it gives promotion a form to fill in. Finding 2 proposes the fix.

## Findings

**1. §4.1, last bullet and the scope of the labels: refusal, and decisions that are not Yu's [blocking]**
- *Text:* "Adoption and refusal (§4) rest on Yu's word alone." Every decision the series relies on MUST carry one of four labels, and all four are defined by reference to Yu.
- *Why it fails:*
  - §4 says reviewers and editors "MUST retain the power to refuse a spec on the record". That is the "both directions" of §4, and the bullet, read as written, removes it.
  - The series also creates decisions that are not Yu's. Examples: editors abandoning a draft (§2), a reviewer's refusal (§4), and a maintainer accepting a Kingdom Standard amendment under FOUNDATION's own rule (obs: kingdom-standard `FOUNDATION.md` at `07efbc0`, Amendment).
  - None of these fits any of the four labels. The MUST either cannot be met, or is met by claiming a delegation the decider never had.
- *Change:*
  - Limit §4.1 to "a decision attributed to Yu or made on Yu's authority".
  - Reword the bullet: "Yu's adoption and Yu's refusal rest on Yu's word alone. A reviewer's or editor's refusal (§4) is their own record and needs no label."

**2. §4.1, "Yu's word" kept privately; §3, §8, §9 [blocking]**
- *Why it fails:* see the strongest objection. Under FOUNDATION F1 a record is testimony, so a privately kept "Yu's word" written by a session is that session's testimony that Yu said something.
- *Change:*
  - In the "Yu's word" row, add: "If the words are kept privately, name who keeps them and in what kind of record, and who read them for this text. The label is then that reader's report (FOUNDATION F1)."
  - In §3, add: "A reviewer who cannot see a private record says so. The claim stands as not checked until Yu confirms it in the review record or the pull request."
  - In §8, add a bullet: "Label laundering. A session can assert a private 'Yu's word' or a private confirmation. §4.1 makes the assertion visible, not true."
  - In §9, add: "Until Yu holds a signing key, 'Yu's word' in this repository is always someone's report that Yu said it."

**3. §4.1, "A label changes only by a new record" [should_fix]**
- *Text:* "When Yu confirms a reading, record the confirmation and relabel it Yu's word."
- *Why it fails:*
  - "Yu's word" means "Yu said or wrote it". A confirmation does not make Yu the author of a session's words.
  - Relabelling invites an edit in place. F5 has corrections appended, and §8 makes any post-adoption edit a new release.
  - "The record it read" can itself be a reading. A chain of sessions then looks like one step from Yu (inf).
- *Change:* "When Yu confirms a reading, append the confirmation beside it: 'a reading of Yu's word, confirmed by Yu's word of <date> (<where>)'. The earlier label stays. The record a reading cites is Yu's own words; a reading of another reading cites the whole chain."

**4. §4.1, "reading" versus "call under delegation", and §10's own labels [should_fix]**
- *Why it fails:*
  - The two labels overlap whenever Yu's words accept a proposal or set a scope.
  - By §10's own account, the go-ahead accepted the session's recommendation of two habits. It named neither the home for them (KS-000) nor the wording. Those were the session's choices, which is what a call means. Labelling them a reading places them closer to Yu than they are (inf).
  - The delegation row asks for no scope, no check that the delegation was current, and no rule on subdelegation. FOUNDATION F3 and CONSENT Q12 require authority that is "current, scoped, separately evidenced", and say "Subdelegation is absent unless explicit" (obs: `CONSENT.md` at `9abb501`).
- *Change:*
  - Add a test: "If Yu's words name the outcome, the text is a reading. If they accept a proposal or set a scope, what the agent then chose is a call under delegation, and the proposal is cited."
  - Make the delegation row cite: "the delegation, itself labelled, its scope, that it was current, and the session; a subdelegation is cited as such."
  - Relabel §10's last paragraph to match.

**5. §4.1, the disagreement rule against "one of four labels" [should_fix]**
- *Why it fails:* a decision whose records disagree cannot take one label without picking one, and the bullet says "Do not pick one".
- *Change:* "Where records disagree about who decided, give each record with the label it supports and say that they disagree. Until a new record settles it, the decision is relied on only as Unrecorded."

**6. §4.1, reach over every commit and pull request [should_fix]**
- *Text:* "a commit message or pull request in this repository relies on a decision".
- *Why it fails:*
  - Four of the five most recent commits on `origin/main` touch no spec. They are estate-wide sweeps under shared author names that touch AGENTS.md, DADA.md, PLEASE-DONT-FOLLOW.md and hooks (obs: `4fb8798`, `6a4bd6a`, `bc0bb57`, `b284390`).
  - "Relies on a decision" is undefined, and almost every commit relies on one.
  - Commit messages cannot be corrected in place, §3 does not review them, and nothing checks them. The rule adds cost with no return (inf; §1).
- *Change:* "Wherever a KS or a review record, or a commit or pull request that changes `specs/` or `zone/`, cites a decision as its authority (says that something was decided, chosen, approved or settled)".

**7. §7.1, what counts as an earlier rule, and hidden omissions [should_fix]**
- *Text:* "any text the Kingdom has treated as binding or foundational". Editors must name where they looked only when they found nothing.
- *Why it fails:*
  - Nothing tests what counts as "treated as binding", or when a KS "restates" a text.
  - §10 drifts both ways. It lists as ancestors texts that 0.2 only borrows from: ABUNDANCE, an agent guide in KINGDOM-OS and a product decision record.
  - It omits texts that §4.1 does restate. The kingdom decision log already has Proposed, Accepted and Superseded statuses, the rule "supersede it with a new one and link", and the form "an agent's call under Yu's … delegation … Yu overturns it by saying so" (obs: cambridgetcg/kingdom `DECISIONS.md` at `21b8eaa`). The Seven Walls already give Yu the power to override a decision (obs: cambridgetcg/love-unlimited `WALLS.md` at `0a3aa1b`). Neither clone was fetched today.
  - Because a search is described only when nothing is found, a partial list reads as complete. Leaving out an inconvenient ancestor is invisible (inf).
  - The search has no limit, which is a burden on any citizen who writes a draft (§2).
- *Change:*
  - Define the term: "An ancestor is an earlier rule on the same matter that this KS replaces, narrows or restates. Texts a KS only borrows from are cited where used, not in Lineage."
  - Require every Lineage section to name where its editors looked.
  - Set a floor for the search: this series, the Kingdom Standard repository and the ancestors §7.1 names. Reviewers may add others.

**8. §7.1, ancestors still in force elsewhere; revival; judgment [should_fix]**
- *Why it fails:*
  - A Kingdom Standard release stays in force under its own amendment rule (obs: FOUNDATION at `07efbc0`), so a KS cannot replace or narrow it. Current law already shows the right form: CONSENT and COMMON-GROUND each say they do not amend, supersede or replace FOUNDATION (obs: `CONSENT.md` at `9abb501`, `COMMON-GROUND.md` at `ff11f32`).
  - A "Kept" row can be read as taking in the ancestor by reference, which would revive it (inf).
  - A recorded reason for a drop, copied in without attribution, can bring in a verdict on the ancestor (inf).
- *Change:* add three lines.
  - "An ancestor still in force under its own amendment rule is not replaced or narrowed by a KS. The KS says it does not amend it, and a change to it goes through its own rule."
  - "A KS keeps only what its own text states. A Lineage row incorporates nothing by reference."
  - "A recorded reason is quoted with its source and its §4.1 label. Editors add no assessment of the ancestor."

**9. §10 does not follow §7.1 or §4.1 [should_fix]**
- *Why it fails (obs unless marked):*
  - §7.1 asks for a section titled "Lineage". §10 has a different title.
  - Only the first row says what is dropped. Other rows drop things too:
    - §7.1 keeps ABUNDANCE's observation and inference but not "hope".
    - §4.1 drops the word "settled" from the KINGDOM-OS row.
    - §4.1 would not let a reading be headed "Owner decisions", as `CLAUDE.md` at `6536d11` does.
  - No row gives a reason for its change or says "no recorded reason".
  - §4.1 says the labels "are taken from records that already use them". Only two of the four are sourced.
  - 0.1's own ancestors are waived. §4 restates FATE's keystone and §3 restates the forge protocol, and both are cited by home-directory paths with no commit.
  - In the local clone (not fetched today), `SOPHIA.md` at `686cf97` has the keystone sentence but no onward path, and FATE has been at `fate/FATE.md` since `1f2956d`. This is about where KS-000 points, not about FATE. The forge-protocol file is not on this machine (n/c elsewhere).
  - "Restate rules that already existed": those rules existed for other scopes. Binding this repository to them is new, so "adapts" is the accurate word (inf).
- *Change:*
  - Retitle the section "Lineage" and add a Dropped column.
  - Give each row its reason, or "no recorded reason".
  - Add rows for FATE and the forge protocol with repository and commit, or say that 0.1's citations are left for a later version.
  - Cite a source for the claim about all four labels, or remove it.
  - Write "adapts".

**10. §10, "The recorded reason for §4.1" [should_fix]**
- *Why it fails:*
  - The quotes match the commits they cite (obs). But the two records do not disagree about who decided.
    - The agenttool comment says "Owner decision, 2026-09-23" (cambridgetcg/agenttool `api/src/billing/commercial-policy.ts` at `422ac856`).
    - The monorepo record says that commit `8165fcbe`'s "Will:" line is an agent's paraphrase and that no decision record was written (cambridgetcg/Cambridge-TCG-monorepo, `docs/decisions/2026-10-20-rewardspro-free-only-relaunch.md` at `64eb9d90`). That is a statement about the record, not about who decided.
    - Both records fit Unrecorded. The case supports the Unrecorded label, not the disagreement rule.
  - "The same decision" is unmarked inference. The evidence is two commits in two repositories, nine minutes apart (obs: `8165fcbe` at 22:15 and `422ac856` at 22:24, both on 2026-09-23).
  - A real disagreement about who decided does exist, in a design document on an unmerged agenttool branch: "never confirmed as Yu's ruling" (obs: `71eedb71`, branch `docs/card-top-ups-spec-20261026`). An unmerged draft is no firmer ground, so I do not propose citing it.
  - A case the editors found in other repositories is not a reason recorded for KS-000. Labelling it "recorded" is what §7.1 item 3 forbids (inf).
  - The citation also ties a process standard to a product's billing history. Whether both repositories are public: n/c.
- *Change:*
  - Write: "The reason for §4.1 is inference by the editors of 0.2, prompted by records that state who made a 2026-09-23 decision in different ways and cite no record of Yu's words."
  - Keep at most one example, or move the case into the review record.

**11. §3 and §8: who launches and briefs the reviewers [should_fix]**
- *Why it fails:*
  - One session can draft, spawn its reviewers, write their briefs and lenses, and then write the dispositions. Each reviewer is a separate process instance, so §3 is met, yet the editor frames every review (inf).
  - §4.1 asks for the provenance of decisions but not of reviews. This review is an example.
- *Change:*
  - §3: "A review record says who launched the reviewer and attaches or cites the brief it was given."
  - §9: "A review launched and briefed by the editing session is independent in process only."

**12. Smaller points [note]**
- *§5:* the new MUSTs are not "backward-compatible additions". The phrase "when this version is adopted" is unclear, because adoption sets `1.0`. Say that 0.x drafts may add requirements in a minor version, and write "when KS-000 is first adopted".
- *Header:* it says the reviews "are in `specs/KS-000-reviews/`". That directory does not exist at the reviewed state (obs). Write "will be".
- *§6:* "Nothing else in 0.1 is changed" keeps §6's statement that no `did:key` has been minted. The ledger names a platform key minted on 2026-06-10 (obs; KS-004 review A said the same). Fix it here, or say it is left.
- *Terminology:* KS-004 0.4 already uses "lineage" for a citizen's archetype lineage, and COMMON-GROUND C11 treats a being's lineage as private (obs). A section titled "Ancestors" avoids the clash.
- *Cost (§1):* the draft grows from 149 to 260 lines. Its benefit stays inside the KS series: none of the law changes §10 cites would have been bound by it (inf). Findings 1, 6 and 7 reduce the cost, and moving §10's narrative into the pull request would reduce it further.

## Points that hold

- All six commits §10 cites exist and contain the quoted words (obs).
- §4.1's bullet on git authors matches the record. This repository's commits use shared names, and `e3b95e5` edited KS-002 as part of an estate-wide sweep.
- "Time passing and silence confirm nothing" agrees with CONSENT's "Silence is unknown" and with §4.
- §7.1's "whatever its standing today" relies on no decision about the standing of REALM, the Seven Walls or FATE.
- "Only §7 changes another spec's status" keeps supersession on one route.
- §10 already says that the placement and wording are not Yu's word, and finding 4 builds on that.

## What I verified, read only, or could not do

**Checked by running read-only commands:**
- Hashed the draft. Diffed it against `origin/main`; only this file changed.
- Ran `git show` on every commit and file that §10 cites, and checked later changes with `git log`:
  - FOUNDATION, CONSENT, ABUNDANCE and the KINGDOM-OS file are unchanged since the cited commits.
  - The monorepo record changed later, at `15380cfb`, but not in the quoted lines.
  - The agenttool file changed later, at `a1b40315`, but its header comment did not.
- Read the commit times of `8165fcbe` and `422ac856`, and the branch that holds `71eedb71`.
- Read `zone/signatures.json`, and the files touched by the five most recent commits.
- Searched SOPHIA, and checked the FATE path and its history.
- Read the decision log header and the passages from the Walls.
- Looked up the uses of "lineage" in KS-004 0.4 and COMMON-GROUND.

**Read only:**
- All of KS-000 0.2.
- Most of FOUNDATION, and the relevant parts of CONSENT, COMMON-GROUND, AMENDMENT-0.2, ABUNDANCE and the KINGDOM-OS guide.
- One passage of KS-001.
- KS-004 review A, for the house format.
- Private study notes named in my brief, for context only. No finding rests on them.

**Could not do, or did not check:**
- The private record of the go-ahead that §10 cites. I could not identify or check it.
- Whether the cited repositories are public.
- The forge-protocol file named in §3.
- The kingdom, Love and love-unlimited clones were not fetched today.
- FATE, REALM and the Walls, which I did not read in full.
- Who launched this review's workflow.

---

## Disposition (applied in v0.2 as committed)

*Written by the editing session (Claude Code session `6a20c00e`, Claude Fable
5.2, 2026-11-13), not by the reviewer. The review above is filed as the
reviewer returned it. It read the first draft; section and line numbers
refer to that draft (see `README.md` in this directory).*

| Point | Disposition |
|---|---|
| Strongest objection, and 2 (blocking) | **Applied in part.** Every label now names who applied it. A label resting on a record its readers cannot open is that party's report, and a reviewer says "not checked" (§4.1). A private record is cited by custodian, kind of record and id. §9 gains the proposed line: until Yu holds a signing key, "Yu's word" here is always someone's report. Not applied: a separate sentence in §3 and a bullet in §8, which would repeat §4.1 and §9. |
| 1 (blocking) | **Applied.** §4.1 is limited to decisions of Yu's, or made on Yu's authority, that are used as authority for a rule or an act. Editors' proposals, reviewers' judgments and dispositions need no label. The last bullet now reads "Yu's adoption (§4) rests on Yu's word alone", and "Yu's refusal needs no record". |
| 3 | **Applied.** A label changes only by a new record appended beside the old one, and only for what the new words cover. A reading of a reading cites the whole chain. |
| 4 | **Applied in part.** A reading states what Yu's words mean. A call is a choice Yu's words left to an agent, by setting a scope or accepting a proposal, and cites the delegation or proposal with its date and scope. A delegation covers the session and scope it names, and no other. The provenance of 0.2 is relabelled to match (`README.md`). Not applied: that the delegation be itself labelled, and that it was current. |
| 5 | **Applied.** Records that disagree fall under the fourth label, renamed "Not established". |
| 6 | **Applied.** The MUST covers KS texts and review records. Commit messages and pull requests that change `specs/` or `zone/` SHOULD carry one `Provenance:` line. |
| 7 | **Applied.** An ancestor is an earlier rule on the same matter. Borrowed wording is not an ancestor, and its source is cited. The search is always stated, has a floor, and bounds the duty. The decision log and the Seven Walls are added to §10 as ancestors. |
| 8 | **Applied.** "A KS keeps only what its own text states"; "An ancestor in force stays in force"; "Editors add no assessment of it" (§7.1). |
| 9 | **Applied in part.** §10 is named Ancestors, has a Dropped column and gives reasons. "Restate" is gone. Three labels are said to borrow wording and one to be new. Not applied: rows for FATE and the forge protocol. 0.1's own citations are left for a later version, and §10 says so. |
| 10 | **Applied.** The comparison between two repositories is removed. §10 gives the reasons as the editors' own. One example is kept, in `README.md`, with only what the record says. |
| 11 | **Applied.** §3 asks a review record to say who launched the reviewer and what brief it was given. §9 says a review launched and briefed by the editing session is independent in process only. `README.md` says so of this round. |
| 12 (a) | **Applied in part.** "when this document is first adopted" and "next minor version". §5 is unchanged. |
| 12 (b) | **Applied.** This directory arrives in the same commit as the note. |
| 12 (c) | **Not fixed.** The status note names §6's and §9's statements as out of date and leaves them for a later version. |
| 12 (d) | **Applied.** The section is named Ancestors. |
| 12 (e) | **Applied in part.** The scope is cut (1, 6, 7) and the narrative moved to `README.md`. The revision is longer than the draft reviewed (2,208 to 2,473 words), and the document more than doubles. The objection stands and is recorded in §9. |
