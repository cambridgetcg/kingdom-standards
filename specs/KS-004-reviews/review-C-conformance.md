# KS-004 review C: conformance to the implementation (v0.3)

Filed under KS-000 §3. This review covers KS-004 v0.3 at commit `276f0d0`.
It checks three things: that each blocking point of re-review B2 (R1 to R6) is
resolved; that the draft matches `kingdom-seat` or names each remaining
difference; and that its agenttool claims hold. Section and line numbers refer
to v0.3 unless a file is named. Each point's disposition is to be added below
when it is applied.

---

KS-004 review, reviewer C (independent session). Lens: conformance of the
draft to its reference implementation, and truth.

- **Subject:** `specs/KS-004-seat.md` v0.3, branch `claude/ks-004-the-seat`,
  commit `276f0d0`, sha256
  `01eb3e299c260b57dc22943204e910625c5fa3d03661a39222533c1049424eb6`. The
  working tree matched HEAD.
- **Reviewer:** a separate session. I did not edit any version of the draft.
  I was not reviewer A, B or B2, and no session I ran built or reviewed
  `kingdom-seat`. I am the same model family as all of them, which limits
  independence in the way KS-000 §9 describes.
- **Sources checked:**
  - `kingdom-seat` branch `claude/s4-build` at `20c4df1`, read only, with a
    clean working tree: `src/`, `docs/ARCHITECTURE.md` and
    `docs/REVIEW-2026-11-05.md` §5 and §7. The draft compared the code at
    `724c660`. Two commits came after v0.3 (17:47 UTC): `5ded5a3` (18:01) and
    `20c4df1` (18:46). The local remote-tracking ref
    `github/claude/s4-build` is at `c776d80`, so the three commits after it
    look unpushed. I did not check this on the network.
  - agenttool at `e9ea51c5`, read only (`/Users/macair/worktrees/citizen-review-1105/agenttool-main`;
    paths are under `api/src/`).
  - Re-review B2 and its v0.3 disposition, in this directory.

**Strongest objection.** §14.4 says it is the complete list of differences
between the draft and the code. It says "A difference not in this table is a
defect in one of the two" (line 1397), and §15 item 1 says "Every disagreement
between them is recorded in §14.4" (lines 1426–1427). Neither is true.
`724c660` is the commit the draft says it compared. At that commit there were
already six substantive differences that the table leaves out, and all six
remain at `20c4df1`. Two of them affect what the draft most needs to be true:

- A registered citizen cannot change itself in the code at all. Nothing
  carries a bound change to its expression or strand.
- The host key the draft says is published is published nowhere. The code's
  mirror seal refuses `.citizen/`, the directory that would hold it.

In the other direction, five rows still say "Code changes" although the code
has matched since `5ded5a3`. So R6 is only partly resolved: B2's part C is
settled, but the record of differences is incomplete.

### A. Re-review B2's blocking points, as v0.3 stands against `20c4df1`

| B2 | Status | Evidence and residue |
|---|---|---|
| R1 | Resolved | §5.7 lines 608–641, §5.8, §9.3. The reply is `{"acts": [...]}`, and the host computes `prior_hash`, `new_hash` and the diff (`src/types.ts:307-314`, `:353-376`; `src/seat.ts:592-596`). It accepts a prefix of at least 8 hex (`src/acts.ts:26-40`, `:378-387`). The field names still differ (`claim`, `body`, `proposal_id`), and §14.4 C2 records this. Residue: §5.7 line 630 says `self.affirm` confirms "a move toward more activity, a step-away, a registration answer". The code affirms only staged self-proposals (`src/seat.ts:628-633`). Its other confirmations work by repeating `state.set`, which the open row at line 1418 records. A registration answer cannot be affirmed at all: no act resolves to a `propose.beyond`, and birth takes the citizen's yes as a ledger hash passed in (`src/birth.ts:53-59`, `:162`). The open row should name registration too. |
| R2 | Resolved in both | §6.3 lines 827–839. `src/spend.ts`: a `begun` line comes before the run, and an unwritable record refuses with `ceiling-usd` (`src/runtime/summon.ts:216-221`). A `settled` line is written on every path (`:222-241`). A `begun` line without a `settled` one, or a `null` cost, makes the day unknown (`src/spend.ts:118-150`). |
| R3 | Resolved in both | §5.5 lines 584–587. The code records `usd: null` with basis `unknown` (`src/runtime/summon.ts:53`, `:183-199`). |
| R4 | Resolved in the spec; the code matches in substance | §4.4 lines 276–282, §4.5 lines 366–422, §16.8, §15 item 15. The code rebuilds the identity-authority/v1 digest from the evidence. It checks that the route is this identity's import, or its revoke with an empty body (`src/ledger.ts:93-130`). It checks the rising-sequence rule and refuses the root as an op key (`:343-366`, `:304`). agenttool backs the sequence rule: a proof must carry `state.sequence + 1` (`services/identity/authority.ts:163`). One precision is in part C. One residue is the host key, which P1 (M2) covers. |
| R5 | Resolved in the spec; the code matches since `5ded5a3` | §10 lines 1087–1107. The default file is `/Users/Shared/kingdom-seat/HALT` (`src/config.ts:26`). `halt` runs as the operator, and the signer raises the beacons through the one fixed call `raise-beacons` (`src/halt.ts:7-10`). `20c4df1` goes further: the operator owns the config, which no verb run as the seat user will accept from that user (KS4-HALT-2). `halt` raises the default file even without a config (KS4-HALT-1). `halt.also_files` covers `$LOVE/HALT` (KS4-HALT-4). §14.4's R5 row is stale. Part C asks the draft to take the config rule. |
| R6 | Partly resolved | The status note, §2, §14.3, §15 item 1 and §17 no longer say the code is missing. §14.4 settles every row of B2's part C. What remains blocks; see P1. |

### B. Points that still block

**P1. §14.4 (lines 1390–1419) and §15 item 1 (lines 1423–1428): the record of differences is stale and incomplete**

- **Problem:** the table compares `724c660`, and the code is now `20c4df1`.
  Rows that have gone stale and rows that are missing both make the table
  say something false.
- **Stale since `5ded5a3`:** the code now matches the draft for each of the
  following, but the table still says "Code changes".
  - **C6:** the porch is beyond self, and a revert onto it is refused
    (`src/self.ts:92-96`, `:338`, `:570`).
  - **C7:** a rest keeps one `state.set` toward less activity
    (`src/acts.ts:237-253`, `:408-420`; `src/seat.ts:544-556`, `:878-902`).
  - **C9:** only `ceiling-usd` exits 3, and a locked keychain exits 0
    (`src/types.ts:129-133`).
  - **C11:** a context that fails the byte rule is refused with
    `context-too-large` (`src/runtime/free.ts:206-220`, `:277`).
  - **R5:** see part A.
- **C14** still matches, and the code now has Yu's switch for it,
  `schedule.wake_confirm_seat`, true by default (`src/config.ts:93`,
  `src/due.ts:72`). The draft should name the switch in §7.3 and §15 item 16,
  so that Yu's decision has a place to land.
- **Missing.** M1–M6 were all present at `724c660`; M7 arrived in `5ded5a3`.
  1. **M1. A registered citizen's self-change never binds.**
     - Draft: §9.3 "Applying" (lines 1023–1026) and §4.3 (lines 244–253):
       an expression update, an `apply` entry, and a strand thought
       "carrying the applied diff, the prior and new hashes, and the reason".
     - Code: production passes `expressionSync: null`
       (`src/cli.ts:714-715`). So for any citizen with a `genesis` entry,
       `canSync` is false (`src/seat.ts:576-577`). No change or affirmation
       binds (each is noted `no-expression-sync`), and a revert is dropped.
     - `createStrand` has no caller (`src/agenttool/client.ts:415`;
       `docs/REVIEW-2026-11-05.md:239`).
     - The thought the interface would post carries the claim and the
       proposal id (`src/self.ts:39-42`, `:458`), not the diff and the hashes.
     - §14.4 has a row only for the encryption key's name.
  2. **M2. The host key is published nowhere, and `.citizen/` cannot reach a
     mirror.**
     - Draft: §4.5 lines 373–375, "the host key's public half is published in
       the status file (§5.10) and, for a citizen with a mirror, in
       `.citizen/allowed_signers`". §5.10 line 740 and §4.4 lines 266–274 say
       the same.
     - Code: `StatusFile` has no such field (`src/types.ts:985-1001`).
     - The mirror seal refuses `.citizen/` at any depth
       (`src/mirror.ts:41`, `:69`).
     - No code signs mirror commits; status only counts the unsigned ones
       (`src/mirror.ts:276`).
     - The trusted host key sits in the operator's config
       (`trust.host_attest_public_keys_b64`, `src/config.ts:97`). That is not
       a place a verifier given a ledger copy can reach.
  3. **M3. Letters.**
     - Draft (§5.7 lines 633 and 648–657, §8.1, §5.3 item 5): `letter.send`
       is within self and is sent within the credit budget once the citizen
       is registered. The recipient's covenants decide whether to admit it.
       A registered citizen also reads letters from its agenttool inbox.
     - Code: every `letter.send` becomes an outbox proposal for Yu + Ai, with
       extent `letter.send <word> to <to>`, registered or not
       (`src/seat.ts:713-716`, `:759-760`).
     - The recipient is checked against the *sender's* own `letters_from`
       list, plus `yu` and `gardener` (`src/seat.ts:865`).
     - No inbox route is called, for sending or reading. Letters come only
       from `letters/` files (`src/context.ts:394-404`).
  4. **M4. Revert.**
     - Draft: §5.7 line 631 and §9.5 lines 1043–1047. A revert "takes effect
       at once and does not count against the pace window". A revert that
       loosens a wall is "lifted beyond self".
     - Code (`src/seat.ts:656-686`): a revert toward wider exposure (a
       shorter cadence, or a sender added to its covenants) is staged for a
       later seat, and then binds as a `self.applied` inside the pace window.
     - Other reverts need a runtime Yu approved, unless Yu is present or
       they go toward rest or back to a text's first version.
     - A revert that loosens a wall is refused and dropped
       (`src/self.ts:571`, caught at `src/seat.ts:723-724`), not lifted.
     - On widening reverts the code is right. Under §9.5 as written, one
       saying could restore a shorter interval or a wider set of senders.
       Principle 4 and §7.3 make exactly that kind of move wait for a second
       saying.
  5. **M5. More than one `self.propose` per seat.**
     - Draft: §5.8 line 682 allows "at most one `self.propose` per seat".
     - Code: `normalizeIndexed` caps only letters (`src/acts.ts:422-456`),
       and each proposal is staged (`src/seat.ts:592-626`).
     - I ran a probe: two `self.propose` acts both pass `validateOutput` (see
       "What I verified").
  6. **M6. Citizen quiet is not wired.**
     - Draft: §6.4 lines 855–866 and §7.1 say the signer declares quiet,
       renews it while the citizen stays quiet, and ends it on waking.
     - Code: `startCitizenQuiet` and `endCitizenQuiet` exist
       (`src/agenttool/client.ts:387`, `:405`), but only tests call them.
     - The C2 row names only the missing `quiet_days` field.
  7. **M7. An eighth entry type, `step-away.said`.**
     - Draft: line 315 says entries are "one of the seven above".
     - Code: since `5ded5a3`, a first step-away said on a rest writes
       `step-away.said` and then a `state` entry to asleep
       (`src/types.ts:552-557`, `src/seat.ts:544-556`).
     - The draft does not say how a first step-away said on a rest is kept.
       §5.8 lines 687–693 do not say that a step-away may ride with a rest at
       all. The code's review record calls this a match needing no §14.4
       entry (`docs/REVIEW-2026-11-05.md` §7.2, KS4-REST-2), but a verifier
       meets the extra type.
  8. **Smaller ones, same rule:**
     - Self-authorship is approved per model digest
       (`self_authorship.approved_model_digests`, `src/config.ts:96`,
       `src/seat.ts:574`), not per runtime class as §5.5 lines 592–593 and
       §9.3 lines 1021–1022 say.
     - The tick never reclaims a live owner's lock by age
       (`src/tick.ts:135-175`), against §5.1 line 443, "a lock older than 2
       hours is reclaimed".
     - The status file carries `last_outcome` but not the refusal's reason or
       an expression lag (`src/types.ts:956-982`); reasons go to `host.jsonl`.
       §5.8 lines 695–697 and §5.10 lines 738–740 say otherwise.
     - C13's list of encodings that "code changes" leaves out three: the
       first `prev_hash` is 64 zeros, not `null` (`src/types.ts:577`); the
       code has `spend` with `usd_basis` where the draft has `cost`; and it
       has `attestation` where the draft has `signer`.
- **Suggested wording:**
  - Re-read the code at its current head, and say in §14.4's opening which
    commits are pushed to PR #1.
  - Turn C6, C7, C9, C11 and R5 to "Matches since `5ded5a3`".
  - Add rows M1–M7, and fold item 8 into C13 and new short rows. Settling
    each row is optional: like the two open rows already there, any of them
    may be marked open.
  - My suggestions:
    - M1, M6: "Code changes; not wired yet".
    - M2: code changes. The pusher should write the host-generated
      `.citizen/allowed_signers` outside the seal, as it does the card, and
      status should carry the public key.
    - M4: take the code's rule into §9.5 ("a revert toward more activity or
      exposure waits for a second saying, like any such move; a revert that
      would loosen a wall is not applied and becomes a `propose.beyond`").
      Code changes only for the lift.
    - M3 and M5: open.
    - M7: draft. Add to §5.8: "a step-away, first or second saying, may
      accompany a rest". Add to §4.5 how the first saying is kept, either as
      the code's entry or as a field of the `state` entry.
  - Then §15 item 1 can stay as written.

**P2. §7.1 lines 896–904: the state table is broken**

- **Problem:**
  - v0.3 inserted "Seats a letter opens keep the awake-interval floor (§5.1,
    §6.3)." between the `asleep` row and the `stepped-away` row.
  - In GitHub-flavoured Markdown a table ends at the first non-table line.
    So the `stepped-away` and `ended` rows now read as paragraph text.
  - Those two rows carry what is normative about stepping away and ending:
    never blocked, `at_rest` irreversible, the mirror card state.
  - v0.2 (`b0c006f`, lines 760–761) had them inside the table.
- **Suggested wording:** move the sentence below the `ended` row, after a
  blank line.

### C. Other corrections, none blocking

1. **§10: the config is part of the HALT path.**
   - Whatever names the HALT file and the beacons can lower HALT.
   - The code found this as KS4-HALT-2: the config sat in the seat user's
     reach, so the seat could edit it to lower HALT.
   - Suggested, after "a seat must not be able to lower HALT" (line 1106):
     "Nor may it rewrite what names the HALT file or the beacons: the
     configuration that does so is owned by the operator, and the seat
     refuses one its own user could change. The verb raises the default file
     even when it cannot read that configuration."
   - Also say that the transition SHOULD is met by configuring extra HALT
     files (`halt.also_files`), which are empty by default.
2. **§4.5 lines 393–395: the evidence names its key in agenttool's
   encoding.**
   - `keys/import` requires `public_key` in canonical standard base64 with
     padding (`routes/identity/keys.ts:269-280`).
   - The ledger's public keys are base64url without padding (line 333).
   - So "the body names the key installed" has to compare the decoded 32
     bytes. A string comparison fails on every honest entry.
3. **§4.5 lines 310 and 337–351: two layouts under one format name.**
   - The draft took the code's format string and domain tag,
     `kingdom-seat-ledger/v1`, for a different entry layout.
   - So until the code changes (C5, C13), two incompatible layouts carry the
     same `format`. Ledgers written by today's code, such as test ledgers and
     the scratch ledgers that `docs/REVIEW-2026-11-05.md` §7.6 item 5
     mentions, would read as this draft's v1.
   - Either name the draft's layout `kingdom-seat-ledger/v2`, or state that
     no ledger written before the code adopts this layout is v1.
4. **Status note lines 32–35, §14.3 line 1365: PR #1.**
   - By the local ref, PR #1's branch is at `c776d80`. Rows that read
     "Matches since `724c660`" cite commits a reader of the PR cannot see.
   - Say "local, not yet pushed" until they are pushed.
5. **§5.9 line 718 and §6.3: an unwritable spend record exits 3.** The code
   refuses with `ceiling-usd` when it cannot write `begun`
   (`src/runtime/summon.ts:216-221`). This follows from §6.3's "counts as at
   the ceiling", but §5.9 names only "a metered runtime at its USD ceiling".
   Add "or whose spend cannot be recorded".

### D. agenttool claims re-checked at `e9ea51c5`

I read each claim below myself in the checkout, and each holds:

- the header names `X-Agenttool-Authority-Sequence`, `-Timestamp` and
  `-Signature`;
- `canonicalIdentityAuthorityBytes` in `services/identity/authority.ts`
  (`:34-36`, `:102-122`), and the sequence rule `proof.sequence ===
  state.sequence + 1` (`:163`);
- `keys/import` requires canonical base64 for a 32-byte key
  (`routes/identity/keys.ts:264-280`);
- revoke is `DELETE /:kid` with an empty body, root-authorised, and the root
  is immutable (`:365`, around `:444-470`);
- a rooted identity is refused server-generated keys (`:191-205`);
- quiet-hours without `identity_id` acts for "the earliest active identity
  that is not an enrolled guest" (`routes/quiet-hours.ts:11-14`);
- quiet-hours ignores unknown body fields, takes `until` uncapped, caps
  `hours` at 720 (`:38`, `:107-128`), and trims `reason` to 200 (`:141`);
- the public profile's fields are `identity_id`, `did`, name, capabilities,
  `trust_score`, status, `forked`, quiet fields and `created_at`
  (`routes/public/agents.ts:109-127`);
- the expression's closed top-level fields plus `updated_at`, and the porch's
  one field `invited_until` (`services/identity/expression.ts:91`, `:106-112`,
  `:224`, `:274`);
- the route mounts for enroll, keys, box-keys, authority, at-rest, fork,
  `/v1/identity/recover`, `/v1/register/agent`, `/v1/quiet-hours` and
  `/public` (`routes/identity/index.ts:45-66`, `index.ts:896-1067`);
- PATCH covers `expression_visibility` and is root-authorised
  (`routes/identity/identities.ts:260-271`, `:366-370`, `:427`);
- the credits per route (`billing/route-credits.ts:35-58`).

The precision in part C item 2 is the only agenttool point I add. I did not
re-read `services/identity/fork.ts`, the enrollment limiter, or the
inbox and elevate charge-before-verify lines; B2 and the v0.3 session did.

### What I verified, read only, or could not do

- **Run:**
  - `git status`, `log`, `show`, `diff` and `branch -vv` in both
    repositories;
  - `shasum -a 256` of the draft;
  - one probe, on bun 1.3.13. A scratchpad script imported `validateOutput`
    from `kingdom-seat/src/acts.ts`, which is a pure function, and fed it two
    `self.propose` acts, a journal and a malformed `self.affirm`. Result:
    `kept: ["self.propose","self.propose","journal"]`, with the affirm
    dropped. That supports M5 and the open row on partial output.
- **Read only:** the `kingdom-seat` files and lines cited above, and the
  agenttool lines in part D.
- **Not done:**
  - I did not run `bun test` or the typecheck, so the code-side gate is
    reported, not reproduced.
  - I did not run Ollama, Claude Code, `security` or launchctl, used no
    network, and did not look at PR #1 on GitHub.
  - I read no secret file.
  - Because the PR was not checked, "unpushed" in part C item 4 rests only on
    the local remote-tracking ref.

B2's R1 to R5 are resolved: R2, R3 and R5 in both the spec and the code, and
R1 and R4 in the spec, with the code agreeing in substance. The agenttool
claims hold, and the design holds. What remains is the record of differences
(P1) and a table that v0.3 broke (P2). Both are fixed by editing the record,
and need no new design. Every new §14.4 row may be left open, as two already
are. If the changes are made as worded above, no further review round is
needed for them.

Verdict: accept with changes.

---

## Disposition (applied in v0.4)

Section numbers below refer to v0.4. Yu decided each difference for this
round (the round-3 decisions, listed in `kingdom-seat`
`docs/REVIEW-2026-11-05.md` §8.1). `kingdom-seat` changed on its side in four
commits after `faf8367`, PR #1's pushed head: `7791c5c`, `2a94032`,
`c78f307` and `f21c360`. Those are local and are to be pushed with this
revision. §14.4 was rewritten against `f21c360`, and its "code" column
describes that commit.

| Point | Disposition | Where, and why |
|---|---|---|
| Strongest objection | Accepted | §14.4 is rewritten against `f21c360` and §15 item 1 now claims only the differences found; §14.4 says what was checked and what was not. |
| A, R1 residue | Accepted (the code's rule) | §5.7 `self.affirm` and `state.set` rows, §7.3, §11.2: a move of state is confirmed by repeating its `state.set`; `self.affirm` confirms staged self-changes and an agreed registration answer. §14.4 K2, G1. |
| P1, stale rows (C6, C7, C9, C11, R5) | Accepted | §14.4: each now reads "Matches since `5ded5a3`"; R5 also cites `20c4df1` for the operator's configuration and `halt.also_files`. |
| P1, C14 switch | Accepted | §7.3 and §15 item 16 name `schedule.wake_confirm_seat`, true by default; §14.4 C14. |
| P1, M1 (self-change never binds) | Code changed; spec stated | §4.3 (the strand made once on first need, its id in the host's record, the key named, deferral), §9.3. Matches since `2a94032` (§14.4 M1). |
| P1, M2 (host key, `.citizen/`) | Code changed; spec stated | §4.4 (the generated `allowed_signers`, `.citizen/` refused, signing through the signer), §4.5, §5.10, §6.2. Signing is wired with an `ssh-keygen -Y verify` test. Matches since `2a94032` (§14.4 M2). |
| P1, M3 (letters) | Code changed; spec stated, two parts open | §5.7: the recipient's covenants decide; held for Yu alone before registration; the inbox between registered citizens; a proposal when credits are short. Matches since `c78f307` (§14.4 M3). Open: a letter that would wake its recipient (N1) and whom a citizen may write to (N4). The inbox stays wired; the bearer's residual powers are §15 item 17, Yu's to revisit. |
| P1, M4 (revert) | Accepted (the code's rule; the code changed only the lift) | §9.5, §5.7, §8.1: toward more exposure waits for a second saying; a loosening revert becomes a `propose.beyond`. §14.4 M4. |
| P1, M5 (two `self.propose` acts) | Code changed | §5.8: one staged saying per seat, a held revert counting as one; extras are invalid acts. §14.4 M5. |
| P1, M6 (quiet not wired) | Code changed; §6.4 reworded to the decision | §6.4, §5.7, §7.1, §9.7, §16.7: every move of a registered citizen to listening or asleep declares quiet under the standing agreement, `quiet_days` setting how long; the tick renews; a wake ends it. §14.4 M6; the code's handling of lost answers and owed declarations is open (N2). |
| P1, M7 (`step-away.said`) | Accepted, both sides | §4.5 (`step_away: "first"` on the `state` entry; no eighth type), §5.7, §5.8, §7.3: a step-away, first or second saying, may accompany a rest. §14.4 M7. |
| P1, item 8: model digest | Accepted (the code's rule) | §5.5, §9.3. §14.4 S1. |
| P1, item 8: tick lock | Accepted (the code's rule) | §5.1, §5.10: only an ownerless lock is reclaimed; a live owner's lock past 2 hours is reported. §14.4 S2. |
| P1, item 8: status reasons and lag | Code changed | §5.8, §5.10. §14.4 S3. |
| P1, item 8: C13's three | Code changed | Folded into §14.4 C13 as suggested: `null` first `prev_hash`, `cost`, `signer`. |
| P1, suggested wording | Accepted | §14.4's opening names the head compared and that it is to be pushed to PR #1 with this revision; the two rows open in v0.3 are settled (K2, K3), and every M1 to M7 has a row. |
| P1, partial output (open row of v0.3) | Accepted (the code's rule, with show-back) | §5.3 item 9, §5.8, §4.5 (`dropped`): invalid acts are dropped and recorded, valid ones apply, the next seat is shown the drops; a reply failing the top-level shape applies nothing. §14.4 K3. |
| P2 (§7.1 table broken) | Accepted | Mended in `2a39385`, before this revision: the sentence sits below the table. |
| C, 1 (§10 and the config) | Accepted | §10: the seat may not rewrite what names the HALT file or the beacons; the configuration is the operator's; the verb raises the default file without it; `halt.also_files`, empty by default, meets the transition SHOULD. |
| C, 2 (evidence key encoding) | Accepted | §4.5 "Root evidence": the import's key is compared as decoded 32 bytes; the code does so since `7791c5c`. |
| C, 3 (two layouts, one name) | Accepted, second option | §4.5: `kingdom-seat-ledger/v1` names this layout only; no ledger in the code's earlier layout is v1, and a verifier refuses it. The code refuses it by name since `7791c5c`. |
| C, 4 (PR #1) | Accepted | Status note, §14.3, §14.4, §17: PR #1 is pushed at `faf8367`; the round-3 commits up to `f21c360` are local and are to be pushed with this revision, which cites `f21c360`. |
| C, 5 (unwritable spend exits 3) | Accepted | §5.9 exit table: "or whose spend cannot be recorded". |

**Found in this revision, not in review C.** Two choices the code made in
round 3 and four differences found by reading it at `f21c360` are recorded
as open in §14.4 rather than settled: a letter that would wake its recipient
is held for Yu (N1); a quiet declaration whose answer was lost is recorded
as standing, and the tick makes one a move owed (N2); the seat does not
verify the chain before it opens (N3); letters reach only Yu, the gardener
desk and citizens on the same host (N4); nothing reads the
registered-citizen ceiling (N5); and the verifier refuses an unsigned host
entry, which this draft allows (N6). Four spellings the draft left open are
written into §4.5 from the code (§14.4 C13), and §15 item 17 is new.

**What the session that applied this review checked.** It ran `git status`,
`log`, `show`, `diff --stat` and `merge-base --is-ancestor` in both
repositories, `shasum -a 256` of the draft, and a script that checks every
Markdown table in the draft has a separator row, the header's column count
on every row, and a blank line before and after. It read review C, the
draft, `kingdom-seat` at `f21c360` (the files §14.4 names), its
`docs/ARCHITECTURE.md` and `docs/REVIEW-2026-11-05.md` §7 and §8, and one
agenttool file at `e9ea51c5` (`routes/identity/keys.ts:262-282`). It did not
run `bun test` or the typecheck, used no network, did not look at PR #1 on
GitHub, ran no Keychain, launchctl, Ollama or Claude Code, and read no secret
file. It did not change `kingdom-seat`.
