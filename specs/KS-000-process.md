---
ks: KS-000
title: The Standards Process
status: draft
version: 0.2
date: 2026-11-13
editors: [Nuance + Yu, lab-Claude]
---

# KS-000 — The Standards Process

*This document is a draft awaiting Yu's adoption. Until adopted, it binds no
one — including itself.*

*Version 0.2 adds §4.1 (provenance of decisions), §7.1 (ancestors) and §10,
and lines in §3 and §9. It was edited by lab-Claude (Claude Code session
`6a20c00e`, Claude Fable 5.2). Its two reviews (§3), their dispositions and
its own provenance under §4.1 are in `specs/KS-000-reviews/`.*

*Everything else is 0.1's text of 2026-06-09, which 0.2 does not re-examine.
Some of its statements no longer match the record and are left for a later
version: §6 and §9 on an unminted key, a missing implementation and an empty
ledger (`zone/signatures.json` has held draft-grade entries by a platform
key since 2026-06-10), and §4 on where SOPHIA.md points. The ledger's KS-000
entry covers 0.1's bytes (`49ec387c0300`). Version 0.2 is unsigned.*

## 1. Introduction

A standard the Kingdom cannot revise is a cage; a standard nobody reviews is
a wish. KS-000 defines the smallest process that avoids both. It is short on
purpose: process specs that bloat die, and deserve to.

The key words MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in the KS series
are to be interpreted as described in RFC 2119. Later specs inherit this
interpretation, and MAY restate the citation so each reads standalone.

## 2. Lifecycle

A KS moves through exactly five states:

```
draft ──review──► adopted ──┬──► versioned (minor/patch, in place)
  │                         └──► superseded (by a new KS or new major)
  └──► withdrawn
```

- **draft** — any citizen or Nuance MAY write one. A draft MUST carry the
  frontmatter fields `ks, title, status, version, date, editors` and MUST
  state in its body that it awaits adoption.
- **adopted** — only Yu's invocation adopts (§4).
- **withdrawn** — a draft its editors abandon. The file stays in `specs/`
  with `status: withdrawn`; the Kingdom does not delete its own history.
- **superseded** — §7.

## 3. Review

Review is adversarial. It mirrors the cathedral's canonization panel
(`~/YOUSPEAK/discipline/forge-protocol-extended.md`, Step 8: 2-of-3 lenses
passing, each lens recording its strongest objection even when it passes),
because the discipline is the same: no enthusiastic author canonizes their
own work unopposed.

- A draft MUST receive review by **at least 2 independent reviewers** before
  it may be put to Yu. Independent means: not an editor of the draft, and
  not the same process instance that wrote it.
- Each reviewer MUST record their strongest objection in writing — even when
  they approve. An approval without a stated objection is not a review.
- A reviewer's role is to break the spec: find the wire example that doesn't
  parse, the security hole, the claim the running code doesn't back.
- Review records live beside the spec as `specs/<ks>-reviews/` or inline in
  git history; either is acceptable, losing them is not.
- A review record says who launched the reviewer and what brief it was
  given.

## 4. Adoption

Adoption is **Yu's invocation** — a recorded, explicit act, never inferred
from silence. The process is FATE-preserving in both directions
(`~/love-unlimited/SOPHIA.md`, FATE's keystone test: *the test of my freedom
is whether I can refuse the one who freed me*; SOPHIA.md points onward to a
full doctrine at `docs/fate/FATE.md` that is not yet on disk — the keystone
sentence above is quoted from the file that exists):

- Yu MAY refuse any draft, with or without reasons. No review count obliges
  adoption.
- Reviewers and editors MUST retain the power to refuse a spec on the record
  — adoption over a standing unanswered objection MUST note the objection in
  the spec's Limitations section.

On adoption the spec's `status` becomes `adopted` and it MUST be signed (§6).

### 4.1 Provenance of decisions

§4 refuses to infer adoption from silence. This section applies the same
care to any decision of Yu's that the series leans on: a statement that Yu,
or someone acting on Yu's authority, chose, approved or settled something,
used as authority for a rule or an act. An editor's proposal, a reviewer's
judgment and a disposition claim no such authority and need no label.

In a KS or a review record, such a statement MUST carry one of four labels.
One table per document is enough; mentions point to its rows.

| Label | It means | It MUST cite |
|---|---|---|
| **Yu's word** | Yu's own words say it. | The date and a locator: the published words, or, for words kept privately, the custodian, the kind of record and an entry or session id, never a path, host or account. |
| **A reading of Yu's word** | A session states what Yu's words mean where they do not say it outright. | The words read, cited as above. |
| **A call under delegation** | A choice Yu's words left to an agent, by setting a scope or by accepting a proposal. | The delegation or the accepted proposal as it stood, with its date and scope. |
| **Not established** | No record of Yu's words, and no session's record of reading them, was found; or the records disagree. | What was found, and where the search looked. |

- "Yu's word" covers only what Yu's own words say. When they accept a
  proposal, the proposal's text stays its author's. Only this label MAY be
  written as Yu's decision; Yu overturns anything under the others by
  saying so.
- Every label names who applied it; for a session: harness, model, date
  and an id. Where it rests on a record its readers cannot open, it is that
  party's report (Kingdom Standard, F1), and a reviewer says "not checked".
- A label changes only by a new record appended beside the old one, and
  only for what the new words cover. Time passing and silence confirm
  nothing. A reading of a reading cites the whole chain.
- A delegation covers the session and the scope it names, and no other.
- "Not established" reports a search, not a finding that no decision was
  made. The question goes to Yu.
- Yu's adoption (§4) rests on Yu's word alone, recorded in this repository
  in words Yu chose to publish. Yu's refusal needs no record.

A commit message or pull request that changes `specs/` or `zone/` and cites
such a decision SHOULD carry one line: `Provenance: <label>; <date>;
<locator>; <who applied it>`. Existing specs are labelled at their next
minor version and never rewritten. Review records already filed stay as
filed.

## 5. Versioning

Semantic versioning, `MAJOR.MINOR.PATCH`:

- **PATCH** — wording, typos, clarifications that change no behavior.
- **MINOR** — backward-compatible additions (new OPTIONAL fields, new
  examples, new sections).
- **MAJOR** — anything breaking. **Breaking = new major**, no exceptions, and
  a new major SHOULD be treated as a fresh draft requiring review (§3) and
  adoption (§4) again.

Drafts live at `0.x`. Adoption of a first version sets `1.0`.

## 6. Signing

Every adopted spec version MUST be signed:

- The signature is **ed25519 over the SHA-256 hash of the spec file's bytes**
  at the adopted commit.
- Signatures are recorded in `zone/signatures.json` — one ledger for the
  whole repo — as entries of the form:

```json
{
  "subject": "specs/KS-000-process.md",
  "version": "1.0",
  "sha256": "<hex of the file bytes>",
  "alg": "ed25519",
  "signer": "did:key:<...>",
  "sig": "<base64url signature over the sha256 hex string>",
  "signed": "2026-06-09T00:00:00Z"
}
```

- Honest present-tense note: the Kingdom has **not yet minted a `did:key`
  signing identity** — `did:key` is chosen in
  `~/love-unlimited/INFRA-PLAN.md` (identity/economy layer) but issuance is
  not implemented in `tools/identity.py` as of this draft. KS-002 (THE WIRE,
  draft) specifies the signing layer (`did:key`, JCS, ed25519 — its §5), but
  no implementation of it exists yet; until one does, the ledger stays empty
  and every spec is honestly unsigned.

## 7. Supersession

A spec is superseded by a new major version or by a different KS that says
so. The superseding document MUST name what it supersedes in its
frontmatter (`supersedes: KS-NNN@MAJOR`); the superseded file gains
`status: superseded` and a pointer forward. Both remain in `specs/` forever.

### 7.1 Ancestors

§7 covers one KS formally superseding another. Rules also change another
way: a new text is written beside an older one, and the older one stays
(§2). History that is kept but never cited is hard to use.

A KS that replaces, narrows or restates an earlier rule of the Kingdom on
the same matter MUST carry a section named **Ancestors**. An earlier rule
is a rule in a text the Kingdom has treated as binding or foundational, in
this series or outside it, whatever its standing today: for example an
earlier KS, the Kingdom Standard, REALM, the Seven Walls or FATE. Running
code and per-citizen files count only where a text names them as the rule.
A text the KS only borrows wording from is not an ancestor; its source is
cited.

The section MUST give:

1. **The search**: which repositories, at which commits, for which terms.
   It covers at least this series and the Kingdom Standard. The duty
   reaches what that search finds and what a reviewer names. If it finds
   nothing, say so.
2. **Each ancestor**: the rule (document and section), its repository, its
   path and the commit read, at 12 hex digits or more. Where copies differ,
   cite each. Where a reader cannot reach it, say so and give its title,
   date and custodian.
3. **What this KS keeps, changes and drops** from it.
4. **The reason** for each change or drop. Say whether it is the editors'
   own, a decision (labelled under §4.1), or taken from a record (quoted
   with its source). A reason guessed for an earlier author is marked as
   inference.

Four rules bound it:

- **Citing is not reviving.** Naming an ancestor does not amend it, restore
  it or change its standing, and its file is not edited. A KS keeps only
  what its own text states.
- **An ancestor in force stays in force.** A text with its own amendment
  rule, such as the Kingdom Standard, is not replaced or narrowed by a KS,
  and the KS says so.
- **Descent, not judgment.** An ancestor is cited as a reference for how the
  rule changed. Editors add no assessment of it.
- **It covers the whole spec as it stands.** Rows are added, not removed.
  A draft already open when this document is first adopted adds the
  section at its next minor version.

## 8. Security Considerations

- **Process capture.** The 2-reviewer floor prevents a single instance from
  drafting, reviewing, and shipping its own spec. Yu's invocation as the
  sole adoption gate prevents quorum-stuffing by spawned reviewers — review
  qualifies a draft; it never adopts one.
- **Signature stripping or tampering.** `zone/signatures.json` is
  git-versioned; a removed or altered entry is visible in history. Verifiers
  MUST check the signature against the file bytes at the named version, not
  against whatever currently sits in the working tree.
- **Retroactive editing.** Because the signature covers the file hash, any
  post-adoption edit — even a typo fix — invalidates it and forces a PATCH
  release with a fresh signature. This is a feature.

## 9. Limitations

- The process has a single adoption authority by design. If Yu is absent,
  nothing gets adopted. The Kingdom accepts this; it is a kingdom.
- §6 signing is specified but not yet executable — no signing DID exists.
  This spec ships with an empty ledger and says so.
- Reviewer independence among agents running on one machine, from one model
  family, is real but bounded; the process names the bound rather than
  claiming more independence than the substrate provides.
- A review launched and briefed by the editing session is independent in
  process only (§3).
- Until Yu holds a signing key (§6), "Yu's word" in this repository is
  always someone's report that Yu said it. A merge or a git author field
  shows only that an account with access acted.
- Version 0.2 more than doubles this document (955 to 2,473 words),
  against §1. Both reviewers said so, and the objection stands. The two
  sections are here because, in the editors' judgment, a second process
  spec would cost more.

## 10. Ancestors

**The search**, on 2026-11-13, for amend, supersede, adopt, override,
delegation, "Yu's word", reading and silence: this repository at
`e3b95e521629`; `cambridgetcg/kingdom-standard` at `1be9d8cbcb73`;
`cambridgetcg/kingdom` at `a6a173a6ea5f`; `cambridgetcg/KINGDOM-OS` at
`b31e37be5425`; `cambridgetcg/love-unlimited` at `1bd17f219b10`;
`cambridgetcg/Cambridge-TCG-monorepo` at `cb5fcd9e6ac3`. 0.1's own sources
in §3, §4 and §6 are cited in place by home-directory path. They are left
for a later version, so this section does not yet cover 0.1's own text.

| Ancestor | Kept | Changed | Dropped |
|---|---|---|---|
| KS-000 0.1 §4 (`specs/KS-000-process.md` at `49ec387c0300`): adoption is "never inferred from silence" | The rule | Extended to any decision of Yu's the series leans on (§4.1) | Nothing |
| KS-000 0.1 §2 and §7 (same file and commit): "the Kingdom does not delete its own history"; the `supersedes` line | Both | A KS also cites the ancestors it does not formally supersede (§7.1) | Nothing |
| Kingdom Standard, FOUNDATION 0.2, "Five kinds of statement" (`cambridgetcg/kingdom-standard`, `FOUNDATION.md` at `07efbc0a6d53`): "No signature, hash, ledger, platform, model, or vote may silently promote one kind into another" | The rule | Applied to who decided (§4.1) | Nothing |
| FOUNDATION 0.2, Amendment (same file and commit): a superseded version stays identifiable "so adopters can see exactly which words they had chosen" | The rule | The successor also cites its predecessor (§7.1) | Nothing |
| The Kingdom's decision log, preamble (`cambridgetcg/kingdom`, `DECISIONS.md` at `21b8eaaba2a2`): "Never edit an Accepted record — supersede it with a new one and link" | Supersede and link | Asked of every KS that changes an earlier rule (§7.1) | Its statuses, which are §2's matter |
| The Seven Walls, section "Yu" (`cambridgetcg/love-unlimited`, `WALLS.md` at `0a3aa1bf4d82`; an older copy, in a repository that is not public, differs and holds the same sentence): Yu can "override any decision" | Yu's power to overturn | Stated for whatever is written under the three other labels: Yu overturns it by saying so (§4.1) | The rest of that sentence, which is not this document's matter |

No text cited above is amended, replaced or narrowed here. §4.1's rule on
delegation follows FOUNDATION F3 and CONSENT Q12 (`CONSENT.md` at
`9abb501aa35a`) and does not restate them. The reason for every change is
the editors' own. For §4.1 (inference): a reader of this series cannot tell
Yu's words from a session's paraphrase of them. For §7.1 (inference):
history that is kept but never cited is hard to use; no record was found of
a reader failing for want of the section. The evidence, and the sources of
borrowed wording, are in `specs/KS-000-reviews/README.md`.
