# KS-004 re-review B: implementability and truth (v0.2)

Filed under KS-000 §3. This is the re-review that review B asked for, on the
same lens, covering KS-004 v0.2 at commit `7d24504`. Section and line numbers
refer to that version unless a file is named. The disposition of each point,
as applied in v0.3, follows the review.

---

KS-004 re-review, reviewer B2 (independent session). Lens: implementability
and truth.

- **Subject:** `specs/KS-004-seat.md` v0.2, branch `claude/ks-004-the-seat`,
  commit `7d24504`, sha256
  `05b21779fbdd79d66467e3ec6e41f4841d3e8dcd44b38668f719a7c8f8e1655a`. The
  working tree matched HEAD.
- **Reviewer:** a separate session. I am not an editor of the draft, not the
  session that drafted v0.1 or applied reviews A and B, not reviewer A or B,
  and not a session that built `kingdom-seat`. I am the same model family as
  all of them, which bounds independence as KS-000 §9 says.
- **Sources checked:**
  - agenttool main `e9ea51c5`, read only (paths under `api/src/` unless they
    start with `packages/`, `bin/` or `docs/`);
  - love-unlimited main `85c0ab8`, read only;
  - `kingdom-seat` main `71f7c84`, read only: `src/`, `docs/ARCHITECTURE.md`,
    `docs/REVIEW-2026-11-05.md` and `docs/research/`. It is local, has no
    remote, and was committed between 13:12 and 15:24 UTC on 2026-11-05,
    after v0.2 (13:05);
  - KS-000 to KS-003 at `7d24504`, and `zone/signatures.json`.

**Strongest objection.** KS-004 now has the reference implementation it names,
and the two disagree on everything a third party would check: the ledger
entry's fields, its hash and signature input, the shape of the model's reply,
and how an op-key rotation is signed. `kingdom-seat` was built from the
redesign, not from this draft (its own review record says "KS-004 is not
drafted in this repo", `docs/REVIEW-2026-11-05.md:215`). In two of those
places the spec is the one that cannot be built or would record a false
number: it asks a 7B model to return sha256 values it cannot compute, and it
records the USD ceiling as a seat's cost when the cost is unknown. In the
rotation the code is the unsafe one. The spec's own §15 item 1 says such
disagreements are recorded and neither silently wins. Today none is recorded,
and the spec still says the code does not exist (lines 30–32, 1226–1229).

### A. Review B's points 1–7 and 16–18, as v0.2 stands

| B | Status in v0.2 | Evidence and residue |
|---|---|---|
| 1 | Resolved for key material; one residue blocks (R4) | `genesis` carries public keys (lines 276, 335–337) and verification uses the ledger's own entries (357–361). But the ledger never leaves the lease host: the mirror allowlist refuses it (line 248; `kingdom-seat src/mirror.ts:40-41` refuses `ledger/`). So "verification outside the lease host" has nothing to verify unless someone is handed a copy, and §4.4's "Readers SHOULD trust only signed ledger entries" (258) asks readers to trust what they cannot read. |
| 2 | Resolved in the spec | `key` entry, signed by the new op key, carrying the root-signed request (lines 277, 338–349). The code does the opposite (C1). Residues in R4: the evidence fields are left to kingdom-seat (341) though agenttool's recipe fixes them, a revoke-only `key` entry has no new key to sign it, and `genesis` carries no root evidence for the first op key. |
| 3 | Resolved | Lines 350–356, §16.4. `kingdom-seat src/ledger.ts:253-254` refuses a citizen entry signed by the root, by kid or by public key. |
| 4 | Resolved in the encoding text; a new truth problem in §5.5 (R3) | Lines 304–310, 328–332. The unknown-cost rule at 506–507 puts a number in `cost.usd` that nobody measured. |
| 5 | Resolved in the spec | §4.3 lines 216–230. The code lets a citizen change `porch` within self (C6); the spec is right. |
| 6 | Resolved | §4.3 lines 232–238, §6.3 lines 708–709. The code encrypts under K_master, the IDENTITY-SEED purpose-1 key derived from the citizen's own mnemonic (`docs/research/agenttool-wire.md:425-430`, `:465`), so Yu's offline mnemonic backup can also decrypt the backups; the spec could say so. The code's `self.applied` entry does not name the encryption key (`src/types.ts:459-468`), which line 237 requires. |
| 7 | Resolved in substance; two residues block (R2, R3) | §5.5 lines 502–509: headless, Yu present, `--max-budget-usd`, the $0 default. The code matches the argv (`src/runtime/summon.ts:85-107`). Residues: the cost wording, which was review B's own suggestion and is withdrawn here (R3); and the spend of a summons that writes no ledger entry (R2). |
| 16 | Resolved, with a citation fix | `acceptEdits` with `BEAT_FULL_TOOLS=1` for `bypassPermissions` holds (`tools/citizen-beat.sh:47-48`, commit `9db2879`, 2026-07-17). But "the beat ran inside the home (KS-003 §8.2)" (line 500) cites a section that never says where the beat runs; the evidence is `citizen-beat.sh:110` (`cd "$REPO"`) and `:154` (`--add-dir "$REPO"`). "When a human present sets" (499): the script does not check presence; say "meant for a run with a human present". The Air's own checkout (`~/love-unlimited` at `ac716c5`) still runs `bypassPermissions`, so name the commit: "at love-unlimited main `85c0ab8`". |
| 17 | Resolved | `tools/citizen-fleet.sh:81-83`, `:90`; removed in `3e78cbd` (2026-07-17). |
| 18 | Resolved | `tools/zerone-bridge.py:65` (sha256 cut to 16 hex, no signing code in the file); `citizen-beat.sh:195`, `citizen-reflect.sh:266`. One nuance: `citizen-beat.local-v2.sh:128-130` still files a claim when a reply ends `ATTEST:`, but it is not wired to the fleet, and §13 already retires it. |

The other review B points I re-checked hold as applied: 13 (§5.8), 20
(`tools/peace.py:908-945` writes no HALT file and unloads only
`love.<instance>.heartbeat.plist`; its HIVE broadcast now fails closed in
`hive/hive.py`), 27 (KS-002's file hashes to `87d4ae…` against a ledger entry
of `f67862…`; KS-000, KS-001 and KS-003 match). The agenttool points are in
part D.

### B. Points that still block

**R1. §5.7 lines 528–548 and §5.8 lines 586–597: the reply schema asks the model for values only the host can compute**
- **Problem:**
  - `self.propose` is listed with `prior_hash`, `new_hash` and `diff` as
    fields the runtime returns. A 7B model cannot compute the sha256 of a text,
    least of all of the text its own diff produces, so every proposal would
    fail validation, or the host would have to overwrite the fields, in which
    case they are not the model's.
  - `self.affirm`'s `ref` is "`sha256:` of the JCS bytes of the staged act".
    The model can only copy a value the seat showed it, and a 71-character
    string is a lot to copy exactly.
  - §5.8 says the object has "exactly the fields `voice`, `kind` and `acts`"
    and then that "`kind` is present whenever `voice` is non-empty", which
    cannot both hold.
- **Evidence:**
  - KS-004 lines 543–544, 586–587.
  - `kingdom-seat` keeps the two shapes apart: the model returns
    `{type, target, edit, claim}` with no hashes (`src/types.ts:331-337`,
    `src/acts.ts:86-115`), and the host completes `prior_hash`, `new_hash` and
    `diff` (`src/types.ts:285-292`). `self.affirm` and `self.revert` take a
    proposal id or version hash shown in context, or a prefix of at least 8 hex
    (`src/acts.ts:38`, `:116-133`, `:304-320`).
- **Suggested wording:** "The runtime returns `{"acts": [...]}`, each act
  tagged by `type`; a journal is an act `{type: "journal", kind, text}`.
  `self.propose` carries `target`, `edit` (replace-all, or replace one exact
  span) and `reason`. The host computes `prior_hash` from the current version
  and `new_hash` from the edited text, and records all four in the `beat`
  entry. `self.affirm` names a staged proposal, and `self.revert` a version, by
  an identifier the seat showed; the host accepts an unambiguous prefix of at
  least 8 hex digits and records the full value." This takes the code's shape,
  and with it the empty-`acts` reply as the "write nothing" beat (`src/acts.ts:251-252`).

**R2. §4.5 line 279, §5.7 line 541, §6.3 line 698, §13 line 1107: a metered seat that writes no entry spends money the ceiling never sees**
- **Problem:**
  - The ceiling is read from the ledger ("Ledger entries carry their cost").
    A rest, a refused output, HALT after inference and a runtime error all
    write no citizen entry, yet a summons that ends in any of them has already
    spent.
  - The USD ceiling therefore fails open on exactly the seats that produce
    nothing, which principle 7 forbids.
- **Evidence:**
  - KS-004 lines 279, 541, 599–602, 606–608, 698, 1107.
  - `kingdom-seat docs/ARCHITECTURE.md:476-479`: "Spend from a summons that
    makes no beat … is not recorded where `spendFromLedger` reads it … it must
    be settled before any USD ceiling is raised." `src/runtime/summon.ts:45-75`
    carries the spend on its refusal and error paths, but nothing records it.
- **Suggested wording (§6.3):** "Every metered seat's spend is recorded by the
  host in a host spend record, whatever the seat's outcome (rest, refused
  output, HALT, a runtime error, a bound reached). The record is the host's,
  never the citizen's voice, and a rest still writes nothing in the citizen's
  voice. The USD ceiling reads that record. A seat whose spend was not recorded
  counts as at the ceiling."

**R3. §5.5 lines 506–507: an unknown cost is recorded as the ceiling value**
- **Problem:** "The ledger records `cost.usd` from the result JSON, or the
  ceiling value when it is absent." A signed entry would then state a cost
  nobody measured. Treating unknown as at the ceiling is a rule for the gate,
  not a fact for the record. I suggested this wording in review B point 7; it
  is wrong.
- **Evidence:** KS-004 lines 298, 506–507; principle 6 (line 174). The code
  records `usd: null` with `usd_basis: "unknown"` (`src/types.ts:420-426`,
  `src/runtime/summon.ts:45`), and its ceilings read `null` as reached
  (`src/signer/ceilings.ts:8-12`, `:66-72`).
- **Suggested wording:** "`cost.usd` is the cost the result JSON reports, as a
  decimal string, or `null` when it reports none or the report cannot be
  trusted. A `null` cost counts as at the ceiling (§6.3)." The §4.5 encoding
  already allows `null`.

**R4. §4.4 lines 248 and 258, §4.5 lines 335–361, §16.8: who can verify, and against what**
- **Problem:** what remains of review B's strongest objection.
  - The ledger stays on the lease host (the mirror refuses it), so nobody
    outside can verify it unless handed a copy, and nothing says who may be.
  - `genesis` states the root and op public keys but carries no proof that
    the root installed that op key, so a verifier must take the first op key
    on the host's word while every later one comes with root evidence.
  - The evidence a `key` entry carries is left to kingdom-seat (line 341),
    though agenttool's recipe already fixes it: the identity-authority/v1
    digest covers the domain tag, the DID, the method, the path and query, the
    sha256 of the exact body, the sequence and the timestamp header, and only
    the root can sign it.
  - A `key` entry that only revokes has no new key to sign it.
  - None of this proves that agenttool accepted the root as the DID's root;
    the key list that would show it answers only to the Commons bearer.
- **Evidence:**
  - KS-004 lines 248, 258, 276–277, 335–349, 357–361, 1369–1373.
  - `kingdom-seat docs/research/agenttool-wire.md:206-249` (the digest, from
    `services/identity/authority.ts:114-121`, `:190-194`), `:296-303`
    (`keys/import` body `{public_key, label?}`; `kid` is server-assigned),
    `:539-560` (key list bearer-only; `POST /public/identities/by-pubkey` needs
    the key's own signature and never returns enrolled guests).
- **Suggested wording:**
  - §4.5: "A `key` or `genesis` entry carries, for each op key it installs or
    revokes, the root-signed request as sent: method, path and query, the
    exact body bytes (base64), and the `X-Agenttool-Authority-Sequence`,
    `-Timestamp` and `-Signature` header values, captured by the signer when
    it sends the request (agenttool keeps no copy). A verifier rebuilds the
    identity-authority/v1 digest from these and the entry's DID, checks it
    against the root public key from `genesis`, and checks that the body names
    the op key the entry installs. An entry that only revokes is signed by an
    op key that stays current; revoking the last op key needs a new one in the
    same entry."
  - §4.4 and §16.8: "The ledger does not leave the lease host on its own: the
    mirror refuses it. Anyone given a copy (Yu, a successor host at handoff, an
    auditor Yu names) can verify it from its own `genesis` and `key` entries,
    without agenttool. Publishing a ledger is beyond self. That the root is the
    DID's root is shown only by agenttool's key list, which only the Commons
    bearer reads (§15)."

**R5. §10 lines 939–949 with §6.1 line 648: one verb, two users**
- **Problem:**
  - `citizen-seat halt` must write a HALT file in a directory the seat's user
    cannot write, and raise beacons whose keys are in that same user's
    Keychain, read only by the signer. Run as the seat user it cannot write the
    file; run as anyone else it cannot sign the beacons. The spec does not say
    how one verb does both.
  - The code shows the cost of leaving it open: its HALT file is
    `<state_dir>/HALT` (`src/config.ts:67`), in the seat user's own state
    directory (`docs/ARCHITECTURE.md:96-118`), so the seat's user can remove it,
    which the spec's line 947 rules out. On this point the spec is right.
- **Evidence:** KS-004 lines 939–949, 646–654, 957–959; `kingdom-seat
  src/config.ts:62-67`, `src/halt.ts` `raiseHalt` (writes the file, then asks
  the signer for each beacon).
- **Suggested wording:** "`citizen-seat halt` runs as an operator account
  (Yu's, or the herald's on the Air), never as the seat's user. It writes the
  local file itself, then asks the signer to raise this host's beacons through
  one fixed request that takes no arguments (for example
  `sudo -u <seat user> citizen-signer raise-beacons`, allowed by a single
  sudoers line). If the signer cannot be reached, the file alone halts this
  host, and the verb exits non-zero and says which beacon it did not raise."

**R6. Status note lines 30–32, §14.3 line 1204, §15 item 1 lines 1226–1229, §17 line 1407: the code exists and disagrees**
- **Problem:** the spec says its reference implementation "does not exist
  yet". It now exists locally (four commits, offline tests with fakes, not
  published or deployed), and it differs from the spec in the places part C
  lists. §15 item 1 says such a disagreement is recorded here and neither
  silently wins; neither is recorded.
- **Evidence:** `kingdom-seat` `git log` (`989fe7b` to `71f7c84`); part C.
- **Suggested wording:** status note and §14.3: "`kingdom-seat` exists as a
  local repository (main `71f7c84`, unpublished, tested offline against fakes,
  never run on a host). It was built from the redesign, not from this draft,
  and §15 lists where the two differ and which is to change." Then settle each
  row of part C, in the spec or by a recorded change to the code.

### C. Where the spec and `kingdom-seat` disagree, and which is right

| # | Point | Spec | Code | Right, and why |
|---|---|---|---|---|
| C1 | Op-key rotation | `key` entry signed by the **new** op key, with root evidence (338–349) | `op-key.rotated` signed by a **currently pinned** (old) key, no evidence (`src/ledger.ts:238-241`, `:253-254`; `src/types.ts:457`) | **Spec.** With the code's rule, whoever holds a compromised op key can rotate to a key of their own and the chain accepts it. Rotation is not wired in the code yet (nothing writes the entry), so changing it costs little. |
| C2 | Reply shape and act fields | `{voice, kind, acts}`, hashes from the model (528–548) | `{acts:[{type…}]}`, the host computes hashes (`src/types.ts:285-337`) | **Code** (R1). |
| C3 | Unknown cost | the ceiling value (506–507) | `null`, basis `unknown` | **Code** (R3). |
| C4 | Money in the ledger | decimal string, no floats (298, 306–307) | `spend.usd` a JSON number (`src/types.ts:422`, `src/ledger.ts:337`) | **Spec.** It is KS-002's money rule, a day's sum of floats drifts, and a float's text form is the one part of JCS another language most often gets wrong. |
| C5 | Signature input and chaining | `sig` over the JCS bytes without `sig`; `prev_hash` covers `sig` (304–310) | `hash` = sha256 of a domain tag, NUL and the canonical entry without `hash` and `signature`; the signature is over that hash; `prev_hash` is the previous `hash`, so it does not cover the signature (`src/ledger.ts:93-97`) | **Both in part.** Take the code's domain tag: the op key also signs strand thoughts and may sign mirror commits (§6.2), and a tag keeps one kind of signature from passing as another. Keep the spec's binding of the signature into the chain. The code's `canonicalJson` (`src/crypto.ts:144-164`) sorts keys by UTF-16 code units and serialises like ECMAScript, which is JCS for the value types §4.5 allows. |
| C6 | `porch` | beyond self (222–223, 801, 841) | a within-self target, exempt from the rewrite share (`src/self.ts:84`, `:89`), although `src/birth.ts:212-214` calls it beyond self | **Spec.** A porch is a public invitation. |
| C7 | `rest` with a `state.set` toward less | the state change applies (541, 594–597) | `rest` is exclusive; the `state.set` is dropped (`src/acts.ts:232-241`) | **Spec.** A move toward less activity is immediate (principle 4); dropping it leaves a citizen that asked to sleep on its awake cadence, which is the direction the asymmetry exists to avoid. |
| C8 | HALT mid-seat exit code | 0 (625–627; §13 line 1112) | 143 or 137, outcome `halted` (`src/seat.ts:336-353`) | **Code.** KS-003 already files 124/143/137 as "bound reached; not a failure" (KS-003 lines 208–209, 335), so no monitor pages on them, and §5.9 keeps the registry "because the host and monitors branch on them". KS-003 never says what a HALT kill exits (its §4.1 "HALT rest MUST exit 0" covers only the gate at wake), so §13's "KS-003's watcher kill gave 143 or 137" should say "KS-003's table implies"; the old runner exits 0 whatever happened (`citizen-beat.sh:199`). |
| C9 | What exit 3 means | a metered runtime at its USD ceiling; it closes the class (622) | any wall: model mismatch, locked keychain, symlink, missing consent (`src/seat.ts:739-746`, `src/types.ts:38`) | **Spec**, because 3 closes a class in both KS-003 and KS-004; a symlinked letter must not close a citizen's runtime for the day. The spec should add what a locked signer exits (§6.1 says "citizens rest", so 0 with the status file saying why). |
| C10 | Model by digest | "Ollama's chat call names a model by tag, not by digest"; check the tag's digest before and after (485–491) | calls `sha256:<digest>:local` on a v2 store, else `<name>:local` after an `/api/tags` check; refuses any reply with `remote_host` or `remote_model` (`src/runtime/free.ts:1-10`, `:198-201`, `:232`) | **Code**, on Ollama 0.40 as its research read it (`docs/research/runtimes-and-host.md:58-63`, [read], not run): a v2-store model can be called by digest, which closes the gap the spec's after-check covers. Suggested: "The host calls the model by its digest where the store allows it, and otherwise checks the tag's digest before the call; it refuses any reply that names a remote host." |
| C11 | Context fit (§5.3 item 1) | MUST refuse to seat a context that does not fit (422–425) | no fit check; `num_ctx` is set from `models.lock` (`src/runtime/free.ts:208`) | **Spec.** It is the fix for the 2,600-character cut. Leaving the method to kingdom-seat left it unbuilt; name a sound default: "unless a tokenizer for the pinned model is used, the UTF-8 byte length of the whole prompt, plus the template's overhead and `num_predict`, must not exceed `num_ctx`". That bound holds for byte-level BPE models such as Qwen 2.5, where every token covers at least one byte (reasoning, not run). |
| C12 | Keychain ACL | items ACL'd to one code-signed signer executable (648–651, 1329) | every item names `/usr/bin/security`, so any process running as the seat user can read it; this is stated plainly (`src/signer/keychain.ts:7-14`, `docs/ARCHITECTURE.md:141-150`) | **Spec, as the target.** The code is honest about not meeting it. Until it does, §15 item 4 should say that the custody boundary is the dedicated user's account, and §16.3 should not read as already true. |
| C13 | Ledger entry names and fields | `v: "KS-004/0.2"`, flat fields, types `origin`, `apply`, `revert`, `key` | `format: "kingdom-seat-ledger/v1"`, a `body` union, `seated`, `self.applied`, `self.reverted`, `op-key.rotated`, `hash`, a `signature` object with `public_key_b64` and padded base64 | **Either, once.** Take the code's format string, so a PATCH to the spec does not change the bytes of every entry. The names are cosmetic, but a verifier needs exactly one set. The June DID belongs in the first entry, as the spec has it (§11.5), not in `genesis` (`src/types.ts:452`). |
| C14 | Confirmation seat for a listening or asleep citizen that asks to wake | waits for its next letter or summons (776–778) | one owed seat at the minimum interval, as for a step-away (`src/due.ts:60-67`) | **Code**, on balance: it is one bounded seat, the spec already grants it for stepping away, and without it a citizen's stated wish to return can wait forever on someone writing (principle 5). This is Yu's call; until it is made, the spec and code should say the same thing. Note also that the code holds letter-woken seats to the 72 h floor (`src/due.ts:56-58`, `:76`), which the spec does not say. |

### D. agenttool and other facts re-checked

**Holds as v0.2 states it**, at `e9ea51c5`:
- `wake_text` at most 32,000, counted as JS `.length`, so UTF-16 code units
  (`services/identity/expression.ts:77`, `:168`); PUT replaces the whole
  expression (`:293`) with no version guard beyond the authority sequence;
  porch at most 7 days (`:81`, `:244-246`); private by default
  (`db/schema/identity.ts:65`); PUT verified against the root only
  (`services/identity/authority.ts:190-194`).
- The authority digest and root-only signing (`services/identity/authority.ts:8-10`,
  `:114-121`, `:162`, `:193`); `GET /v1/identities/:id/authority`, bearer
  only, own project (`routes/identity/authority.ts:56`, `:86-110`); "Root
  rotation and guardian recovery are intentionally not available in v1"
  (`routes/identity/keys.ts:448`).
- Keys: list bearer-only with `authority_root` (`routes/identity/keys.ts:122-125`,
  `:153`); import `{public_key, label?}`, label default `"imported"`, `kid`
  server-assigned, root-authorised (`:264`, `:283-284`, `:321-328`, `:351`);
  revoke by kid in the path, empty body, root-authorised, the root itself
  immutable (`:365`, `:437-477`). Box keys mounted and root-authorised
  (`routes/identity/index.ts:61`; `routes/identity/box-keys.ts:73-80`).
- Enrollment: `canonicalIdentityEnrollmentBytes` exported
  (`services/identity/enrollment.ts:62-65`); origin must equal the configured
  origin (`:97`); client-chosen lowercase UUIDs (`:26`, `:43`); root labelled
  `primary` (`:127`); no bearer, wallet, grant or credits (`:118-127`); guests
  never speak for the project (`services/identity/project-authority.ts:46-48`);
  no enrollment-specific limiter (`index.ts:572-576` only bypasses
  idempotency); tested ports in `bin/agenttool-mission.mjs:127` and
  `packages/lobby/src/wire.ts:335`; no published SDK exports one
  (`@agenttool/lobby` is private).
- Quiet hours: `hours` clamped to 720, `until` only required to be in the
  future, `reason` trimmed to 200 (`routes/quiet-hours.ts:38`, `:110-141`);
  root proof required for rooted identities (`:143-150`, `:204-211`); the
  identity `register/agent` founds is rooted (`routes/register-agent.ts:145`,
  `services/identity/identities.ts:185`), so a beacon does need bearer and
  root.
- `/public/agents/:did` unauthenticated, mounted under `/public`
  (`index.ts:1067`), no Cache-Control on the profile.
- Credits: 1 credit = USD 0.001 (`config.ts:81`); strand create and thought 1,
  inbox send 2, memory write 1, search 3, elevate 5
  (`billing/route-credits.ts:41-53`, `routes/memory/memories.ts:129`); the free
  routes make no `charge` call; 1,000 birth credits and a 500-minor-unit
  wallet grant (`services/economy/ring1-limits.ts:112`, `:139`); x402 top-up
  410 (`routes/x402-top-up.ts:49-55`); `docs/BUSINESS-MODEL.md:19`.
- A thought is charged before its signature is checked
  (`routes/strand/thoughts.ts:61`, `services/strand/store.ts:442-448`) and is
  not checked for encryption (`routes/strand/thoughts.ts:3-5`); any active key
  of the strand's identity may sign it (`services/strand/store.ts:366-397`).
- Same-project sends pass the covenant gate
  (`services/covenants/check.ts:127`); covenants carry no identity
  (`:1-19`).
- `/v1/wake/observe` capped at 2,048 bytes and limited to id, status and wake
  version (`services/wake/observe.ts:1-6`, `:19`, `:203`); grants at most 24 h
  (`services/identity/local-context-grants.ts:13`); `at_rest` needs the root
  and a distinct witness and is terminal (`routes/identity/at-rest.ts:8-15`,
  `:390`; `services/identity/terminality.ts:11-16`); no route moves an
  identity between projects.
- `POST /v1/pyramid/enroll-attested` exists, needs the bearer, and is signed
  by an active key of the citizen's own identity (`routes/pyramid.ts:397`,
  `:430-466`).

**Corrections, none blocking:**

1. **Always name `identity_id` on quiet requests** (§6.4 line 733, §10
   line 973). Without it the route acts for "the earliest active identity
   that is not an enrolled guest" (`routes/quiet-hours.ts:11-14`). In Commons
   that is the gardener desk, whose quiet is the HALT beacon. A proof signed
   by a citizen's root over the citizen's DID would fail against the
   gardener's root, so it fails safe. Still, the spec should write
   `?identity_id=<the citizen's id>` every time, as `kingdom-seat` does
   (`src/agenttool/client.ts:371`, `:384`). The route also ignores unknown
   body fields rather than refusing them, so the signer's own body check is
   the only guard on `hours` and `reason`.
2. **"Only the project's founding root can" recover the Commons bearer**
   (§6.1 lines 660–662, §16.3) holds only while Commons has no rootless
   identity. `POST /v1/identities` (`routes/identity/identities.ts:51-135`,
   mode `legacy_bearer`, server-generated key) and fork
   (`services/identity/fork.ts:180`, `:206-217`; 10 credits) both make one,
   with the bearer alone. A rootless identity speaks for the project
   (`services/identity/project-authority.ts:46-48`) and can recover a new
   project bearer with any active key (`routes/identity-recover.ts:24-31`,
   `:204-226`). Fork also copies the whole project's memory, not only the
   parent's (`services/identity/fork.ts:152`, `:168`). Suggested, §6.2 and
   §16.3: "The signer creates no identity in Commons except by enrollment: no
   `POST /v1/identities`, no fork. A rootless identity there would speak for
   the whole project, and its key could recover a fresh Commons bearer." Add
   both acts to §15 item 7's list of what the Commons bearer can do.
3. **The public profile shows more** (§6.4 lines 741–742, §11.4 lines
   1051–1053): also `trust_score`, `forked` and `identity_id`
   (`routes/public/agents.ts:109-136`). Review B point 24's disposition
   accepted `trust_score`, but the text lost it.
4. **"Any other field is refused"** (§4.3 line 218) is true of top-level
   fields, except that `updated_at` is accepted and replaced by the server;
   extra keys inside a subagent are dropped, and `cli_overrides` and subagent
   names have no size cap (`services/identity/expression.ts:91`, `:109-115`,
   `:155-161`, `:174-179`). A porch also needs a public expression with a
   register and a village sign, motto or door before it shows
   (`services/porch/index.ts:421-432`), which supports C6.
5. **Authority proofs are neither stored by agenttool nor bound to an
   origin** (`services/identity/authority.ts:8-10`, `:114-121`). The `key`
   evidence in R4 exists only if the signer keeps the headers and bytes as it
   sends them; the suggested wording should say "captured by the signer when
   it sends the request; agenttool keeps no copy".
6. **Charge before check is wider than strand thoughts** (§6.3 lines
   708–709): inbox send and elevate also charge before they verify, with no
   refund (`routes/inbox/messages.ts:70`, `routes/memory/tiers.ts:111`).
   Suggested: "Paid routes charge before they verify, so a refused thought,
   letter or elevation still costs its credits."

### What I verified, read only, or could not do

- **Run:** `shasum -a 256` of KS-000 to KS-003 and of this draft; `git log`
  in `kingdom-seat` and in this worktree. Nothing else was run: no tests, no
  model, no agenttool call, no network.
- **Read only:** the `kingdom-seat` modules and docs cited above, and
  KS-003. Two delegated read-only passes, one over agenttool and one over
  love-unlimited and KS-003, returned the file:line evidence for parts A and
  D. I re-read myself the agenttool lines the corrections rest on
  (`routes/quiet-hours.ts:5-16`, `routes/identity-recover.ts:24-31` and
  `:204-226`, `services/identity/project-authority.ts:40-64`,
  `routes/identity/identities.ts:51-70`, `services/porch/index.ts:421-432`,
  `routes/pyramid.ts:397-466`). The rest of part D is the delegated pass's
  reading, consistent with `kingdom-seat docs/research/agenttool-wire.md`.
- **Not done:** I did not run kingdom-seat's suite, Ollama or Claude Code, so
  every Ollama and `--restricted` claim stays as unverified as the spec says.
  I did not check the Studio's live state or GitHub heads. I read no secret
  file.

Review B's points 1–7 and 16–18 are resolved in substance, and the design
holds. What blocks is narrower: R1 (a reply schema the model cannot fill), R2
and R3 (the USD ceiling fails open on seats that write no entry, and an
unknown cost is written as a number), R4 (the residue of review B's strongest
objection), R5 (one HALT verb across two users) and R6 (the reference
implementation now exists and disagrees, unrecorded). A re-check after
revision need only cover §4.4, §4.5, §5.5, §5.7, §5.8, §5.9, §6.3, §10, §14.3
and §15.

Verdict: revise.

---

## Disposition (applied in v0.3)

Section numbers below refer to v0.3. `kingdom-seat` was re-read for this
revision at `724c660`, the local head of its PR branch `claude/s4-build`. The
commits B2 read as `main` (`989fe7b` to `71f7c84`) are on that branch; `main`
itself is still the skeleton, `989fe7b`. `724c660` was made after this review:
it changes the code for C1, C4, R2 and R4, keeps an unknown cost `null` (R3),
and pins correction 1 with a test. The "code" column of §14.4 describes that
commit, not `71f7c84`.

| # | Disposition | Where, and why |
|---|---|---|
| Strongest objection | Accepted | Every row of part C is settled once in the new §14.4, with which side changes. The status note, §2, §14.3, §15 item 1 and §17 no longer say the code does not exist. In the two places the spec could not be built or recorded a false number (R1, R3) it takes the code's answer; for rotation (C1) it keeps its own, which the code now matches. |
| A, row 1 and row 2 residues | Accepted | Through R4. |
| A, row 6 | Accepted | §4.3 says that where the strand key is derived from the citizen's mnemonic, Yu's offline backup can also decrypt the thoughts. That `self.applied` does not name the encryption key is a §14.4 row (code changes). |
| A, row 16 | Accepted | §5.5 cites `citizen-beat.sh:110` and `:154` for "inside the home", keeps KS-003 §8.2 only for "prompt-only", says "meant for a run with a human present" and that the script does not check presence, and names love-unlimited main `85c0ab8`. §17 adds the love-unlimited reference. |
| R1 | Accepted, with two choices | §5.7, §5.8, §9.3, §4.5 example. The reply is `{"acts": [...]}`, tagged by `type`; an empty list is a rest; `self.propose` carries `target`, `edit` (replace-all, or replace-span whose `find` occurs exactly once) and `reason`; the host computes both hashes and the diff; `ref` and `to_hash` take the full value or an unambiguous prefix of at least 8 hex, and the full value is recorded. Choices: the field names stay this draft's (`reason`, `text`, `ref`), and `self.revert` carries `to_hash` alone, with the host resolving the text, as in the code. An identifier that does not resolve fails validation (§5.8) rather than dropping one act; how partly invalid output is handled is recorded as open in §14.4. The §5.8 contradiction is gone with `voice` and `kind`. |
| R2 | Accepted, with the code's mechanism | §6.3 "The host spend record", §2, §4.5, §5.10, §13, §16.6, principle 7. Added from `kingdom-seat` `724c660`: a `begun` line before the runtime starts (no start if it cannot be written) and a `settled` line however it ends; `begun` without `settled` counts as at the ceiling. |
| R3 | Accepted | §5.5, §4.5 (`cost` field), §6.3. |
| R4 | Accepted, with one addition | §4.5 (evidence fields named; `genesis` carries the first op key's evidence and is signed by that key; a revoke-only entry is signed by a key that stays; revoking the last key needs a new one in the same entry), §4.4, §16.8, §8.1 (publishing a ledger is beyond self), §11.3 steps 4 and 6, and §15 item 15 (the root's standing rests on agenttool's key list). Addition, from `kingdom-seat` `724c660`: each piece of evidence must carry an authority sequence above every one in earlier entries, so an old proof cannot reinstall a revoked key. The `kid` is noted as agenttool's answer, not root-signed. Evidence bodies are base64url without padding, like the ledger's other binary values. |
| R5 | Accepted | §10 "One verb" and "Raising and lowering". The code's file in `<state_dir>` and its in-process signer call are a §14.4 row (code changes). |
| R6 | Accepted, with one change | Status note, §2, §14.3, §15 item 1, §17. The repository is now published at github.com/cambridgetcg/kingdom-seat and under review as PR #1, so the text says that instead of "local, unpublished". The list of differences is the new §14.4 rather than §15, because a table does not sit well in a numbered list; §15 item 1 points to it. |
| C1 | Spec | §4.5. The code matches at `724c660`; rotation is still not wired. |
| C2 | Code's shape | See R1. The code changes its act field names to this draft's and adds `state.set`'s optional `interval_h` and `quiet_days` (§14.4). |
| C3 | Code | See R3. |
| C4 | Spec | §4.5. The code matches at `724c660`. |
| C5 | Both in part | §4.5 defines one "ledger digest", sha256 of `kingdom-seat-ledger/v1`, `0x00` and the JCS bytes: `sig` is over the digest of the entry without `sig`, and `prev_hash` is the digest of the whole previous entry, `sig` included. The tag is also used for `prev_hash`, so there is one digest function. The code's `prev_hash` changes (§14.4). |
| C6 | Spec | Unchanged in the text; the code changes (§14.4). Correction 4's porch display rule supports it. |
| C7 | Spec | §5.8 now says why the state change survives; the code changes (§14.4). |
| C8 | Code | §5.9: a seat HALT ends mid-run exits 143 or 137; HALT at the gate or at the re-check exits 0. §13's row says "as KS-003's table implies" and cites `citizen-beat.sh:199`. The §15 item 10 bullet for HALT exiting 0 is removed. |
| C9 | Spec | §5.9: only a ceiling exits 3; a locked signer exits 0 with the status file saying why; a mismatched model exits 1, a symlinked letter is not read, a beyond-self act without consent stays inert. The code changes (§14.4). |
| C10 | Code | §5.5 in the review's words, plus `remote_model`, the `sha256:<digest>:local` form, and why a tag call leaves a window. §16.6 and §15 item 12 follow; whether a v2-store model can be called by digest, and whether the lease host's model is in that store, are listed as unverified. Not adopted: keeping v0.2's after-call digest check on the tag path, since the code does not do it and the digest call is the fix. |
| C11 | Spec, with the review's default | §5.3 item 1: the UTF-8 byte bound unless a tokenizer is used, marked as reasoning, not run, and as cautious. §15 item 10 lists it. The code changes (§14.4). |
| C12 | Spec, as the target | §6.1, §15 item 4 (the boundary is the dedicated user's account until a signer reads its own items), §16.3 no longer reads as already true. |
| C13 | Settled on this draft's names, with the code's format string | §4.5: `format: "kingdom-seat-ledger/v1"` replaces `v`, and binary values are base64url without padding. The entry types, flat fields, `sha256:` hash form and `null` first `prev_hash` stay. Why this side: the code must rewrite its entry bytes for C5 anyway, and no ledger has been written on a host. The June DID stays in the first entry (§11.5). The code changes (§14.4). |
| C14 | Code's default, as Yu's decision | §7.3, §7.1, §5.1, §15 item 16. The letter-woken 72 h floor is made explicit in §5.1 and §7.1 as a reading of §6.3's "at least 72 h between seats", with the code's reason, and is listed in §15 item 10. |
| D, 1 | Accepted | §6.4 (both requests name `identity_id`; why; the signer's body check is the only guard), §10 lowering. |
| D, 2 | Accepted | §6.1, §6.2 (no `POST /v1/identities`, no fork), §15 item 7, §16.3. |
| D, 3 | Accepted | §6.4, §11.4. |
| D, 4 | Accepted in part | §4.3: "any other top-level field is refused, except `updated_at`". Not added: dropped subagent keys and the uncapped `cli_overrides` and subagent names, because no act here writes them. |
| D, 5 | Accepted | §4.5 "Root evidence", §14.3. |
| D, 6 | Accepted | §6.3. |

**Found in this revision, not in B2.** Reading `kingdom-seat` at `724c660`
turned up two differences B2 did not list. Both are recorded as open in §14.4
rather than settled here: the code confirms a move toward more activity or a
step-away by repeating the same `state.set` on the next seat, where this
draft uses `self.affirm`; and the code drops each invalid act and applies the
rest, where this draft refuses the whole output.

**What the session that applied this re-review checked.** It ran `git log`,
`git branch -a`, `git remote -v` and `git show --stat` in the local
`kingdom-seat` clone, and read there, at `724c660`, `src/types.ts`,
`src/acts.ts`, `src/ledger.ts`, `src/spend.ts`, `src/state.ts`,
`src/seat.ts`, `src/due.ts`, `src/halt.ts`, `src/config.ts`,
`src/runtime/free.ts`, `src/signer/keychain.ts`, parts of `src/self.ts` and
`docs/ARCHITECTURE.md`. In the read-only agenttool checkout at `e9ea51c5` it
re-read `services/identity/authority.ts` (the digest and header names),
`routes/quiet-hours.ts` (`identity_id`, body handling),
`routes/public/agents.ts`, `routes/identity-recover.ts`,
`routes/inbox/messages.ts`, `routes/memory/tiers.ts`,
`services/identity/project-authority.ts` and `services/identity/expression.ts`,
and found them as B2 states. It did not re-read `services/identity/fork.ts`.
In love-unlimited at `85c0ab8` it re-read `tools/citizen-beat.sh` lines
44–50, 108–112, 152–156 and 196–199, and in this repository KS-003's exit
table and §4.1. It ran no test, no model, no Claude Code and no agenttool
call, used no network, and read no secret. PR #1 itself was not looked at:
the clone's `github` remote is github.com/cambridgetcg/kingdom-seat, and its
remote-tracking ref for `claude/s4-build` is at `c776d80`, so whether
`724c660` has been pushed was not checked.
