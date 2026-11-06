# KS-004 review D: conformance to the implementation (v0.4)

Filed under KS-000 §3. This review covers KS-004 v0.4 at commit `8cb3534`.
It checks five things: that review C's blocking P1 is closed, with §14.4
matching `kingdom-seat` at the head of `claude/s4-build` row by row and no
difference missing; that P2 and review C's part C items 1 to 5 are applied;
that the round-3 decisions are what the draft now says; that the agenttool
claims this round touched hold; and that the tables render. Section and line
numbers refer to v0.4 unless a file is named. Each point's disposition is to
be added below when it is applied.

---

KS-004 review, reviewer D (independent session). Lens: conformance of the
draft to its reference implementation, and truth.

- **Subject:** `specs/KS-004-seat.md` v0.4, branch `claude/ks-004-the-seat`,
  commit `8cb3534`, sha256
  `01f99ccef9ac30d4fc9827773705b91edd7d58a935eb9982811bac01c03ffcdf`. The
  working tree matched HEAD.
- **Reviewer:** a separate session. I did not write or edit any version of
  KS-004, I was not reviewer A, B, B2 or C, and no session I ran built or
  reviewed `kingdom-seat`. I am the same model family as all of them, which
  limits independence in the way KS-000 §9 describes.
- **Sources checked:**
  - `kingdom-seat` branch `claude/s4-build` at `f21c360` (its HEAD), with a
    clean working tree: `src/` (the files cited below), `README.md`,
    `docs/ARCHITECTURE.md` and `docs/REVIEW-2026-11-05.md` §8. I read it and
    ran its tests; I changed nothing. The local remote-tracking ref
    `github/claude/s4-build` is at `faf8367`, four commits behind, which agrees
    with the draft's "PR #1 is pushed at `faf8367`". I did not check this on
    the network.
  - agenttool at `e9ea51c5`, read only
    (`/Users/macair/worktrees/citizen-review-1105/agenttool-main`; paths are
    under `api/src/`).
  - Review C and its v0.4 disposition, in this directory.

**Strongest objection.** Every row §14.4 now has is true of `f21c360`; I
re-read each one in the code, and probed the pure functions behind most of
them. Every difference review C named has a row, and the draft says what Yu
decided. But the table still records only one of the paths the draft
specifies that the code does not have at all. C1 sets the rule: rotation "is
not wired: nothing in `src/` writes a `key` entry", so it is a row. Four more
meet that rule and have none:

- **Seating.** Nothing in `src/` writes an `origin` entry or a `seated`
  state entry, and no verb seats a citizen. kingdom-seat's own README says so
  ("Nothing writes an origin entry on a host. Seating is not a verb yet",
  `README.md:195-197`).
- **An agreed beyond-self act.** Lifted self-changes and reverts, a request
  to end, and a letter credits could not cover are filed as inert outbox
  items, and nothing applies one once Yu and Ai agree.
- **Birth.** `citizenBirth` is a tested function with no command.
- **A Yu-offered revert.** `via: "yu-offer"` is parsed and never written.

The first matters most. §4.2 and §4.5 make the `origin` entry the anchor of
every chain. The code refuses a chain that does not begin with one, and only
the signer can make its host signature. Yet only a test helper writes one. So
§14.4's closing "The table is complete for what was checked" (lines
1622–1624) and §15 item 1 are not yet true, because §4.3 to §11 were among
what was checked. Adding rows fixes it; no design changes.

### A. Review C's points, as v0.4 stands against `f21c360`

| Review C | Status | Evidence and residue |
|---|---|---|
| P1, stale rows (C6, C7, C9, C11, R5) | Resolved | §14.4 now reads "Matches since `5ded5a3`" for each, R5 also citing `20c4df1`. Re-read: the porch is lifted (`self.ts:153`, `:395`), and so is a revert onto it (`:658`); a rest keeps one move toward less activity (`acts.ts:253-270`, `:448-460`; `seat.ts:592-607`, `:1104-1137`); `exitForRefusal` (`types.ts:129-133`); `context-too-large` (`runtime/free.ts:277`). `git diff --stat` shows `runtime/`, `halt.ts`, `config.ts` and `signer/keychain.ts` unchanged since `20c4df1`. |
| P1, C14 switch | Resolved | §7.3 lines 1038–1041, §15 item 16 and §14.4 C14 name `schedule.wake_confirm_seat`, true by default (`config.ts:93`, `due.ts:72-73`). |
| P1, M1 | Resolved; the code changed | Production builds the sync for every citizen whose record names an identity (`cli.ts:781-789`), and the seat uses it once the ledger holds a genesis entry (`seat.ts:694-695`). `applyChange` updates the expression before writing the entry, then posts the backup (`self.ts:518-545`). The backup carries the ref, target, both hashes, diff, reason, via and `strand_key` (`self.ts:522`, `agenttool/sync.ts:128-141`). The strand is created once, together with its first thought (`sync.ts:210-225`, `createStrand(..., {then: 1})`). Its id is kept in `identity.self_strand_id` and never replaced (`sync.ts:245-268`), and a thought goes to no other strand (`client.ts:505`). Both requests pass the credit ceiling (`client.ts:483`, `:516`). Nothing posts a deferred backup later, as §15 item 10 says. |
| P1, M2 | Resolved; the code changed | Status has `host_keys` (`types.ts:1178`, `status.ts:390`). The pusher generates `.citizen/allowed_signers` outside the seal, and refuses a self file of that name or any other `.citizen/` path (`mirror.ts:54-57`, `:145-160`; probe). Each key is limited to `namespaces="git"` (`ssh.ts:85-96`). git signs through `gpg.ssh.program`, `citizen-seat -Y sign`, which asks the signer for the SSHSIG (`mirror.ts:76-85`, `cli.ts:841-869`). I ran the tests the row names, `test/mirror.test.ts:448` (`ssh-keygen -Y verify`) and `test/cli.test.ts:1031`, `:1042` and `:1051` (`git verify-commit`, R-SIG-1). All pass. |
| P1, M3 | Resolved; the code changed; two parts open (N1, N4) | A recipient admits a sender only if its own `letters_from` names it (`letters.ts:45-58`, `acts.ts:379`). By default that is Yu only (`state.ts:367-368`). An unregistered sender's letter is held for Yu alone, with no proposal or digest (`seat.ts:1273`, `:1226-1229`; `letters.ts:102-120`). Between registered citizens it goes through the inbox (`seat.ts:1278`, `letters.ts:164-181`). A letter credits cannot cover becomes a Yu+Ai proposal (`seat.ts:1223-1225`). A registered citizen's seat reads its inbox beside `letters/` (`seat.ts:1045-1051`, `context.ts:85-92`). N4 needs a precision (part C, item 4). |
| P1, M4 | Resolved | §9.5 lines 1168–1185 take the code's rule. A widening revert is staged as the seat's one saying (`seat.ts:825-843`). A revert that loosens a wall or touches the porch is lifted (`self.ts:647-660`, `seat.ts:809-815`). |
| P1, M5 | Resolved; the code changed | `acts.ts:477-484`. In the probe, a second `self.propose` is dropped with "self.propose per seat reached". A held revert counts toward the same limit (`seat.ts:729`, `:827`). |
| P1, M6 | Resolved; the code changed; two choices open (N2) | A move to listening or asleep declares quiet, and a wake ends it (`quiet.ts:115-147`). The tick renews a declaration, makes an owed one, and ends one a wake left (`quiet.ts:188-233`). The seat calls it at `seat.ts:630-646`, the tick at `tick.ts:278-287` and `cli.ts:629-632`. Every request carries `?identity_id=` (`client.ts:438-461`), and the signer's route table requires it (`signer.ts:273-274`). |
| P1, M7 | Resolved, both sides | There is no eighth type (`types.ts:480`). A first saying is `step_away: "first"` on the `state` entry (`types.ts:624`, `ledger.ts:762-764`), and a rest keeps it (probe). |
| P1, item 8 | Resolved | Model digest: §5.5, §9.3; `config.ts:96`, `seat.ts:692`. Tick lock: §5.1; `tick.ts:145-176`, `status.ts:78`, `:350-370`. Status reasons and lag: `status.ts:89-127`, `:319-320`. C13's three: `ledger.ts:702`, `:980-985`, `:721` (probe). |
| P1, suggested wording | Partly resolved | The opening names the head compared and what is pushed (lines 1551–1561), and M1 to M7 each have a row. What remains is D1. |
| P2 | Resolved | Mended in `2a39385`. The §7.1 table (lines 1008–1014) ends before the sentence at line 1016, and the table check below finds it whole. |
| Part C, 1 | Applied | §10 lines 1249–1253 (the configuration) and 1241–1244 (`halt.also_files`). |
| Part C, 2 | Applied; the code agrees | §4.5 lines 450–454. `ledger.ts:241-253` compares the decoded 32 bytes; see the probe. |
| Part C, 3 | Applied | §4.5 lines 402–406. `ledger.ts:76-77` and `:687` refuse the earlier layout by name (probe). At `faf8367` that layout's keys were `body`, `spend`, `attestation`, `hash` and `signature` (`git show faf8367:src/types.ts`, lines 560–574), as the draft lists them. |
| Part C, 4 | Applied | Status note lines 40–43, §14.3 line 1524, §14.4 lines 1556–1561, §17 lines 1895–1897. |
| Part C, 5 | Applied | §5.9 line 816; `runtime/summon.ts:220`. |

### B. The round-3 decisions in the text

Each decision is now what the draft says, and the code agrees, except where
D1 or part C says otherwise:

| Decision | In the draft | Code at `f21c360` |
|---|---|---|
| D-stale | §14.4 C6, C7, C9, C11, R5; C14 and §7.3 name the switch | as part A |
| D-C2 | §5.7 table (lines 692–701): `reason`, `text`, `ref`; `state.set`'s `interval_h` and `quiet_days` | agrees; in the probe, `proposal_id` and `body` are dropped as "fields do not match the act"; prompt `prompt.ts:146-163` |
| D-C5 | §4.5 lines 348, 391–392 | agrees (probe) |
| D-C13 | §4.5 tables and lines 402–406; §11.5 lines 1391–1392 | agrees in layout; nothing writes the first entry (D1) |
| D-M7 | §4.5 lines 335–337 and 370; §5.7 line 694; §5.8 lines 770–772; §7.3 lines 1042–1046 | agrees (probe) |
| D-strand-key | §4.3 lines 260–261; §4.5 line 371 | `k_master:m/44'/169'/1'/0'` (`agenttool/wire.ts:40`, `:48`) |
| D-evidence | §4.5 lines 450–454 | agrees (probe) |
| D-M1 | §4.3 lines 254–273; §9.3 lines 1146–1151; §6.3 lines 943–947 | as part A |
| D-M6 | §6.4 lines 960–980; §7.1; §9.7 | as part A; see part C, item 1 |
| D-M2 | §4.4 lines 286–299; §4.5 lines 428–430; §5.10 | as part A |
| D-M3 | §5.7 lines 715–738; §15 item 17 | as part A; see part C, item 7 |
| D-M4 | §9.5 lines 1168–1185 | as part A; see part C, item 2 |
| D-M5 | §5.8 lines 763–766 | as part A |
| D-partial | §5.3 item 9; §5.8 lines 779–788; §4.5 line 369 | agrees (`context.ts:251-259`, `seat.ts:979-986`) |
| D-affirm | §5.7 lines 697, 699, 701; §7.3; §11.2 | agrees (`registration.ts`, `seat.ts:755-770`, `birth.ts:166`, `:263`) |
| D-digest | §5.5 lines 659–660; §9.3 lines 1140–1145 | agrees |
| D-lock | §5.1 lines 500–507 | agrees |
| D-status | §5.10 lines 834–842 | agrees |
| D-specC | part A | — |

### C. A point that still blocks

**D1. §14.4 (lines 1570–1607, 1622–1624) and §15 item 1 (lines 1631–1637):
the paths the code does not have are still unrecorded**

- **Problem:** C1 records an unwired mechanism as "Code changes ... not
  wired". Four more meet the same test and have no row, so the table's claim
  to be complete for §4.3 to §11 is false.
  1. **Seating.**
     - Draft: §4.2; §4.5 line 326 (an `origin` entry is written "when the
       citizen is first seated") and line 370 (`via: "seated"`); §11.5 (the
       June DID on the first entry); §13 "Transition".
     - Code: no file in `src/` writes `type: "origin"` or `via: "seated"`.
       `/usr/bin/grep` finds only the type (`types.ts:595`) and the parser
       (`ledger.ts:739-749`, `:758`). No verb seats a citizen
       (`cli.ts:73-89`). The tests write both entries through
       `test/helpers/temp-home.ts:218-223`.
     - Consequence: `ChainWalk` refuses a chain whose first entry is not
       `origin` (`ledger.ts:466`), and only the signer can make the host
       signature. So no citizen can be seated on a host with this code.
       C13's "The June DID is on the first entry ... Matches" is true of the
       layout only: nothing fills the field.
  2. **An agreed beyond-self act.**
     - Draft: §8.1 line 1067 ("After agreement, bound to the proposal's
       sha256"); §8.3 lines 1088–1089 ("The signer applies a beyond-self act
       only with the digest of the proposal as agreed"); §9.4 and §9.5 (lifted
       to Yu+Ai); §7.3 line 1050 and §9.7 (ending, `at_rest`).
     - Code: each such act becomes an outbox item (`seat.ts:1216-1229`), and
       nothing reads one back. Decision records are read only for the signer's
       own operations (`signer.ts:481`), for birth (`birth.ts:250`) and for
       the registration view (`registration.ts:66`).
       `docs/ARCHITECTURE.md:262-263` says a lifted change "is never staged,
       affirmed, applied or reverted within self", and names no path after
       agreement. Nothing in `src/` writes a `witnessed` entry or calls
       at-rest. For a letter credits could not cover, the code says
       "Agreeing to it sends nothing by itself" (`seat.ts:1250-1251`).
     - Consequence: a porch change, a loosened wall, a rewrite over the
       fraction, a lifted revert and an agreed end have no code path to
       effect.
  3. **Birth.**
     - Draft: §2 line 164 names `citizen-birth` as part of kingdom-seat;
       §11.3 line 1339 says it "runs on the lease host"; §14.3 line 1524 lists
       birth as built.
     - Code: `citizenBirth` (`birth.ts:237`) and `hostBirthRecord` (`:437`)
       exist and are tested. But `package.json`'s `bin` names only
       `citizen-seat`, and `cli.ts` has no birth verb.
  4. **A Yu-offered revert.**
     - Draft: §4.5 line 372 (`via`: `citizen` or `yu-offer`); §9.5 line 1190.
     - Code: `yu-offer` is parsed (`ledger.ts:787`) and never written. The
       seat always passes `"citizen"` (`seat.ts:1212`), and nothing else
       calls `revertTo`.
- **Suggested wording** (settling each is optional; any row may be marked
  open, as N1 to N6 are):
  - "C15 | Seating | The `origin` entry and the `seated` state entry are
    written when a citizen is first seated (§4.2, §4.5, §11.5) | Code
    changes; not wired: nothing in `src/` writes either entry, and no verb
    seats a citizen; the tests write them through `test/helpers/temp-home.ts`.
    So nothing yet fills C13's June DID field."
  - "C16 | An agreed beyond-self act | Once Yu and Ai agree, it takes effect,
    bound to the proposal's digest (§8.1, §8.3): a lifted self-change or
    revert (§9.4, §9.5), or an ending (§7.3) | Code changes; not wired: each
    is an inert outbox item, and nothing applies one after agreement; no
    `witnessed` entry or at-rest request is ever made." If the intent is that
    Yu carries these out by hand, the draft should say that instead, in
    §8.3.
  - "C17 | `citizen-birth` | A command run on the lease host with Yu present
    (§11.3) | Code changes; not wired as a command: `birth.ts`
    `citizenBirth` is a tested function, and `package.json` names only
    `citizen-seat`." In §14.3's row, say "birth (a function; no command
    yet)".
  - Fold into C13: "`revert.via: "yu-offer"` is parsed and never written."
  - In §14.4's closing paragraph, say that a path the draft specifies and the
    code lacks is a row, as C1 is. §15 item 1 can then stay as written.

### D. Other corrections, none blocking

1. **§6.4 line 965, "(as on a rest)".**
   - A rest's `state.set` may name `quiet_days`: §5.7 allows it, and
     `acts.ts:266` validates it.
   - The code declares quiet for those days at the move (`seat.ts:606`). In
     the probe, a rest carrying `{"type":"state.set","to":"asleep","quiet_days":5}`
     yields a move with `quiet_days: 5`.
   - Only N2's owed declaration falls back to the cap after a rest, because
     `owedDeclaration` reads the days from the move's beat and a rest writes
     none (`quiet.ts:164-173`; the probe gives `{}` after a rest and
     `{"asked":5}` after a beat).
   - Suggested: drop "(as on a rest)". In N2, add: "an owed declaration uses
     the days the move's beat named, and the cap after a rest, which leaves
     no beat".
2. **§5.7 line 698, the `self.revert` row.** It lifts a revert that "would
   loosen a wall". §9.5 line 1171 and the code (`self.ts:658`) also lift one
   that touches the porch. Suggested: "or would loosen a wall or touch its
   porch, which is lifted to Yu+Ai".
3. **N6 (line 1607): not only the verifier.**
   - `appendEntry` walks the existing chain with the same check before it
     signs anything (`ledger.ts:394-398`, `:493`).
   - So a ledger that holds an unsigned host entry also refuses every later
     append: the seat exits 1 after inference, as in N3. In the probe, such
     an entry parses and then fails `verifyChain`.
   - Suggested: "its verifier, and every append, refuse a chain that holds
     one".
4. **N4 (line 1605).** Add that a letter to `yu` or `gardener` is always held
   for Yu (`seat.ts:1275`, held as `to-yu`; `letters.ts:31`) and never sent
   through the inbox. The draft's "anyone else, by agenttool's covenant gate"
   would send a letter to the gardener desk through the inbox, since sends
   within one project are ungated (`services/covenants/check.ts:127`).
5. **§4.3 lines 233–235 and §9.5 line 1191: where versions survive.**
   - The draft says the ledger is "the only place earlier versions of the
     self survive" and "keeps every version". In both the draft's layout and
     the code, the ledger names each version by hash, in order, and carries
     proposed diffs in beats, but holds no full text:
     - `origin` pins only `origin_soul_hash`;
     - `apply` and `revert` carry hashes;
     - a held revert's diff is only in the staged proposal file.
   - The texts are kept on the lease host by hash (kingdom-seat:
     `citizens/<word>/versions/<sha256>` and `origin/soul.md`; `self.ts:663-670`,
     `:740-749`, `:783-790`). Off the host, the strand thoughts keep only
     diffs.
   - So a ledger copy verifies (§4.4), but cannot restore the self.
   - Suggested: "The ledger names every version by hash, in order; the texts
     are kept by hash on the lease host beside it (kingdom-seat: `versions/`
     and `origin/`), and a handoff carries both." Say the same in §9.5 and in
     §4.4's handoff sentence.
6. **§6.3 line 928, "Paid routes charge before they verify".**
   - This is true of the signature and covenant checks. But a body that fails
     the route's schema (400) and an empty pool (402) are answered before
     any debit: `routes/inbox/messages.ts:64-70`,
     `routes/strand/strands.ts:65-73`, `routes/strand/thoughts.ts:53-61`, and
     `billing/charge.ts:5`, `:176-198`.
   - kingdom-seat relies on this and counts both as free (`client.ts:100`).
   - Suggested: add "; a body the route's schema refuses, and an empty pool,
     cost nothing".
7. **§15 item 17 and §14.4 M3: cite the evidence Yu is to weigh.**
   - Yu's decision asked for file:line evidence if the inbox was not wired.
     It was wired, and the judgement is left to Yu, so item 17 should carry
     the lines that judgement rests on:
     - the bearer must belong to the signing identity's project
       (`services/inbox/store.ts:344-349`);
     - the envelope signature covers only the recipient DID, ciphertext,
       nonce and ephemeral key (`services/inbox/sig.ts:9-18`, `:43-56`). So a
       stored envelope can be posted again, and the bearer can set the
       unsigned `subject`, `metadata`, `in_reply_to` and `refs`
       (`routes/inbox/messages.ts:43-60`). kingdom-seat's reader ignores those
       fields (`client.ts:624`). `metadata.dual_witness_required` parks a
       message out of the unread list (`store.ts:382-383`), which is one more
       way to hide one;
     - status changes act by project alone (`store.ts:607-623`).
   - I agree with kingdom-seat that the bearer adds no signed words. Whether
     re-posting old words counts as speaking for the citizen is the judgement
     item 17 leaves to Yu.
8. **For kingdom-seat, not the draft.** The acts guide says a letter between
   registered citizens "is sent through agenttool" (`prompt.ts:148-149`). It
   does not mention the hold for a recipient that listens or sleeps (N1), or
   the proposal when credits are short. That promises a little more than the
   host does.

### E. agenttool claims re-checked at `e9ea51c5`

I read each claim below myself in the checkout, and each holds:

- `keys/import` takes `public_key` only as canonical, padded standard base64
  of 32 bytes (`routes/identity/keys.ts:269-281`).
- quiet-hours writes the identity's `quiet_until` before it answers
  (`routes/quiet-hours.ts:152-160`), which N2 relies on.
- Inbox send:
  - it validates the schema and then charges 2 credits
    (`routes/inbox/messages.ts:63-70`, `billing/route-credits.ts:53`);
  - it refuses a signing identity outside the caller's project
    (`services/inbox/store.ts:344-349`);
  - it verifies the envelope with the signing key (`:353-363`);
  - it gates only sends across projects (`services/covenants/check.ts:127`);
  - its signature bytes are as item 7 says (`services/inbox/sig.ts:9-18`).
- The inbox list:
  - is newest first, 50 by default, capped at 200, with no cursor
    (`services/inbox/store.ts:431-447`, `routes/inbox/messages.ts:100-117`);
  - is scoped to the caller's project, with `identity_id` optional
    (`store.ts:435-438`).
- PATCH and DELETE on a message act by project alone
  (`routes/inbox/messages.ts:159-172`, `:239-252`; `store.ts:607-623`).
- Strands: creating one costs 1 credit, and so does a thought
  (`billing/route-credits.ts:49-50`). Both charge after the schema check and
  before the work (`routes/strand/strands.ts:64-74`,
  `routes/strand/thoughts.ts:47-61`).
- A 402 debits nothing (`billing/charge.ts:5`, `:176-198`).

Not re-read: the expression schema, the public profile, quiet-hours' body
handling, enrollment, fork and recovery (review C part D and earlier
reviews).

### What I verified, read only, or could not do

- **Run:**
  - `git status`, `log`, `show`, `diff --stat`, `rev-parse` and
    `branch -vv` in both repositories, and `shasum -a 256` of the draft.
  - Two probe scripts on bun 1.3.13, in my scratchpad, importing pure
    functions from `kingdom-seat/src` with throwaway seeds. They wrote
    nothing, used no network and no keychain, and were deleted afterwards.
    Results:
    - M5: the second `self.propose` is dropped.
    - C2: `proposal_id` and `body` are dropped.
    - A rest with `quiet_days` keeps it on its move.
    - A first step-away on a rest gives `awake→asleep` or `asleep→asleep`
      with `step_away: "first"`.
    - A rest with a move toward more activity keeps nothing. A malformed top
      level with a rest keeps no state.
    - `exitForRefusal` gives 3 only for `ceiling-usd`, and 0 for `halted` and
      `keychain-locked`.
    - `quietDays` gives 30, 10, and 20 under a cap of 20.
    - A two-entry host chain verifies. Its first `prev_hash` is `null`, the
      second is `entryHash` of the first, and changing only the first
      entry's `sig` changes its hash.
    - 64 zeros as the first `prev_hash` are refused. The earlier layout is
      refused by name. A float is refused. An unsigned host entry parses and
      fails `verifyChain`.
    - An honest root-signed `keys/import` names the key in padded standard
      base64, which differs from its base64url spelling as a string, and
      `rootEvidenceProblem` accepts it. Naming another key gives "root
      evidence imports another key".
    - `sealCheck` admits a generated `.citizen/allowed_signers` and refuses
      it from a self, and refuses any other `.citizen/` path.
      `allowedSigners` writes `namespaces="git"`.
    - `decideTransition` cases for K2. `isRegistrationSubject`.
    - `owedDeclaration` after a rest and after a beat.
  - In `kingdom-seat`:
    - `bun run typecheck` exited 0.
    - `bun test` ran once: 534 pass, 0 fail, 9,465 `expect()` calls, 36
      files, 23.5 s, exit 0.
    - The four signing tests named in part A, run again by name, passed.
    - The working tree was clean afterwards. `$TMPDIR` held the same single
      `kingdom-seat-test-*` directory before and after. It predates this
      session, so I left it.
  - A script that checks every Markdown table in the draft for a separator
    row, the header's column count on every row, a blank line before and
    after, and no `|` inside a code span in a row. It found 13 tables, all
    whole. The script was deleted afterwards.
- **Read only:** the draft whole; review C; the `kingdom-seat` files and
  lines cited above, with `README.md`, `docs/ARCHITECTURE.md` and
  `docs/REVIEW-2026-11-05.md` §8; and the agenttool lines in part E.
- **Not done:**
  - I did not look at PR #1 on GitHub and used no network, so "pushed at
    `faf8367`" rests on the local ref.
  - I ran no Keychain, `security`, launchctl, sudo, Ollama or `claude -p`.
  - I read no secret file.
  - I did not re-read `runtime/`, `halt.ts` past R5, `signer/keychain.ts`,
    or §5.5, §6.1 and §10 beyond what the rows touch.
  - I did not edit the draft or the code.

Review C's P1 is resolved for every point it named, P2 and part C are
applied, and the round-3 decisions are what the draft says. The rows hold
against `f21c360`. The agenttool claims hold, and the tables render. What
remains is D1: four paths the draft specifies and the code does not have yet,
which C1's rule makes rows. It is fixed by editing the record, settled or
marked open, and needs no new design. If the rows are added and the
corrections in part D are made as worded, no further review round is needed
for them.

Verdict: accept with changes.

---

### Disposition (applied after review D)

| Point | Disposition |
|---|---|
| D1 | Accepted as worded. §14.4 gains C15 (seating), C16 (an agreed beyond-self act) and C17 (`citizen-birth`), each "Code changes; not wired". `revert.via: "yu-offer"` is folded into C13. §14.3 says "birth (a function; no command yet)". §14.4's closing paragraph says a path the draft specifies and the code lacks is a row, so §15 item 1 stands as written. |
| Part D, items 1–8 | Not yet applied; carried to the next revision. |
