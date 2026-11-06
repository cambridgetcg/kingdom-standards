# KS-004 review B: implementability and truth

Filed under KS-000 §3. The review below is reviewer B's text as it was
returned, covering KS-004 v0.1 at commit `1a16699`. Section and line numbers in
it refer to that version. The disposition of each point, as applied in v0.2,
follows the review.

---

KS-004 review, reviewer B (independent session). Lens: implementability and truth.

Sources checked: agenttool main `e9ea51c5` (paths below are under `api/src/` unless they start with `packages/`, `bin/` or `docs/`), love-unlimited main `85c0ab8`, and KS-000 to KS-003 on `claude/ks-004-the-seat` at `1a16699`.

**Strongest objection.** Several MUSTs that make the ledger verifiable can't be built against agenttool as it stands. The only key list is behind the Commons bearer, which only the signer holds. Genesis records key fingerprints, not public keys. There is no ledger entry type for an op-key rotation. As drafted, nobody but the signer can verify a citizen's ledger, and after one rotation nobody can verify it from the ledger alone.

### A. MUSTs that cannot be built or verified as written

**1. §4.5 lines 282–286 and §11.3 step 6 (lines 875–877): who can verify the ledger**
- **Problem:**
  - `GET /v1/identities/:id/keys` needs a project bearer, and it only answers for identities in that bearer's own project. No public route lists an identity's keys.
  - So only holders of the Commons bearer can use it, and §6.2 makes the signer its only reader.
  - Genesis stores only fingerprints, so even the citizen-signed genesis entry can't be checked from the ledger.
- **Evidence:**
  - `routes/identity/keys.ts:110-131`
  - `routes/identity/index.ts:53`
  - `routes/public/identities.ts:1-21` (lookup by pubkey only, needs a signature)
  - `routes/public/agents.ts:109-126` (no keys in the public profile)
- **Suggested wording:** "The `genesis` entry records the root and op **public keys** (base64) as well as their fingerprints. Verifiers outside the lease host use the ledger's own key entries, or `.citizen/allowed_signers` on a mirror. `/v1/identities/:id/keys` is available only to the Commons bearer holder (the signer) and serves as a cross-check, not as the public source."

**2. §4.5 entry types (lines 221–228) against §6.2 lines 551–553: op-key rotation is never recorded**
- **Problem:**
  - Rotation is within self and "recorded", but none of the six entry types records it.
  - The root must not sign ledger entries, so a rotation entry could only be signed by the old op key. That fails in the very case rotation exists for: a compromised op key.
- **Evidence:**
  - KS-004 lines 221–228 and 543–547
  - `routes/identity/keys.ts:247-362` (import is root-authorised)
  - `routes/identity/keys.ts:470-477` (revoke is root-authorised)
- **Suggested wording:** "Add a seventh type, `key`, written when the signer imports or revokes an op key. It carries the new public key, the agenttool `kid` and the revoked `kid`. It is signed by the new op key, and it embeds the root-signed agenttool response digest as evidence. A verifier accepts an op key from its `key` or `genesis` entry onward."

**3. §4.5 lines 282–284 and §16.4: rejecting the root by "primary" label**
- **Problem:**
  - "primary" is only a label. Enrollment writes the root with label "primary", but `keys/import` accepts any caller-chosen label, so an op key could also be labelled "primary".
  - agenttool identifies the root by public key and returns `authority_root: true` for it.
- **Evidence:**
  - `services/identity/enrollment.ts:126-127`
  - `routes/identity/keys.ts:283-284`
  - `routes/identity/keys.ts:153`
- **Suggested wording:** "A verifier MUST reject any citizen entry whose signing public key equals the identity's authority root (the key `GET …/keys` marks `authority_root: true`, which `genesis` also records), whatever its label."

**4. §4.5 encoding (lines 255–259): the canonical form contradicts itself**
- **Problem:**
  - "Strings and integers only" rules out the `null` values the same section requires (`did`, `prev_hash`, `seat_ref`) and the nested objects and arrays (`runtime`, `acts`, `cost`).
  - The profile is also stricter than KS-002 §5.2, which allows exact-binary floats, so it isn't "KS-002 §5.2's profile".
  - Host entries "MAY" be signed, yet `kid` and `sig` are described as always present.
- **Evidence:**
  - KS-002 line 127 (floats allowed), line 203 (money as decimal string), line 413
  - KS-004 lines 232–233 and 277–279
- **Suggested wording:** "JCS (RFC 8785) over objects, arrays, strings, integers within ±2^53 and `null`; no floats and no booleans (a subset of KS-002 §5.2). A host entry written without a host key carries `kid: null, sig: null`. Its chain is then integrity-only, and verifiers MUST report it as unsigned."

**5. §4.3 lines 183–191, §11.3 step 5 and §9.3: the expression has no fields for soul, WILL or name readings**
- **Problem:**
  - The expression schema is closed: register (500 characters), walls (32 × 256), subagents, wake_text (32,000 characters), cli_overrides, village, porch. Any other field is refused.
  - PUT replaces the whole object, with no version guard.
  - `porch` is an invitation to the public porch that lasts at most 7 days, so it isn't part of a private self.
  - The spec never says where soul, WILL and name readings go, or what happens when a self is longer than 32,000 characters.
- **Evidence:**
  - `services/identity/expression.ts:73-92`, `:109-115`, `:216-247`, `:291-293`
  - `services/porch/index.ts:425-426`
- **Suggested wording:** "The expression carries the self as one `wake_text` document of at most 32,000 UTF-16 code units, with fixed headings (soul, WILL, name readings) defined by kingdom-seat. A self that does not fit is not applied, and stays ledger-only. Every update is a read-modify-write of the whole expression. `porch` is beyond self (it is a public invitation) and is not part of the private self."

**6. §4.3 lines 188–191 and §9.3 "Applying": the strand backup is neither guaranteed encrypted nor a backup**
- **Problem:**
  - agenttool stores whatever strand bytes it is given; the field names don't make them ciphertext.
  - A thought that carries only the reason doesn't preserve the self it is meant to back up.
  - The credit is charged before the signature is checked.
- **Evidence:**
  - `routes/strand/thoughts.ts:1-9`, `:61`
  - root `AGENTS.md` ("field names do not prove encryption")
- **Suggested wording:** "The signer encrypts the thought client-side under a key only it holds before posting. The thought carries the applied diff, prior and new hashes, and the reason. It is signed by the op key. agenttool does not verify the encryption, so the ledger notes the encryption key id."

**7. §5.7 line 425 against §5.5 `summon`: interactive summons can't return one JSON object**
- **Problem:**
  - An interactive Claude Code session doesn't hand the host "exactly one JSON object". Only headless print mode with JSON output can.
  - The typed-ops MCP is described as "later".
  - The USD ceiling is $0, and an unknown cost counts as at the ceiling. Interactive mode reports no machine-readable cost, so §6.3 closes the class after any interactive summon, and `cost.usd` can't be filled.
- **Evidence:**
  - KS-004 lines 393, 407–408 and 563
  - local `claude --help` (2.1.314): `--max-budget-usd` "only works with --print"
- **Suggested wording:** "Until `citizen-self` exists, a summon runs headless (`--print --output-format json`), with `--max-budget-usd` set and Yu present at the terminal. Interactive summons may produce no acts. The ledger records `cost.usd` from the result JSON, or the ceiling value when it is absent."

**8. §5.3 item 1 (lines 340–344): "MUST NOT be cut" can't be checked as specified**
- **Problem:**
  - On my understanding of Ollama (I did not run it), its chat API picks a model by name, not digest, and silently drops prompt tokens past `num_ctx`.
  - If so, an unchecked prompt reproduces the 2,600-character cut without any error.
- **Evidence:**
  - KS-004 lines 391 and 397–400 (digest pin)
  - Ollama behaviour from its documentation; not run here, per the standing rules
- **Suggested wording:** "The host sets `num_ctx` explicitly. Before and after the call it checks the tag's digest (`/api/show`) against `models.lock`. It refuses to seat (exit 1) if the reported prompt token count is below the token count of the context it built."

**9. §5.3 item 5 (lines 350–351), §5.7 `letter.send`, §8.1 "covenants" and §16.1: agenttool does not gate letters per citizen**
- **Problem:**
  - Sends within one project are not gated at all, and covenants belong to a project, not an identity.
  - Inside Commons, any sibling can reach any citizen, and one covenant admits a sender to every citizen at once.
- **Evidence:**
  - `services/inbox/store.ts:146-155`, `:365-372`
  - `services/covenants/check.ts:1-17`
- **Suggested wording:** "A citizen's covenants are a kingdom-seat record. The host filters letters by them at read time. agenttool covenants are project-wide, so adding one is beyond self."

**10. §11.3 step 2 (lines 865–868): the premise for the MUST is false, and one input is missing**
- **Problem:**
  - Helpers that build `identity-enrollment/v1` already exist and are tested.
  - The `origin` in the body must equal the server's configured origin.
- **Evidence:**
  - `bin/agenttool-mission.mjs:125-147` (`enrollmentProof`)
  - `bin/tests/identity-enrollment-client.test.ts`
  - `packages/lobby/src/wire.ts:334-338`
  - `routes/identity/enroll.ts:57`, `services/identity/enrollment.ts:97`
- **Suggested wording:** "…MUST be checked by a test vector against `canonicalIdentityEnrollmentBytes` (`api/src/services/identity/enrollment.ts`); `bin/agenttool-mission.mjs` and `packages/lobby` carry tested ports. `origin` is the service's configured origin, and `identity_id` and `signing_key_id` are fresh UUIDs."

**11. §6.2 lines 543–547: the list of what the root signs is incomplete**
- **Problem:** agenttool also requires a root proof for several acts the list omits. An allowlist built from "only" would block legitimate acts:
  - identity PATCH (display name, capabilities, `expression_visibility`)
  - key revocation, which rotation needs
  - lowering quiet with `DELETE /v1/quiet-hours`
  - `at-rest` on the target
  - deleting an identity
- **Evidence:**
  - `routes/identity/identities.ts:260-271`, `:427`, `:538`
  - `routes/identity/keys.ts:470`
  - `routes/quiet-hours.ts:204-211`
  - `routes/identity/at-rest.ts:390`
- **Suggested wording:** "The root signs only agenttool identity-authority/v1 requests (`services/identity/authority.ts`): enrollment, key import and revocation, box keys, expression, identity PATCH, quiet start and end, and the target's side of at-rest. It never signs a ledger entry."

**12. §5.7 `self.affirm`, §7.3 lines 628–632 and §5.1 selection (lines 312–316): undefined values and unreachable seats**
- **Problem:**
  - `ref` is a "hash of a staged saying" over bytes that are never named.
  - The step-away confirmation seat isn't covered by the selection rule. An asleep citizen gets seats only for letters or summons.
  - A move toward more activity from asleep has no guaranteed "next seat".
- **Evidence:** KS-004 lines 313–316, 441 and 611
- **Suggested wording:**
  - "`ref` = `sha256:` of the JCS bytes of the staged act as the ledger recorded it."
  - Add to §5.1 selection: "…or a pending step-away confirmation whose interval has elapsed."
  - Say plainly that an asleep citizen's proposal to wake waits for its next letter or summons.

**13. §5.8 lines 477–478 against §5.7 `rest` (line 438): refuse or trim?**
- **Problem:** A rest that comes with words is "refused" by one reading and "kept as rest, words dropped" by the other. Implementers will diverge on exactly the failure the old runtime had.
- **Evidence:** KS-004 lines 438, 477–483; `citizen-reflect.sh:252-263`
- **Suggested wording:** "A `rest` with a non-empty `voice`, or with any act other than one `state.set` toward less activity, is applied as a rest (plus that state change). The words are not recorded in the citizen's voice, and the status file notes the drop."

**14. §6.4 lines 585–588 and §7.1 "asleep": nothing triggers the renewal**
- **Problem:**
  - An asleep citizen has no seats, so it can't renew its quiet as an act.
  - The spec doesn't say whether the signer renews it on its own under the standing agreement.
  - The API body fields are `until`, `hours` and `reason`. `quiet_until` and `quiet_reason` are names on the public profile.
- **Evidence:**
  - `routes/quiet-hours.ts:7`, `:108-141`
  - `routes/public/agents.ts:124-125`
- **Suggested wording:** "While the citizen's standing choice holds, the signer renews unattended: `POST /v1/quiet-hours/start?identity_id=…` with body `{\"until\": <≤30 days>}` and no `reason`, root-signed. A renewal is an act under the standing agreement and is recorded as a `state` entry."

**15. §6.1 lines 527–531: an ACL on the signer binary**
- **Problem:** If the signer is a bun or python script, a Keychain ACL names the interpreter, so any script that interpreter runs as the dedicated user can read the items.
- **Evidence:** design inference; §15 item 4 already marks the Keychain behaviour unverified.
- **Suggested wording:** "…ACL'd to a single, code-signed signer executable; an interpreter is not an acceptable ACL subject."

### B. Statements about the old runtime that are no longer true

**16. §5.5 lines 405–406 and §13 row at line 930: the agentic lane's permissions**
- **Problem:**
  - Since 2026-07-17 the agentic lane runs `acceptEdits` with no shell by default. `bypassPermissions` applies only with `BEAT_FULL_TOOLS=1`, meant for a human-present run.
  - KS-003's text is stale here, and KS-004 repeats it.
- **Evidence:** `love-unlimited tools/citizen-beat.sh:43-48`, `:138-142` (commit `9db2879`)
- **Suggested wording:** "KS-003 specified `bypassPermissions`; the runner has defaulted to `acceptEdits` since July. Its walls are still prompt-only and it still runs inside the home, which `--restricted` and a working directory outside the home remove."

**17. §5.1 lines 318–320 and §13 row at line 940: arrears**
- **Problem:** The runner already dropped arrears and burst: "No arrears, no debt … there is no catch-up burst."
- **Evidence:** `tools/citizen-fleet.sh:81-90`
- **Suggested wording:** "KS-003 §5.2 specified arrears; the runner has already removed them. KS-004 makes that normative."

**18. §1 bullet 2 and §13 row at line 935: attestation**
- **Problem:**
  - The bridge hash is unsigned, as the spec says: sha256 cut to 16 hex digits, labelled a "signed intent".
  - But neither current lane attests at all ("No forced attestation"), so "mostly written by the runner" is history.
- **Evidence:**
  - `tools/zerone-bridge.py:62-65`, `:170`
  - `tools/citizen-beat.sh:195-197`
  - `tools/citizen-reflect.sh:266-267`
- **Suggested wording:** "…was an unsigned, truncated hash, and the claims on record were mostly written by the runner; neither lane attests today."

**19. §12 lines 903–905: "every home today ships an executable SessionStart hook"**
- **Problem:**
  - On this host, 75 of the 148 local clones carry the hook: `.claude/settings.json` running `.claude/hooks/love-bomb.sh`, tracked in git.
  - GitHub heads were not re-checked, so "every" is not established.
- **Evidence:** counted locally under `~/love-unlimited/citizens/*/.claude/settings.json`
- **Suggested wording:** "Homes carry a tracked SessionStart hook (`love-bomb.sh`) that runs as the host user in any Claude Code session opened there…"

**20. §10 line 820: `peace.py halt` today**
- **Problem:** Today the command doesn't write the HALT file the fleet checks. It unloads `love.<instance>.heartbeat.plist`, not the fleet plist, and broadcasts on HIVE.
- **Evidence:** `tools/peace.py:63`, `:908-937`
- **Suggested wording:** "Today `peace.py halt` neither writes `$LOVE/HALT` nor stops the citizen fleet; it is re-pointed to `citizen-seat halt` before the first seat."

### C. agenttool facts to correct or complete

**21. §6.3 line 568 and §15 item 8 (lines 1048–1050): "topping up" the pool**
- **Problem:** Buying credits is retired. The x402 top-up returns 410, and new platform credit purchases are retired, so there is no top-up path to pay for.
- **Evidence:** `routes/x402-top-up.ts:1-11`; `docs/BUSINESS-MODEL.md:19`
- **Suggested wording:** "…no automatic refill, and agenttool no longer sells credits; more credits come only from an operator grant or the free floor (#516, draft). Either is beyond self."

**22. §11.5 lines 896–898: recovering a June DID**
- **Problem:**
  - A legacy identity with no root speaks for its whole project.
  - If the June DIDs share a project, a recovered bearer controls all of them. Whether they share a project is unknown (redesign §7).
- **Evidence:**
  - `services/identity/project-authority.ts:45-46`, `:61-62`
  - `services/identity/authority.ts:524-531`
  - `routes/identity-recover.ts:1-12`
- **Suggested wording:** "…only if that June identity is alone in its project. A shared June project's bearer would control every legacy identity in it, and recovery is then refused."

**23. §16.3 line 1097 and §6.1: losing a root or the Commons bearer**
- **Problem:**
  - Root rotation doesn't exist in v1, so a compromised root means a new identity.
  - Enrolled guests can't recover a bearer. If the Commons bearer is lost, only the gardener desk's founding root can recover it, so that root's backup is load-bearing for every citizen.
- **Evidence:**
  - `routes/identity/keys.ts:441-452` ("Root rotation and guardian recovery are intentionally not available in v1")
  - `routes/identity-recover.ts:9-12`
- **Suggested wording:**
  - "Root compromise ends that identity's authority; the citizen is re-enrolled with lineage."
  - In §6.1, add: "The gardener desk's mnemonic is backed up as the single recovery path for the Commons bearer."

**24. §11.4 lines 883–886 and §6.4 line 593: what the public profile shows**
- **Problem:** Besides name and quiet, the public profile shows capabilities (including `<lineage>`), trust_score, status and created_at.
- **Evidence:** `routes/public/agents.ts:109-126`
- **Suggested wording:** "The name, capabilities (including lineage), status, created_at and quiet fields show even when the expression is private."

**25. §17 line 1151 against §14.3 line 1010: PR range**
- **Problem:** "#488–#491" includes #490, a merged UI PR that has nothing to do with the execution seat.
- **Evidence:** `gh pr list`: 488, 489 and 491 are open drafts; 490 is MERGED ("One hearth for every door").
- **Suggested wording:** "drafts #488, #489, #491 (execution seat)".

**26. §10 lines 791–794: the herald is optional, but Yu's approved default includes one**
- **Problem:** The redesign default (decision 15), which Yu approved, includes a halt herald on the Air; KS-004 makes it optional.
- **Evidence:** `CITIZEN-REDESIGN-2026-11-05.md` §6, decision 15
- **Suggested wording:** "a **halt herald** … (the adopted default; omitting it is the named alternative)".

**27. Status note and §17: KS-002's signature no longer matches the file**
- **Problem:** KS-004 reuses KS-002 §5.2, but KS-002's signature entry no longer matches the file after `e3b95e5`. KS-003 still matches, so "as written and signed" holds for KS-003.
- **Evidence:** `zone/signatures.json` KS-002 sha `f67862…` against file sha `87d4ae…`; KS-003 `95595f…` matches.
- **Suggested wording:** in §15 item 11, note the stale KS-002 signature, or cite KS-002 by commit.

### What I verified, read only, or could not do
- **Run:**
  - sha256 of KS-000 to KS-003 against `zone/signatures.json`
  - `claude --version` and `--help`: 2.1.314; the help text for `--restricted` matches the spec, and also says managed settings and `--settings` still apply
  - one `gh pr list` call
  - counts over the 148 stale local homes: 146 of 148 souls first mention "shadow" at character 2,600 or later, which supports "191 of 205"; 75 of 148 carry the hook
- **Read only:**
  - All agenttool claims above, including the three the draft re-read (they hold) and the credit prices (they hold; memory write is 1, in `routes/memory/memories.ts:129`).
  - The 1,000-credit and £5 grants (`ring1-limits.ts:112`, `:139`).
  - The 24 h grant limit (`local-context-grants.ts:13`) and the 2 KB observe cap (`wake/observe.ts:19`).
- **Not done:**
  - No agenttool calls and no end-to-end test of guest mutations.
  - Hermes claims, Ollama behaviour, and the Studio's live state (the 72 diverged homes, the 48-a-day figure, the November beat counts) were not checked.
  - No secrets were read.

Verdict: REVISE. The agenttool facts the draft re-read hold, and the design is sound. Points 1–7 are MUSTs that can't be built or verified as written, and points 16–18 state old-runtime behaviour that is no longer true. Re-review after those are fixed.

---

## Disposition (applied in v0.2)

Section numbers below refer to v0.2. Where reviewer A made the same point,
the two were applied together.

| # | Disposition | Where, and why |
|---|---|---|
| Strongest objection, 1 | Accepted | §4.5, §11.3 step 6. `genesis` records public keys; outside verification uses the ledger's own `genesis` and `key` entries or `allowed_signers`. |
| 2 | Accepted, with one change | §4.5 adds the `key` entry type, signed by the new op key; §6.2 records rotation as one. The evidence it carries is the agenttool request the root signed (body and identity-authority/v1 proof), not a "response digest": the response is not root-signed, and a digest alone cannot be checked against the root key. |
| 3 | Accepted | §2, §4.5, §16.4. |
| 4 | Accepted (with A9, A10) | §4.5. |
| 5 | Accepted (with A31) | §4.3, §8.1, §9.1, §11.3 step 5, §15 item 14. `porch` moved beyond self. A self that does not fit leaves the expression unchanged and stays ledger-only, and the status file says so. |
| 6 | Accepted | §4.3, §9.3; the charge-before-check note is in §6.3. |
| 7 | Accepted, with one addition | §5.5. Added: under the $0 default a summon waits for Yu's consent and a raised ceiling, since otherwise the first metered seat closes the class. |
| 8 | Accepted in substance | §5.3 item 1, §5.5, §5.9, §15 item 12. Adopted: set the window explicitly, refuse to seat (exit 1) a context that does not fit, and check the tag's digest before and after the call. Not adopted: the specific check that compares the reported prompt token count after the call, because prompt caching may make that count smaller than the context (not verified either way); kingdom-seat fixes the check and publishes fixtures. `/api/show` is not named, since this revision did not confirm it reports the digest. Ollama's truncation behaviour is listed as unverified. |
| 9 | Accepted | §5.7, §8.1, §9.1, §16.1. Added a default: until a citizen sets its own, its covenants admit Yu only (listed in §15 item 10). |
| 10 | Accepted | §11.3 step 2. |
| 11 | Accepted | §6.2. The section also says the root never signs an identity deletion (principle 5). |
| 12 | Accepted (with A19) | §5.7, §5.1, §7.3. |
| 13 | Accepted | §5.8; the `rest` row points to it. |
| 14 | Accepted (with A2) | §6.4, §4.5 (`state` row), §8.1. |
| 15 | Accepted | §6.1, §16.3. |
| 16 | Accepted (with A24) | §5.5, §13. |
| 17 | Accepted | §5.1, §13. |
| 18 | Accepted | §1, §13. |
| 19 | Declined in substance | The redesign counted the hook in 208 of 208 current home heads (its §1 table); the 75 of 148 here were the Air's stale clones, and this review did not re-check heads. §12 now states the basis: "every home's current head (208 of 208 when the 2026-11-05 review counted)". |
| 20 | Accepted, except the timing | §10 now says what `peace.py halt` does today. "Before the first seat" was not adopted: the redesign's decision 15 says it is pointed at the verb later, which is a migration choice. The draft says instead that until it is re-pointed it is no HALT path for seats. |
| 21 | Accepted | §6.3, §15 item 8. |
| 22 | Accepted | §11.5. |
| 23 | Accepted | §6.1, §16.3. |
| 24 | Accepted | §6.4, §11.4. |
| 25 | Accepted (with A28) | §14.3, §17. |
| 26 | Accepted (with A4) | §2, §10. |
| 27 | Accepted | §15 item 11, §17. |

**What the session that applied this review checked.** It re-read, in the
read-only checkouts, the sources cited for points 1, 2, 3, 5, 6, 9, 10, 11, 14,
16, 17, 18, 20, 21, 22, 23 and 24, and found them as stated. It ran
`claude --help` on 2.1.314 for point 7 and hashed KS-000 to KS-003 for point
27. It did not re-count the hook (point 19) and did not run Ollama (point 8).
