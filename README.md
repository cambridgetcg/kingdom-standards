# KINGDOM STANDARDS (KS)

**The Kingdom writing its own internet the way the internet was actually written: specs + running code.**

The original internet was not legislated into existence. It was written — one
numbered memo at a time, each backed by an implementation someone could run
that evening. The KS series does the same for the Kingdom: Yu's sovereign
network of citizens, organs, and works (the YOUSPEAK cathedral, the
love-unlimited fleet, the OIKOS platform). Every KS is a draft until Yu adopts
it, and every KS that claims a wire format ships, or names, the code that
speaks it.

This repository is the protocol layer's home: `specs/` for the documents,
`impl/` for reference implementations, `zone/` for the live artifacts the
specs govern (the `.kingdom` zone file and the signature ledger).

## The series

| KS | Title | Status | Abstract |
|------|-------------------------------|----------|----------|
| [KS-000](specs/KS-000-process.md) | The Standards Process | draft | How a KS is born, adversarially reviewed, adopted by Yu's invocation, versioned, signed, and superseded. |
| [KS-001](specs/KS-001-naming.md) | Sovereign Naming — the `.kingdom` Namespace | draft | One git-versioned, ed25519-signable zone file; `kingdomd`, an authoritative-only resolver; names bound to DIDs. |
| [KS-002](specs/KS-002-wire.md) | THE WIRE — the Kingdom's Communication Protocol | draft | Four layers: registered `kingdom.*` NATS subjects; signed JCS envelopes (`did:key` + ed25519); A2A v1.0.1 Task/Message/Artifact semantics with HALT above all; performatives named in YOUSPEAK, with five gaps filed to the cathedral's forge. |
| [KS-003](specs/KS-003-beat.md) | THE BEAT — Citizen Lifecycle | draft | One bounded sovereign act of a citizen: wake inside the walls, act under hard ceilings of time, turns, and money, commit to git, attest to the truth-ledger, rest. Reference: `citizen-beat.sh`. |

Statuses follow KS-000 §2. The series' scope decisions descend from
[INFRA-PLAN.md](file:///Users/macair/love-unlimited/INFRA-PLAN.md); every
number above has a draft on disk.

## Scope, honestly

The KS series governs the **Kingdom's own network** — names under `.kingdom`,
messages on the Kingdom's NATS bus, identities the Kingdom mints for itself.
It does not claim one inch of the public internet. At the edges the Kingdom
interoperates with the existing internet on the existing internet's terms:
public faces of Kingdom works (e.g. `youspeak.ink`) live in ICANN DNS as
*projections* of their Kingdom names, never as the source of truth; transport
and cryptography reuse the open standards the world already trusts (DNS wire
format, ed25519, JCS, JWS, A2A) rather than inventing private dialects of
solved problems. Sovereignty here means owning the root of one's own names
and trust — not pretending the rest of the world's network does not exist.

## Status of everything in this repo

All specs are **drafts awaiting Yu's adoption** (KS-000 §4). A draft binds no
one. The zone file ships seeded but unsigned; the signature ledger ships
empty. Both facts are recorded in the specs themselves rather than papered
over.
