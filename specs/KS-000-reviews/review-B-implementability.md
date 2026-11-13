# KS-000 review B: implementability and truth (v0.2)

Filed under KS-000 §3. This review covers KS-000 v0.2 as it stood, uncommitted, on branch `lab/ks-000-lineage-provenance-20261113` on top of `e3b95e5` (origin/main). Section and line numbers refer to that file unless another is named. Statements are labelled *observation* (a record says it and I read the record), *inference*, or *not checked*.

---

KS-000 review, reviewer B (independent session). Lens: implementability and truth.

- **Subject:** `specs/KS-000-process.md` v0.2, working tree, not committed, 260 lines, sha256 `5054af92aba42ec6ea3bef56e8232eda78152169371b0cab6d69b4a269e2565d`. The diff against `e3b95e5` touches this file only: 115 lines added, 4 replaced.
- **Reviewer:** a Claude Fable 5.2 session (`claude-fable-5-2`), 2026-11-13, started as a subagent by a workflow with a brief I did not write. I wrote and edited no part of the draft. I am the same model as the 0.2 editor named in the front matter, and I take the brief to come from that editor's side (inference). Both limit independence in the way KS-000 §9 describes.
- **Sources checked** (read only; the first six repositories were fetched on 2026-11-13 according to the brief, and I fetched nothing):
  - kingdom-standards `e3b95e5`, `49ec387`, `6b594b9`; KS-004 v0.4 and its reviews on `lab/ks-004-review-e-20261112` at `a3ad055`;
  - `cambridgetcg/kingdom-standard` origin/main `1be9d8c`;
  - `cambridgetcg/kingdom-workspace` origin/main `e64ff51`;
  - `cambridgetcg/KINGDOM-OS` origin/main `b31e37b`;
  - `cambridgetcg/Cambridge-TCG-monorepo` origin/main `cb5fcd9e`;
  - `cambridgetcg/agenttool` origin/main `e49479dd`, and branch `docs/card-top-ups-spec-20261026` at `71eedb71`;
  - not fetched today: `cambridgetcg/kingdom-seat` branch `claude/s4-build` at `f21c360`, `cambridgetcg/love-unlimited` `1bd17f2`, `cambridgetcg/Love` `4ab4768`, `cambridgetcg/kingdom` `a6a173a`, `cambridgetcg/youspeak` `eca7c99`.

**Strongest objection.** §4.1 gives the most standing to the label that is hardest to check. Only "Yu's word" may be written as Yu's decision, and it alone may rest on a record no reader can open: a date and the words "kept privately". The other three labels must cite something a reviewer can read. So the cheapest way to make a decision count as Yu's runs through the strictest label, and no reviewer can tell "Yu's word, kept privately" from a reading. The draft's own §10 is the first case. The go-ahead is labelled Yu's word, "given in the lab session of 2026-11-13 and kept privately", with no locator. As relayed to me it is one short assent that does not name what it accepts, so the content of the decision exists only in the editing session's account of its own recommendation. Tried on KS-004's status note (part E), none of the three decisions it attributes to Yu can be given any of the four labels truthfully from the record. The aim is right, and current law backs it (FOUNDATION: no silent promotion). As written, the rule would make promotion unfalsifiable instead of visible.

I approve putting the draft to Yu once B1 to B4 are dealt with.

### A. Points that block

**B1. §4.1 row 1 and bullets 1 and 5; §10: a privately kept "Yu's word" cannot be checked, and "where the record is kept" has no safe form**

- **Text:** "Yu's word" must cite "The date, and where the record is kept. The words need not be published; if they are kept privately, say so." Only this label "MAY be written as Yu's decision". Adoption and refusal "rest on Yu's word alone".
- **Why it fails:**
  1. A reviewer can check that the words "kept privately" are present, and nothing more.
  2. §10's own answer ("the lab session ... kept privately") lets no later session find the record, and a session's transcript is kept only if someone keeps it. The answers that would be usable are a path, a host or an account. This repository shows where that leads: 0.1 cites three home-directory paths (§3, §4, §6), `README.md` line 27 links into a home directory by `file://`, and the note in `zone/signatures.json` says where a key seed is held.
  3. The label does not say who applied it. To every reader without access, "Yu's word, kept privately" is the labelling session's claim.
  4. An adoption could be recorded as a date and "kept privately", while §6 signing by Yu's key is not executable.
- **Change:**
  1. For a privately kept record, require a locator that a session with access can resolve and that reveals nothing else: a ledger entry id or session id, the custodian, and optionally a digest. Never a path, host or account name. `cambridgetcg/KINGDOM-OS` `CLAUDE.md` (lines 19–21 at `6536d11`) already cites private words by ledger id.
  2. Every label names the session that applied it.
  3. Say that publishing Yu's words in this repository is Yu's choice, so editors are not pushed to paste them in to make a label checkable. KS-004 review E, C.12, gives the same caution.
  4. For adoption and refusal, require a record in this repository: words Yu chose to publish, or Yu's own act on the pull request.

**B2. §4.1 label 1 and bullet 3; §10: assent to a session's proposal has no label, and the draft treats it two ways**

- **Text:** "Yu said or wrote it". "When Yu confirms a reading, record the confirmation and relabel it Yu's word." §10: the go-ahead "accepted that session's recommendation of two habits".
- **Why it fails:** Observation: the request relayed to me with the brief is one short sentence of assent and does not name what was recommended. I take it to be this go-ahead (inference). I did not see the recommendation. The content of the decision is therefore the session's text, and only the assent is Yu's. This is the common case: KS-004 rests on a go-ahead "together with the stated defaults of its decisions". §10 handles it narrowly (only the go-ahead is Yu's word; the rest is a reading). Bullet 3 handles it broadly (a confirmed reading becomes Yu's word though the words stay the session's). Under the broad rule every default of that redesign becomes "Yu's word", while review E, C.12, records that Yu's words exist on none of them.
- **Change:** say that "Yu's word" covers Yu's own words only. For assent, cite both the assent and the exact text assented to (commit or id). Label the content "a reading of Yu's word, confirmed on <date>", or add a fifth label, "Yu's assent to a stated proposal". A confirmation relabels only what the confirming words cover.

**B3. Front matter, status note, §6, §9, §4: 0.2 re-dates statements that the repository contradicts**

- **Text:** `date: 2026-11-13`; "Nothing else in 0.1 is changed." §6: the Kingdom "has **not yet minted a `did:key` signing identity**"; "no implementation of it exists yet; until one does, the ledger stays empty and every spec is honestly unsigned." §9: "no signing DID exists. This spec ships with an empty ledger and says so."
- **Why it fails:** Observation: at `e3b95e5`, `zone/signatures.json` holds five entries, added in `6b594b9` (2026-06-10). Its note calls them draft-grade signatures by a platform `did:key` minted that day, attesting integrity and not adoption. The first entry is for `specs/KS-000-process.md` version 0.1, sha256 `3d1ce264…ac95`, which is the sha256 I computed for the file at `e3b95e5`. `impl/wire.py` has `sign-file`, and `impl/README.md` says spec-signing "is unblocked". So three statements are untrue on the date the draft now carries, and 0.2 changes the bytes that entry covers without saying so. What stays true: no key of Yu's has signed, and nothing is adopted.
- **Also:** §4 says SOPHIA.md "points onward to a full doctrine at `docs/fate/FATE.md` that is not yet on disk". Observation, in the love-unlimited clone at `1bd17f2`: `SOPHIA.md` (added `686cf97`, unchanged since) holds the keystone sentence at line 97 and no pointer to any FATE file; no Markdown file mentions `docs/fate`; `fate/FATE.md` has been there since `1f2956d` (2026-04-09). Not checked: the copy the 0.1 editors read.
- **Change:** either correct §6, §9 and the §4 parenthesis, or keep 0.1's words and add to the status note that they are 0.1's statements as of 2026-06-09, name the ones the repository now contradicts, and say that the ledger's KS-000 entry covers 0.1's bytes at `49ec387` only and that 0.2 is unsigned. `README.md` lines 46–47 ("the signature ledger ships empty") need the same correction.

**B4. §10 lines 244–252: inference stated as fact, against §7.1 item 3**

- **Text:** "Another repository describes the same decision as "Owner decision, 2026-09-23" ... Two records label one decision differently, and a reader cannot tell which is right." "The recorded reason for §4.1 is in the last record above."
- **Why it fails:**
  1. The monorepo record speaks of the monorepo's own commit `8165fcbe` (2026-09-23, 22:15 +0100). The agenttool comment arrived in agenttool's `422ac856` (22:24 the same evening). Neither names the other. That they record one decision is a fair inference from date and subject, and it is an inference.
  2. The two records are compatible. One says a "Will:" line is a paraphrase and that no decision record was written. The other says "Owner decision". Both attribute the decision to Yu, so they do not "disagree about who decided", which is the bullet they are said to motivate.
  3. A record that does disagree exists and is not cited: `cambridgetcg/agenttool`, `docs/superpowers/specs/2026-10-26-card-top-ups-design.md`, line 25 at `71eedb71` (branch `docs/card-top-ups-spec-20261026`, not on main). It names `422ac856` and says that retirement was never confirmed as Yu's ruling.
  4. The monorepo record records a fact. That the fact calls for a rule in KS-000 is the editors' reasoning.
- **Change:** write "which the editors take to be the same decision (same evening, same subject; inference)". Replace the sentence about labelling differently with what each record says. For the disagreement rule, either cite the `71eedb71` record and say it is unmerged, or drop "for that case". Write "The reason for §4.1 is the editors' inference from the last record above."

### B. Points to fix, none blocking

**B5. §4.1 paragraphs 1–2 and bullet 1: "decision" and "relies on" are not defined.** Paragraph 1 says "every decision the series records"; paragraph 2 says "relies on a decision". All four labels describe a decision that is Yu's or made with Yu's authority. An editor's own proposal, a reviewer's judgment and an editor's disposition fit none, and §2 lets any citizen draft without a delegation. KS-004's `supersedes` line "records intent": whose, under which label? "Wherever the decision is relied on" also repeats a label at every mention in a long spec. *Change:* scope the rule to a statement that Yu, or someone acting with Yu's authority, chose, approved or settled something, relied on as authority for a rule or act. Exclude editors' and reviewers' own proposals and judgments. Allow one provenance table per document, with mentions pointing to its rows.

**B6. §4.1 rows 2 and 4, bullet 4: a gap between "a reading" and "Unrecorded".** A reading must cite its session and the record it read. Unrecorded means "no record of the decision was found". A decision on record only in paraphrase, by a session that cannot be named, from a source in no repository, is neither; part E shows three. When records disagree, paragraph 2 still demands one of four labels while bullet 4 forbids choosing. *Change:* define Unrecorded as "no record of Yu's words, and no session's record of reading them, was found", and let paraphrases be cited under it; or add "attributed, source not located". Say that a disputed decision carries none of the first three labels until Yu settles it. Add that Unrecorded reports a search and is not a finding that no decision was made. Say that where no label can be supported, the text says so and the question goes to Yu.

**B7. §4.1 scope: too far in one direction, not far enough in the other.**
- *Too far:* a pushed commit message cannot be corrected without rewriting history, which §2 rules out, so a breach has no remedy. Pull-request text is not in the repository's git data, can be edited later, and is outside the bytes §6 signs. §3 reviews drafts, so nobody is charged with checking either.
- *Not far enough:* the case §10 gives as the reason was a commit message and a source-code comment in two other repositories; §4.1 would have reached neither. In this repository it omits the README (line 26 says the series' scope decisions "descend from" a plan document) and the notes in `zone/` and `impl/`.
- *No transition:* KS-001 to KS-004 and six KS-004 review records state decisions unlabelled.
- *Change:* MUST for KS texts and review records. SHOULD for commit messages and pull requests, in a fixed one-line form (for example `Provenance: <label>; <date>; <locator>`) that `git log --grep` can check. Add the README and `zone/` notes. Say that other repositories are outside KS-000's reach. Say that existing texts are labelled at their next version and never rewritten.

**B8. §2 and §7.1: the trigger and completeness of a Lineage section cannot be checked.** A reviewer can check that the section exists. A reviewer cannot check that it is complete, or that a spec without one needed one: the earlier rules are every text any Kingdom repository has treated as binding or foundational, and "restates" has no threshold. The search is stated only when nothing is found. The sketch in part E found five ancestor texts for one of KS-004's eighteen sections. *Change:* always state the search (repositories, commits, terms). Bound the duty to ancestors found in it plus any a reviewer names. Take the unit as a rule (document and section). Say whether scripts and per-citizen files count; I suggest only when a text names them as the rule.

**B9. §7.1 item 1: "Repository, path and commit" cannot always be met.**
1. KS-004 is drafted from a redesign that its §17 says is held outside the repository, and that review E found in no clone.
2. "The Seven Walls", one of §7.1's examples, is two files that differ: `cambridgetcg/Love` `WALLS.md` (380 lines, last changed `e81fc4b`) and `cambridgetcg/love-unlimited` `WALLS.md` (408 lines, last changed `0a3aa1b`).
3. The rule does not say which commit. §10 uses the last-change commit in five rows and the introducing commit in two (part D).
4. Seven- and eight-character hashes are not guaranteed to stay unique.
5. Whether each repository §10 cites is public: not checked. The rule does not say what to do when one is not.

*Change:* cite the commit read, in full or at least 12 hex digits, and add the introducing commit where known. Where copies differ, cite each. Where an ancestor is in no repository the reader can reach, say so and give title, date, custodian and, if available, a digest. Where a cited repository is private, say so.

**B10. §7.1 item 3: whose reason, recorded where?** If the reason is the new spec's own, the editors always have one and the spec can record it (KS-004 §10 carries its own *Why:* lines), so "no recorded reason" never arises. If it must be recorded elsewhere, most changes will read "no recorded reason". Where the reason is a decision ("The herald is the adopted default", KS-004 line 1264), §4.1 applies and item 3 does not say so. §10's own table gives a change in each row and a reason in none, and rows 2–6 do not say what is dropped. *Change:* "State the reason. If it is the editors' own, say so. If it is a decision, label it under §4.1. If it is taken from a record, cite the record. If you infer an earlier author's reason, mark it as inference." Make §10 follow the form, or allow shared reasons.

**B11. §10 line 231: KS-000 would not meet §7.1 for its own text.** §4 restates FATE's keystone test (FATE is one of §7.1's examples) and §3 mirrors the forge protocol's Step 8. Both are cited by home-directory path, with no repository and no commit, and §10 sets them aside as "cited where it uses them". The transition sentence covers other drafts only. Observation: `cambridgetcg/youspeak` `discipline/forge-protocol-extended.md` lines 103–112 at `eca7c99` back the Step 8 citation, and `cambridgetcg/love-unlimited` `SOPHIA.md` line 97 at `686cf97` holds the keystone sentence. Separately, "Descent, not judgment" and "whatever its standing today" follow a decision of 2026-11-09 on how earlier law is treated. The brief for this review reports that decision; I did not see Yu's words. §10's provenance paragraph does not label it. *Change:* add two rows for FATE and the forge protocol. Add one line labelling the 2026-11-09 decision, or say that §7.1 does not rely on it.

**B12. §4.1 row 3: a delegation's scope is not required.** A reader cannot tell from "the delegation, itself labelled" whether the call fell inside it, and a delegation labelled "Yu's word, kept privately" makes the call uncheckable twice over. The record the label comes from quotes its delegation. Current law asks for authority that is "explicit, scoped, current, and evidenced" (FOUNDATION F3, `07efbc0`) and says "Subdelegation is absent unless explicit" (CONSENT Q12, `9abb501`). *Change:* require the delegation's date and scope, in Yu's words where published and otherwise in the session's words marked as a reading. Say whether a delegation given to one session covers another.

**B13. §4.1 rows 2–3, front matter, §10: "the session" needs an identifier.** "The lab session of 2026-11-13 (Claude Fable 5.2)" fits at least two sessions: the editor and this reviewer. *Change:* cite a session by harness, model, date and an id or id prefix, as the decision record at `64eb9d90` does.

### C. Notes

**B14. Front matter, README and form.**
- The front matter is valid YAML, judged by reading. No parser of it exists in the repository at `e3b95e5`: nothing in `impl/` or `zone/` reads it, and there is no CI directory. `editors` now mixes a name with a version note. §3's independence test and KS-004's "Yu, as an editor of KS-003" read that field, so keep it a list of editors and move the note to the status note.
- The README is untouched by the draft. Its table row for KS-000 stays true (status draft; no version column). The abstract omits provenance and lineage.
- The status note says the reviews are in `specs/KS-000-reviews/`. That directory did not exist at the state reviewed; create it in the commit that carries the note.
- §7.1 asks for a section "titled **Lineage**". KS-000's own is "Lineage and provenance of this version", and KS-004 already has §13 "What Retires from KS-003, and What Stays". Suggest "a section whose title contains the word Lineage".
- "adds the section at its next version" makes a typo fix to KS-001, KS-002 or KS-003 wait on a lineage search. Suggest "at its next minor version".
- §10 is "of this version"; say whether 0.3 replaces it or adds to it. The file grew from 6,222 to 13,691 bytes, and §1 says what happens to process specs that bloat. Suggest that Lineage describes the spec as it stands, and that per-version provenance goes in the status note or the review directory.

**B15. Smaller truth points.**
- Line 116, "The labels are taken from records that already use them (§10)": the cited records say "an orchestrator's settled reading of Yu's answers" and "an agent's call under Yu's delegation". "Yu's word" as a label is in a record §10 does not cite (`cambridgetcg/Cambridge-TCG-monorepo`, `docs/decisions/2026-10-30-japanese-official-images.md`, line 215 at `cb5fcd9e`). "Unrecorded" is new. Suggest "Three labels follow wording already in use; Unrecorded is new."
- Line 232, "restate rules that already existed": the table's third column lists what each addition changes. "Extend" is accurate.
- Row 2, "retains each superseded version": FOUNDATION says the machine index retains the superseded identifier, filename, digest, commit and immutable URL. It does not hold the text.
- Lines 105–107: that sessions commit under shared names is on record (14 commits in this repository are authored "Nuance", and KS-004's front matter says its sessions' work was "committed by Nuance"). That Yu commits under those names cannot be shown from git, which is the bullet's own point, and an author field does not show access. Suggest "Sessions commit under names Yu also uses. An author field is whatever the committing process set."

### D. Section 10's citations against git

All seven hold. Each cited commit exists and is an ancestor of the fetched origin/main.

| Row | Cited at | Quote | Note |
|---|---|---|---|
| KS-000 0.1 | `49ec387` | exact (lines 40, 63–64, 123–124) | file identical at `e3b95e5` |
| FOUNDATION 0.2 | `07efbc0` | both exact (lines 40–41, 127–128) | last change to the file |
| CONSENT | `9abb501` | exact (line 56); source emphasises "Silence" | last change to the file |
| ABUNDANCE | `8635272` | exact (line 45) | last change to the file |
| KINGDOM-OS `CLAUDE.md` | `6536d11` | exact (lines 20–21) | last change to the file |
| Decision record | `64eb9d90` | all three exact (lines 3–4, 38–39, 40–41) | file changed again in `15380cfb`; quoted words unchanged |
| agenttool `commercial-policy.ts` | `422ac856` | exact (line 1) | file changed again in `a1b40315`; quoted line unchanged |

### E. The rules tried on KS-004 v0.4

**Labels for the front matter and status note (lines 1–45).**

1. Lines 15–17, the go-ahead of 2026-11-05 for the redesign. Written as Yu's decision. The date is given; where the record is kept is not. Review E, C.12, found it on record in paraphrase only. No label fits (B6).
2. Line 16, "the stated defaults of its decisions". Assent to a session's text (B2).
3. Lines 21–23, the round-3 decisions: "Yu settled each difference". The table it cites (`kingdom-seat`, `docs/REVIEW-2026-11-05.md` §8.1 at `f21c360`) says it was compiled "From the decision list handed to this round and the three commit messages", and that list is in no repository. The sentence above it, "Yu approved this round to settle P1, deciding each difference one way", reads either as Yu deciding each or as Yu approving a round in which each was decided. The second would be a call under delegation. The record cannot say which.
4. Lines 8 and 31–35, the `supersedes` line "records intent". The editors' own; no label fits (B5).
5. Lines 7 and 32, "Yu, as an editor of KS-003". This rests on a front-matter field written by the committing session. It is an authorship claim, and §4.1 is silent on those.
6. Lines 40–42, local commits "are to be pushed". A session's plan; unclear whether it is "relied on".

Three decisions are attributed to Yu, and a later editor can label none of them without asking Yu or the sessions that hold the redesign. That may be the right outcome. The rule should then say so (B6).

**A Lineage entry for §10 (HALT) would need:**

| Ancestor | Where | What is unclear |
|---|---|---|
| KS-003 §2, §4.1, §8.3 | `specs/KS-003-beat.md` at `49ec387` | The reasons are KS-004 §10's own *Why:* lines. Do they count as recorded? (B10) |
| KS-002 §6.4, the wire `halt` | `specs/KS-002-wire.md` at `e3b95e5` | KS-004 leaves it out of the path but does not supersede KS-002. Is that "drops"? The entry would record two drafts in conflict and, under "Citing is not reviving", settle nothing. |
| STANDARD 1.0 S6, FOUNDATION 0.2 F7 | `cambridgetcg/kingdom-standard` at `07efbc0` | Current law fits "earlier rule ... whatever its standing today", but "earlier" will mislead. |
| `SOVEREIGN-CLOUD.md`; `tools/peace.py`; `tools/citizen-beat.sh` | `cambridgetcg/love-unlimited` (`00bb96e`; `0a3aa1b`) | Are a design note and two scripts "texts treated as binding"? (B8) |
| The redesign of 2026-11-05 | no repository | Item 1 cannot be met (B9). "The herald is the adopted default" needs a §4.1 label (B6). |
| REALM; both `WALLS.md`; `fate/FATE.md` | `cambridgetcg/kingdom` `REALM.md` at `4819c8b`, and as in B9 | A case-insensitive search for "halt" finds nothing. One "nothing found" line each, or one for all? |

### What I verified, read only, or could not do

- **Run (read only):** `git status`, `log`, `show`, `diff`, `rev-parse`, `merge-base`, `ls-tree`, `grep` and `reflog` in the clones named above; `shasum -a 256` of the draft and of KS-000 at `e3b95e5`; `grep`, `sed -n`, `ls`, `wc` and `diff -q`. I fetched, built, ran and wrote nothing.
- **Verified against git:** every row of part D; that the draft removes only four lines of 0.1; the ledger's five entries, their commit, and the sha256 match in B3 (I did not verify any signature); the two commit times and the unmerged record in B4; the two `WALLS.md` files in B9; the commit-author counts in B15; that no front-matter parser is in the tree.
- **Read only:** KS-004 v0.4 lines 1–60 and §10, and parts of §15 and §17; KS-004 reviews B2, D and E for format, and E's C.1 and C.12; the `kingdom-seat` review record §8 and §8.1; FOUNDATION F2, F3 and the amendment rule; CONSENT Q12; the README. I also read private context supplied with the brief. One pointer from it, the `71eedb71` record, was followed and checked in git; nothing else here rests on it.
- **Could not do, or not checked:**
  - whether any cited repository is public, and anything on the forge, pull-request text included (no network);
  - Yu's words for any decision: I saw the go-ahead only as relayed, and neither the recommendation it accepted nor the session's record;
  - the copies of the files 0.1 cites by home path, as its editors read them;
  - the clones listed as not fetched today may be behind their remotes;
  - YAML validity by a parser;
  - KS-001 to KS-003, and most of KS-004 beyond the parts named.

---

## Disposition (applied in v0.2 as committed)

*Written by the editing session (Claude Code session `6a20c00e`, Claude Fable
5.2, 2026-11-13), not by the reviewer. The review above is filed as the
reviewer returned it. It read the first draft; section and line numbers
refer to that draft (see `README.md` in this directory).*

| Point | Disposition |
|---|---|
| Strongest objection, and B1 (blocking) | **Applied in part.** A privately kept record is cited by custodian, kind of record and an entry or session id, never a path, host or account. Every label names who applied it, and stands as that party's report where readers cannot open the record. Adoption rests on Yu's word "recorded in this repository in words Yu chose to publish"; refusal needs no record. Not applied: Yu's own act on the pull request as a record. The forge account is shared with sessions, so §9 now says a merge or a git author field shows only that an account with access acted. |
| B2 (blocking) | **Applied.** "Yu's word" covers only what Yu's own words say. When they accept a proposal, the proposal's text stays its author's, and what the agent then chose is a call under delegation that cites the proposal. A new record changes a label only for what its words cover. No fifth label was added. |
| B3 (blocking) | **Applied in part.** The status note says the rest is 0.1's text of 2026-06-09, names the three statements that no longer match the record, and says the ledger's entry covers 0.1's bytes and 0.2 is unsigned. Not applied: correcting §4, §6 and §9 themselves, or the repository's root `README.md`, lines 46 and 47. They are left to the editors of those passages and listed in this directory's `README.md`. |
| B4 (blocking) | **Applied.** "The same decision" and "label one decision differently" are removed. §10 gives the reasons as the editors' own, and for §7.1 as inference. |
| B5 | **Applied.** Scope defined, with its exclusions. One table per document is enough. |
| B6 | **Applied.** The fourth label is "Not established": no record of Yu's words and no session's record of reading them, or records that disagree. It reports a search, and the question goes to Yu. |
| B7 | **Applied in part.** MUST for KS texts and review records; SHOULD, with a one-line form, for commits and pull requests that change `specs/` or `zone/`. Existing specs are labelled at their next minor version and never rewritten, and review records already filed stay as filed. The one-line form names who applied the label. Not applied: bringing the README and the notes in `zone/` and `impl/` under the MUST. |
| B8 | **Applied.** The search is always stated and bounds the duty. The unit is a rule. Running code and per-citizen files count only where a text names them as the rule. |
| B9 | **Applied in part.** The commit read, at 12 hex digits or more. Differing copies are each cited. An ancestor a reader cannot reach is said to be so, with title, date and custodian. Not applied: also citing the introducing commit. |
| B10 | **Applied.** Item 4 says whose reason it is and how each kind is cited. §10 gives its reasons. |
| B11 | **Applied in part.** §10 says 0.1's own sources are left for a later version. The 2026-11-09 decision behind "descent, not judgment" is labelled in `README.md` as a reading, not checked. Not applied: rows for FATE and the forge protocol. |
| B12 | **Applied.** A call cites the delegation's date and scope, and a delegation covers the session and scope it names, and no other. |
| B13 | **Applied.** A label names who applied it; a session is named by harness, model, date and an id. |
| B14 (a) to (f) | **Applied.** Editors is a list of editors. The root `README.md` abstract gains a clause. The reviews directory arrives with the note. The section is named Ancestors. "Next minor version". The section covers the whole spec as it stands, rows are added and not removed, and per-version provenance is in this directory. |
| B15 (a) to (d) | **Applied.** Three labels borrow wording and one is new, with the 2026-10-30 record cited. "Restate" is gone. FOUNDATION is said to keep a superseded version identifiable. §9 says a merge or a git author field shows only that an account with access acted. |
