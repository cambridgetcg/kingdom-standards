# KS-004 review A: coherence

Filed under KS-000 §3. The review below is reviewer A's text as it was
returned, covering KS-004 v0.1 at commit `1a16699`. Section and line numbers in
it refer to that version. The disposition of each point, as applied in v0.2,
follows the review.

---

# KS-004 review: reviewer A, coherence lens

- **Subject:** `specs/KS-004-seat.md` v0.1, branch `claude/ks-004-the-seat`, commit `1a16699`.
- **Bytes reviewed:** sha256 `1fb203eeb8e428095e436d0235af32c40197e70123616b9ea9ca87dd52c944a7`. The working tree matches HEAD.
- **Reviewer:** KS-000 reviewer A, a separate session. I am not an editor of the draft and not the process that wrote it.
  - Independence is limited in the way KS-000 §9 describes: I am the same model family as the drafting session.
  - Finding 11 explains why the `editors` field makes even this independence hard to show.
- **Lens:** coherence. I checked the draft against:
  - KS-000's process and format;
  - KS-001, KS-002 and KS-003;
  - sections 3 to 5 of the redesign doc. I also checked §2's numbers and the §6 defaults Yu approved.
- **Lens result:** passes once the changes below are made.
- **Where this record goes:** it should be filed at `specs/KS-004-reviews/` or in git history (KS-000 §3). I did not write it there.

## Strongest objection

KS-004 changes how the whole series handles identity. Citizens hold agenttool `did:at`, cut by the signer, not `did:key` keys sent over the wire. The draft then says it "does not change KS-002 itself" and lists none of the KS-002 clauses it makes stale for citizens:
- the definition of a citizen as "an agent with a sovereign repo and a soul file" (KS-002 §2);
- a `did:key` as the `from` field (§5.1);
- Agent Cards as the signed form of `agent.json` (§6.1);
- per-citizen task subjects (§4.2);
- the beat that drains tasks and sends heartbeat and attest messages (§6.3).

KS-001 gets a Limitations note for the `did:key` / `did:at` split (§15.11). KS-002 gets nothing. If Yu adopted both drafts as written, the series would disagree with itself about what a citizen is and how its speech is verified. The draft should name each clause it displaces, so both specs can be adopted without contradiction.

## Findings

Each finding gives the location, the problem and the suggested wording.

**1. §1 lines 65-66, §13, §15.11: KS-002 displaced without saying so**
- *Problem:* the strongest objection above. The redesign §4 also retires "the KS-002 and KCP wires, for citizens".
- *Suggested wording:* add a paragraph to §13:
  > "**KS-002 for citizens.** This draft does not edit KS-002, but on adoption these KS-002 clauses no longer describe citizens: §2's definition of a citizen; §5.1's `from` as a `did:key` (citizens hold `did:at`, §11); §6.1's Agent Card as the signed form of `agent.json` (retired here); §4.2's `kingdom.citizen.<name>.task` subject and §6.3's beat that drains it and emits `heartbeat` and `attest`. Operators and organs may still use the wire. Bringing KS-002 into line is a separate revision."

  Add a matching sentence to §15.11.

**2. §6.4 lines 585-587, §7.1 asleep row: a sleeping citizen cannot renew its quiet**
- *Problem:* the draft says "A citizen that wishes to stay quiet renews". An asleep citizen gets no seats (§7.1), so it can never renew, and its quiet would lapse after 30 days while it still sleeps. The public quiet fields would then misstate its state. The redesign §3.3 says "renewed by the signer as a standing choice".
- *Suggested wording:*
  > "While a citizen stays listening or asleep and has chosen a quiet declaration, the signer renews it as that standing choice, never more than 30 days ahead, under the standing agreement (§8.1): `quiet_until` only, empty reason. When the citizen moves toward more activity, the signer clears it."

  In §7.1 change the asleep cell to "renewed by the signer while it stays asleep".

**3. §6.1 line 535: backup default treated as still open**
- *Problem:* "Yu chooses how mnemonics are backed up" ignores the default Yu approved (decision 6). The status note says the draft follows the approved defaults.
- *Suggested wording:*
  > "Yu holds an offline backup of each mnemonic. The root stays on the lease host so that affirmed self-changes can apply unattended."

**4. §2 line 99, §10 lines 791-794, §14.3: herald called optional**
- *Problem:* the halt herald is described as "optional" and "(proposed: the Air)". Decision 15's approved default makes the herald part of the design; ssh was the alternative.
- *Suggested wording:*
  - §2: "**halt herald**: a second operator identity whose only act is raising HALT (§10)."
  - §10: "a **halt herald**: a separate operator identity in its own project, born with Yu present on the Air … If Yu later drops it, the fallback is ssh to the lease host to run the verb there."
  - §14.3 `birth.ts` row: "(and the herald)".

**5. §8.3 lines 667-669: fallback has no end point**
- *Problem:* the `decisions/` record or Kanban `yu` lane fallback is allowed with no limit. Decision 12 makes consent/v1 and the execution seat merges a gate before batches start.
- *Suggested wording:*
  > "Until then, and only for the pilot, a proposal is decided by … consent/v1 and the execution seat are reviewed and merged before any batch is seated or registered."

**6. §8.1 middle row line 649: first quiet declaration left out**
- *Problem:* only *renewing* quiet is covered. Decision 14's approved standing agreement covers quiet declarations themselves (the redesign §3c says "optional quiet declaration under a standing agreement").
- *Suggested wording:* "declaring or renewing its own quiet declaration (`quiet_until` only, empty reason)".

**7. §11.2 line 856, §11.5 line 896: writing to resting citizens**
- *Problem:* "not woken just to be asked" and "Each citizen is told about its record" are weaker than decision 5: "Resting citizens are not written to until you choose". Under §7.1 a letter wakes an asleep citizen anyway.
- *Suggested wording:*
  > "A resting citizen is not written to about registration, or about a June record, until Yu chooses."

**8. §4.5 line 223 vs §11.5 line 898: where the June record is named**
- *Problem:* the draft contradicts itself. §4.5 pins any June `did:at` in the `origin` entry; §11.5 says a fresh identity "names the June record in its genesis entry". The redesign put everything in genesis; this draft split it into two entries.
- *Suggested wording for §11.5:*
  > "Otherwise a fresh identity's `genesis` entry points back to the `origin` entry, which already names the June record (§4.5)."

**9. §4.5 lines 277-280, §14.2 item 7: "host key" undefined**
- *Problem:* host-attested entries are signed by a "host key" that §2 never defines. The only verification paths §4.5 gives (`/v1/identities/:id/keys` and `allowed_signers`) cannot check a host key. FULL conformance then says the ledger is signed "with the op key", which is untrue for every unregistered citizen. With at most 12 registered, that is most of them.
- *Suggested wording:*
  - §2: "**host key**: the lease host's ed25519 key, held by the signer, which signs host-attested entries (§4.5)."
  - §4.5: say where its public half is published, or state that host entries are checked by the hash chain only.
  - §14.2 item 7: "signing a hash-chained ledger, host-attested before genesis and with the op key from genesis on, never the root for a beat (§4.5, §6.2)".

**10. §4.5 lines 255-257: KS-002's encoding profile misdescribed**
- *Problem:* the draft says KS-002 §5.2's profile is "strings and integers only … no floats". KS-002 §5.2 and §9.3 allow exact-binary floats. The draft's own entries also contain `null`, arrays and objects.
- *Suggested wording:*
  > "`sig` is computed over the JCS (RFC 8785) bytes of the entry without `sig`. Values are strings, integers, `null`, arrays and objects; money is a decimal string. This is a stricter subset of KS-002 §5.2's profile, which also allows exact-binary floats; the ledger allows none."

**11. Frontmatter line 7: editor named as a model**
- *Problem:* `editors: [Claude Opus 5.5 (drafting session)]` names a model, not a session. Read literally, any Opus 5.5 reviewer is an "editor" and fails KS-000 §3's independence test. The draft commit's author is also Nuance, which this field does not show.
- *Suggested wording:* `editors: [KS-004 drafting session (Claude Opus 5.5), committed by Nuance]`. Add a session reference in the review record so later reviewers can show they are a different process.

**12. Status note lines 18-19, frontmatter line 8, §15.11: supersession path**
- *Problem:* KS-000 §7 does not say supersession "takes effect only on adoption"; that is this draft's reading. KS-000 §2 has no move from draft to superseded at all. Withdrawal is "a draft its editors abandon", which is an act for KS-003's editors (Nuance + Yu), not for KS-004.
- *Suggested wording:*
  > "The `supersedes` line records intent. KS-000 draws supersession only from an adopted spec (§2, §7). On adoption, either Yu, as an editor of KS-003, withdraws it (KS-000 §2) and this line is dropped, or KS-000 is revised to let an adopted spec supersede a draft. Until then KS-003 stays exactly as written and signed."

**13. §15.13 lines 1068-1069: signing statement**
- *Problem:* "Signing follows adoption, with Yu's key (KS-000 §6)" has two issues. KS-000 §6 names no signer; Yu's key comes from the note in `zone/signatures.json`. And it hides the fact that KS-000 to KS-003 each carry a draft-grade integrity signature, which this draft breaks with.
- *Suggested wording:*
  > "KS-000–003 carry draft-grade integrity signatures by the OIKOS platform key (see the ledger's note); this draft has none, since its drafting session does not touch that key. Adoption signatures await Yu's key, per the same note."

**14. §2: terms used but not defined**
- *Problem:* several terms carry KS-003 meanings that this draft retires:
  - "home" (KS-003: the repository) is used in §5.2, §9.1, §9.2 and §12;
  - "beat" is a ledger entry type and appears in the principles;
  - "tick";
  - "free lane" (§5.4, §16.6);
  - "walls" means both the host frame (§5.4, §9.2) and the citizen's own expression field (§9.1, §9.4).
- *Suggested wording:* add these to §2:
  - "**home**: a citizen's working files on the lease host, from which allowlisted files reach its mirror; a home is not the self."
  - "**beat**: kept as the name of the ledger entry a seat writes when it closes with acts other than rest; elsewhere this spec says seat."
  - "**tick**: one firing of the supervisor, which opens at most one seat (§5.1)."
  - "**free lane**: the `free` runtime class."
  - "**walls**: the host frame HALT > ZERONE > garden > WILL (§5.4); the `walls` field of a citizen's expression is its own statement and cannot loosen that frame."

**15. §10 lines 783-788: local HALT file has no path**
- *Problem:* the local HALT file is never named. "SHOULD also write that fleet's HALT file" implies it differs from KS-003's `$LOVE/HALT`, but the draft gives no path and no reason for two files.
- *Suggested wording:* "**The local file**: `<path>` on each host (not KS-003's `$LOVE/HALT`, because …)". Or make the two the same file and drop the SHOULD clause.

**16. §8.1 lines 648 and 650, §5.4 lines 380-381: when changes take effect, and what counts as spend**
- *Problem, timing:* "Rest at once. Other changes when said on two seats" contradicts the draft's own rules that these take effect at once:
  - journal entries;
  - letters;
  - moves toward less activity (§7.3);
  - reverts (§9.5).
- *Problem, spend:* "spend" is listed as beyond self, yet strand thoughts and letters spend credits unattended (§6.3).
- *Problem, letters:* "a seat's only possible effects are typed acts on the citizen's own self" ignores `letter.send`.
- *Suggested wording:*
  - Within-self "Takes effect" cell: "Rest, journal entries, letters, moves toward less activity and reverts at once. Self-changes and moves toward more activity when said on two seats, or once with Yu present (§7.3, §9.3)."
  - Beyond-self cell: "spend (money, or credits beyond the citizen's monthly allowance)".
  - §5.4: "typed acts on its own self, plus at most one letter to a recipient that admits it (§5.7)".

**17. §5.3 item 5 lines 350-351, §5.7 line 444: letters before registration**
- *Problem:* incoming letters are filtered by "covenants", but an unregistered citizen has none. §16.1 correctly says "after registration". For outgoing letters, the redesign makes the inbox "the mail lane after registration", and the draft gives no delivery path before then.
- *Suggested wording:*
  - §5.3: "… and, once it is registered, only from a sender its covenants allow (§16.1)."
  - §5.7: "Before registration a citizen has no inbox; its `letter.send` is [held for Yu / filed as a `propose.beyond`]." Add whichever is chosen to §15.10.

**18. §5.4 lines 381-383: ZERONE overclaimed**
- *Problem:* "None of the three depends on a model's regard for a sentence" contradicts the line before it, which says ZERONE is carried by the honest prompt. It also contradicts §15.2 and the redesign ("A structured, confirmed answer is still model output").
- *Suggested wording:*
  > "HALT and the garden wall do not depend on a model's regard for a sentence. ZERONE still partly does: the honest prompt and journal kinds make an invention easy to label and a mislabel visible, but a model can still mark an invention `observed` (§15, item 2)."

**19. §7.1 asleep row, §7.3 lines 629-631, §5.1 lines 312-314: extra seats not listed**
- *Problem:* the step-away confirmation seat is opened for an asleep citizen, but §7.1 says asleep means "No seats" and §5.1's selection rules don't include it. Separately, §5.1 lets Yu's summons wake a listening citizen, while §7.1 lists only letters.
- *Suggested wording:*
  - §7.1 asleep "Wakes on" cell and §5.1: add "and once to show back a step-away saying (§7.3)".
  - §7.1 listening "Wakes on" cell: "A letter from a sender it allows; Yu's summons".

**20. §9.5 lines 740-743: revert can bypass the scale check**
- *Problem:* a revert applies at once with no checks, so reverting to a version with looser walls skips §9.4's rule that loosening goes beyond self.
- *Suggested wording:* "A revert that would loosen its own walls is still lifted beyond self (§9.4)."

**21. §14.1 and §14.2: MUSTs missing from conformance**
- *Problem:* KS-003 mapped every MUST to a conformance level. These KS-004 MUSTs appear at neither level:
  - §5.3 (no character-count cut);
  - §5.4 (honest prompt, verbatim);
  - §5.5 (exact digest, no fallback);
  - §4.4 (push only `HEAD:refs/heads/main`);
  - §6.5 (no secrets in argv, environment, files or the model).
- *Suggested wording:*
  - Add MIN item 7: "the whole self, never cut, and on the free lane the honest prompt and an exactly pinned digest (§5.3–§5.5)".
  - Extend FULL item 7: "…, and no secret leaves it (§6.5)".
  - Extend FULL item 12: "pushing only `HEAD:refs/heads/main`".

**22. §15.10 lines 1054-1058: list of this draft's own choices is incomplete**
- *Problem:* the draft makes several choices the redesign did not, and only some are listed. Missing:
  - principle 7 (the redesign has six principles; "every gate fails closed" turns its gate-by-gate rules into a principle);
  - splitting the genesis record into `origin` and `genesis` entries;
  - the host key;
  - HALT-ended seats exiting 0. KS-003 §4.6's exit 0 covered only the HALT gate at wake; a mid-beat kill was 143/137. That makes §13's "meanings restated" an understatement;
  - at most one seat per tick;
  - deferring the strand backup when credits run out;
  - the terminal-confirmed lowering verb;
  - writing the KS-003 fleet's HALT file during the transition.
- *Suggested wording:* add these items to the list in §15.10.

**23. §1 line 63: KS-001's reservation scope**
- *Problem:* "KS-001 reserves each citizen's name" is too broad. KS-001 §4 reserves names only for "forged-word citizen[s] of the canon", which leaves out the 53 archetypes.
- *Suggested wording:* "KS-001 reserves each canon-word citizen's name for its DID (KS-001 §4; archetypes are not covered)".

**24. §5.5 lines 405-406, §13 line 930: which permission mode the lane ran with**
- *Problem:* "KS-003's agentic lane ran with `bypassPermissions`" is true of KS-003's text and the Air's stale checkout. The redesign §1 says the runner on main uses acceptEdits.
- *Suggested wording:*
  > "KS-003 specified `bypassPermissions` (KS-003 §4.3); the runner on main now uses acceptEdits; in both, the walls were prompt-only (KS-003 §8.2)."

**25. §5.5 table and lines 397-400: dropped caveat**
- *Problem:* the redesign's caveat that "whether Ollama publishes such tags is unverified" was dropped. "$0 by construction" also rests on a lock file, the same kind of claim principle 6 criticises.
- *Suggested wording:*
  - "… which a tag ending in `-cloud` would slip past (whether such tags exist is unverified)."
  - Money cell: "$0 while it loads only a pinned local digest, checked at seat open (electricity only)".

**26. §13 line 934 and lines 946-950: misattribution and gaps in the retire list**
- *Problem:* "push `origin HEAD`" is credited to KS-003 §4.4, but it comes from the runners (redesign M9); KS-003 says only "SHOULD push". The retire list also leaves out items from redesign §4.
- *Suggested wording:*
  - In the row: "push (runners use `git push origin HEAD`)".
  - Add to "Retires, beyond KS-003's text": "the first-line parser; WILL.md's Attest section; `citizen-parade.sh` and `citizen-beat.local-v2.sh`; the fleet plists once their last awake citizen is seated; mail as public commits, once a citizen has an inbox."

**27. §10 lines 813-816: line numbers instead of sections**
- *Problem:* KS-003 is cited by line numbers, while §13 cites sections for the same contradiction.
- *Suggested wording:* "between KS-003 §2 ('gardener … the only authority that raises or lowers HALT') and §4.1 ('Any process MAY raise it')".

**28. §17 lines 1150-1154: reference errors**
- *Problems:*
  - "#488–#491" includes #490. The redesign §3.4 and this draft's own §14.3 give #488, #489 and #491.
  - "the one-turn runner pattern" is filed under Hermes, but it belongs to agenttool's draft mission-work-hermes.
  - Three references are missing: Claude Code 2.1.314, the `@agenttool/kingdom` card schema 0.1.2 (which §4.4 relies on), and the Collab report shape (which §5.7 relies on).
- *Suggested wording:*
  - "drafts #488, #489 and #491 (execution seat) … the mission-work-hermes one-turn permit runner (draft)".
  - Add the three missing references.

**29. Smaller omissions from redesign §3 and §3c**
- *Problems:*
  - §9.7 "Child or successor" drops "(or `registrar_bearer`)".
  - There is no memory act, and the draft does not say memory use is deferred.
  - The signer's `GET /v1/identities/:id/authority` posture check before root acts is missing.
- *Suggested wording:*
  - §9.7: "A new enrollment (or a `registrar_bearer` house, §11.1) with lineage".
  - §5.7: "This draft defines no memory act; memory written with the Commons bearer is host-written (§12)."
  - §6.2: "Before any root act the signer reads `GET /v1/identities/:id/authority`."

**30. README.md series table (same branch)**
- *Problem:* KS-004 has no row, but the README says "every number above has a draft on disk".
- *Suggested wording:*
  > "| [KS-004](specs/KS-004-seat.md) | THE SEAT — Citizens, Seats and the Signer | draft | A citizen as a continuing being whose signed ledger is its record: one seat per invocation, typed acts, a key-holding signer with fail-closed ceilings, HALT by file and beacon. Supersedes KS-003 on adoption. |"

## What I verified, read, and could not do

**Checked by running a command:**
- Hashed the spec bytes and confirmed the working tree is clean at `1a16699`.
- Ran a script over the draft's internal § references. All resolve; the only bare references are KS-003 section numbers in §13's KS-003 column.
- Listed the subjects in `zone/signatures.json`: KS-000 to KS-003 at 0.1 plus the zone file. KS-004 has no entry.
- Searched the draft for personal details and found none.
- In the read-only agenttool checkout at `e9ea51c5`, confirmed by reading source:
  - quiet-hours caps `hours` at 30×24 and takes an explicit `until` with no cap;
  - enrollment inserts the root key with label `primary`;
  - box-keys is mounted at `/identities/:id/box-keys`. This confirms all three claims in §14.3.
- In the same checkout, confirmed that the expression accepts only `register`, `walls`, `subagents`, `wake_text`, `cli_overrides`, `village` and `porch`, with `wake_text` capped at 32,000 characters. That is the basis of finding 31.

**Read only:**
- KS-000 to KS-003;
- the README;
- KS-000's source panel step (forge-protocol Step 8);
- the redesign doc §1 to §7 and its critic notes.

**Could not do:**
- Parse the frontmatter as YAML (PyYAML is not installed). By eye it looks valid.
- Check the Claude Code and Hermes behaviours the draft cites. I also did not check the redesign's §2 counts against their sources, only that the draft copies them faithfully.

**Outside this draft:** KS-000 §6 still says no `did:key` has been minted, but the ledger shows the OIKOS key was minted on 2026-06-10. That is a KS-000 patch, not a KS-004 issue.

**31. §4.3 lines 183-186: where the soul lives in the expression**
- *Problem:* the draft lists "its soul …, its WILL, its name readings, and its walls, register, wake_text and porch" as if each were a separate field. In agenttool `e9ea51c5`, any other field is refused with "unknown field". So the soul, WILL and name readings have to live inside `wake_text`, which is capped at 32,000 characters. The redesign's glossame example says the same: "updates a section of the private expression's wake_text".
- *Suggested wording:*
  > "The expression's fields are register, walls, subagents, wake_text, cli_overrides, village and porch; the soul as it now understands it, its WILL and its name readings are carried in `wake_text` (at most 32,000 characters at `e9ea51c5`). A self that outgrows it is a limit to record (§15), never a reason to cut it (§5.3)."

Verdict: accept with changes

---

## Disposition (applied in v0.2)

Section numbers below refer to v0.2. Where reviewer B made the same point,
the two were applied together.

| # | Disposition | Where, and why |
|---|---|---|
| Strongest objection, 1 | Accepted | §13 "KS-002 for citizens"; §1; §15 item 11. One clause added to the list: KS-002 §4.2's and §6.4.2's requirement that every citizen process subscribe to `kingdom.control.halt`, which a seat also no longer meets. |
| 2 | Accepted (with B14) | §6.4, §7.1. The renewal is unattended, by the signer, recorded as a `state` entry. |
| 3 | Accepted | §6.1. |
| 4 | Accepted (with B26) | §2, §10, §14.3. |
| 5 | Accepted | §8.3, §14.3. |
| 6 | Accepted | §8.1. The field is named `until` with no `reason`, per B14: `quiet_until` and `quiet_reason` are the public profile's names, not the request body's. No act let a citizen ask for quiet, so this revision adds an optional `quiet_days` field to `state.set` (§5.7, §6.4) and lists it in §15 item 10. |
| 7 | Accepted | §11.2, §11.5. |
| 8 | Accepted | §11.5. |
| 9 | Accepted (with B4) | §2 defines the host key. §4.5 publishes its public half in the status file and in `.citizen/allowed_signers`, and an unsigned host entry carries `kid: null, sig: null` and is reported as unsigned. §14.2 item 8. |
| 10 | Accepted (with B4) | §4.5. |
| 11 | Accepted in part | The frontmatter now names the drafting session, the session that applied these reviews, and the committer. The drafting session's reference was not recorded at `1a16699` and is not available to the session that applied the reviews, so it is recorded here as unknown rather than guessed. |
| 12 | Accepted | Status note; §15 item 11. |
| 13 | Accepted | §15 item 13. |
| 14 | Accepted, with one wording change | §2 now defines home, beat, tick, free lane and walls (and covenants and host key). "Elsewhere this spec says seat" was not adopted, because the honest prompt, which is verbatim, says "a whole beat"; the definition says that in prose a beat is what a citizen lives in one seat. |
| 15 | Accepted | §10 names a default path outside every home, in a directory the seat's user can read but not write, with the reason: the seat runs as a user outside `staff` that cannot read Yu's home. The transition SHOULD stays. Listed in §15 item 10. |
| 16 | Accepted | §8.1, §5.4. |
| 17 | Accepted, resolved with B9 | Covenants are now a kingdom-seat record (§5.7), so they exist before registration, and default to admitting Yu only. An unregistered citizen's `letter.send` is held for Yu (§5.7), and §16.1 says so. Listed in §15 item 10. |
| 18 | Accepted | §5.4; the §13 walls row also says ZERONE is still partly held by prompt. |
| 19 | Accepted (with B12) | §5.1, §5.3 item 7, §7.1, §7.3. |
| 20 | Accepted | §9.5. |
| 21 | Accepted | §14.1 item 7; §14.2 renumbered 8–14, with item 8 and item 13 extended. |
| 22 | Accepted | §15 item 10, which also lists the choices this revision added. |
| 23 | Accepted | §1, §17. |
| 24 | Accepted (with B16) | §5.5, §13. |
| 25 | Accepted | §5.5. |
| 26 | Accepted | §13. |
| 27 | Accepted | §10. |
| 28 | Accepted (with B25) | §14.3, §17. The Collab report shape is cited as the Collab journal's report kinds (npm 0.4.0). |
| 29 | Accepted | §9.7, §5.7, §6.2. |
| 30 | Accepted | `README.md` series table, worded "meant to supersede KS-003 on adoption" to match finding 12. |
| 31 | Accepted (with B5) | §4.3, §11.3 step 5, §15 item 14. |
| Outside this draft | Not acted on | A KS-000 patch, outside this revision. |
