# KS-000 reviews

## Round 1: version 0.2 (2026-11-13)

**What was reviewed.** The first draft of 0.2 (`specs/KS-000-process.md`,
sha256 `5054af92aba42ec6ea3bef56e8232eda78152169371b0cab6d69b4a269e2565d`,
260 lines, 2,208 words). Reviews A and B read those bytes, and their section
and line numbers refer to them. That draft is not committed here, because it
quoted a sentence from a repository that is not public. The editing session
keeps it. Version 0.2 as committed is that draft revised to answer the two
reviews. Each review ends with a table of how every point was disposed of.

**Who launched and briefed the reviewers (KS-000 §3).** The editing session
(Claude Code session `6a20c00e`, Claude Fable 5.2) launched both reviewers
as read-only subagents and wrote both briefs. Reviewer A (Claude Opus 5.5)
was asked to test coherence and process capture. Reviewer B (Claude Fable
5.2, a separate session) was asked to test implementability and truth, and
to try the rules on KS-004 draft 0.4. Each was asked to break the draft and
to record a strongest objection. The briefs also reported Yu's word of
2026-11-09 on earlier law and named private study notes for context, and
reviewer B says the go-ahead reached it as relayed. Under §9 that
independence is in process only. The reviewers wrote the reviews. The
editing session filed them as returned and wrote the dispositions.

**Repositories.** Checked on 2026-11-13: every repository cited in KS-000
0.2 and in this file is public. The two reviews also name two that are not,
`cambridgetcg/Love` and `cambridgetcg/kingdom-workspace`, by name, file and
commit. Review A also paraphrases one sentence of the second.

### Provenance of version 0.2 (KS-000 §4.1)

Labels applied by the editing session: Claude Code, Claude Fable 5.2,
2026-11-13, session `6a20c00e`. Custodian of the private record cited
below: Yu. Kind of record: that session's transcript. Neither reviewer
could open it, so every row is that session's report: not checked.

| Statement | Label | Cites |
|---|---|---|
| The go-ahead for this version | Yu's word | 2026-11-13, in the transcript. |
| That the go-ahead accepted this proposal: cite the earlier rule when a rule changes, and record whose decision a text rests on | A reading of Yu's word | The go-ahead above, and the session's recommendation of 2026-11-09 as it stood in the same transcript. The proposal's text is the session's, not Yu's. |
| That the two habits belong in KS-000; the four labels; the name Ancestors; every other word of §4.1, §7.1 and §10 | A call under delegation | The proposal of 2026-11-09, accepted 2026-11-13 (the two rows above). Scope: the two habits. |
| §7.1's "Descent, not judgment" and "whatever its standing today" | A reading of Yu's word | Yu's word of 2026-11-09 on how earlier law is to be treated, in the same transcript. |

Yu overturns any of the last three by saying so. Adoption remains §4's.

### Evidence for the reasons §10 gives

For §4.1:

- Observation. `cambridgetcg/Cambridge-TCG-monorepo`,
  `docs/decisions/2026-10-20-rewardspro-free-only-relaunch.md` at
  `64eb9d9057eb`, says of an earlier commit that its "Will:" line "is an
  agent's paraphrase, not Yu's words", and that "No decision record was
  written for it."
- Observation. Review B tried the labels on the three decisions that the
  status note of KS-004 draft 0.4 attributes to Yu, and could support none
  of the first three labels from the record (review B, part E and B6).
- Inference. A reader of this series cannot today tell Yu's words from a
  session's paraphrase of them.

For §7.1:

- Observation. The search §10 describes found no record of a reader failing
  for want of the section.
- Observation. Review B sketched an entry for one section of KS-004 draft
  0.4 (§10, HALT) and found five ancestor texts, four of them in three
  repositories and one in none (review B, B8 and part E).
- Inference. History that is kept but never cited is hard to use.

### Borrowed wording

- The label "Yu's word": `cambridgetcg/Cambridge-TCG-monorepo`,
  `docs/decisions/2026-10-30-japanese-official-images.md` at `f6cf51deeb85`.
- The label "A call under delegation": "an agent's call under Yu's
  delegation, not Yu's own decision. Yu overturns it by saying so.", the
  2026-10-20 record above.
- The label "A reading of Yu's word": "an orchestrator's settled reading of
  Yu's answers; the verbatim words are kept privately",
  `cambridgetcg/KINGDOM-OS`, `CLAUDE.md` at `6536d11036da`.
- §4.1's bullet on silence: "Silence is unknown.",
  `cambridgetcg/kingdom-standard`, `CONSENT.md` at `9abb501aa35a`.

"Not established" is new in 0.2.

### Statements of 0.1 that no longer match the record

Named in the status note and left for a later version. All are read in this
repository at `e3b95e521629` unless another is named.

- §6 says the Kingdom "has not yet minted a `did:key` signing identity" and
  that "the ledger stays empty". §9 says the spec "ships with an empty
  ledger". `zone/signatures.json` holds five entries. Its note calls them
  draft-grade signatures by a platform key minted 2026-06-10, which attest
  the bytes of the drafts and not adoption. Its KS-000 entry covers 0.1's
  bytes at `49ec387c0300`.
- §6 says of the signing layer that "no implementation of it exists yet",
  and §9 that signing is "not yet executable". `impl/wire.py` calls itself
  "the KS-002 reference implementation", and `impl/README.md` says "KS-000
  §6 spec-signing is unblocked".
- §4 says SOPHIA.md "points onward to a full doctrine at
  `docs/fate/FATE.md` that is not yet on disk". In
  `cambridgetcg/love-unlimited` at `1bd17f219b10`, `SOPHIA.md` holds the
  keystone sentence and no such pointer, and the repository has a
  `fate/FATE.md` (review A, 9).
- The repository's root `README.md`, lines 46 and 47, says "The zone file
  ships seeded but unsigned; the signature ledger ships empty". The ledger
  has entries for the four drafts and for the zone file. Not changed in
  this round.

### Re-check of the revised text

Two more readers read the revised text before it was committed. The editing
session launched both as read-only subagents, and its workflow script wrote
their briefs. One (Claude Opus 5.5) checked every quotation, commit and
count against git. The other (Claude Fable 5.2) checked each disposition
against the text, and the text against itself.

They read these bytes: the spec at sha256 `97a244fc1f97…`, this file at
`966b4c2e0305…`, review A at `9a5af01cfede…` and review B at
`80adb9d4e08b…`. Both found every quotation exact and every reviewer point
disposed of. They also found three things that had to change and about
fifteen smaller ones. All were applied afterwards:

- §10 cited FOUNDATION's sentence on silent promotion to F1. It stands under
  "Five kinds of statement". Rows now name their sections.
- The provenance table above gave the accepted proposal a label that is not
  one of §4.1's four. It is now a reading, and a call no longer overlaps it.
- §10's search named file commits where it meant the heads searched, and
  said three clones were not fetched that day when they had been.
- A citation of a copy of the Seven Walls in a repository that is not
  public was replaced by the public copy.
- The list of 0.1's out-of-date statements was two short.
- "Never a path, host or account" was joined to the private case. A label
  now names who applied it, not only a session. Yu's refusal needs no
  record. About ten lines were cut from §2, §4.1 and §7.1.
- §9 said the document "nearly doubles". By words it more than doubles.

The text as committed has not been read again since those changes.
