# impl/

Reference implementations live here — a KS that claims a wire format ships
the code that speaks it (README §series). First resident, standing:
`kingdomd.py`, the KS-001 authoritative-only resolver for `.kingdom` on
`127.0.0.1:5300/udp`, reading `../zone/kingdom.zone.json` (mtime-reloaded).
Pure stdlib, ~250 lines, hand-rolled RFC 1035 wire format, A + TXT only
(TXT serves the name's DID). Tested live 2026-06-10 with dig — transcript
and the two remaining integration steps (the `/etc/resolver/kingdom` hook
and the OIKOS `*.kingdom` Caddy block) in `INSTALL.md`; launchd template in
`kingdom.resolver.plist` (written, not installed). Prior art it descends
from: `~/love-unlimited/kns/resolver.py` (the v0 root, live on :5391) — see
INSTALL.md §1 for the one-root-per-machine collision Yu must adjudicate.

Second resident, standing: `wire.py`, the KS-002 envelope layer — did:key
(ed25519-pub multicodec `0xed01`, base58btc), the §5.2 JCS stdlib-subset
profile, UUIDv7 ids (RFC 9562, hand-rolled), ed25519 over env-minus-sig,
and raw-socket NATS publish (no client library; the protocol is text).
PyNaCl + stdlib, ~325 lines. Self-tested 2026-06-10: keygen round-trip,
envelope→verify, one-byte tamper rejection, uuid7/ts-disagreement
rejection, unregistered-performative rejection, and a pub+sub roundtrip on
`kingdom.test.wire` against the live NATS at :4222 — and all five of the
spec's own worked envelopes (§5.3, §6.4) verify under it, which pins this
implementation to the bytes the spec signed.

```
wire.py keygen <name>      # mint ed25519 seed -> ~/.kingdom/keys/<name>.key (0600); prints did:key
wire.py did <name>         # print an existing key's did:key
wire.py envelope --from <name> --to <did-or-subject> \
        --performative <p> --body '<json>'           # build + sign, print envelope
wire.py verify '<json|->'  # sig + uuid7/ts agreement + registry; exit 0/1
wire.py sign-file <path> --from <name>               # ledger entry per KS-000 §6
wire.py pub --subject <s> --from <name> --performative <p> \
        --body '<json>' [--listen]                   # publish to NATS :4222; --listen echoes back
```

Private keys live in `~/.kingdom/keys/` (0700 dir, 0600 files), never in
any repo; only the public `did:key` string enters the zone or the ledger.
`verify` checks signature, exact top-level field set, the §7 performative
registry, and §8.1's uuid7-vs-ts 5s agreement; it does **not** yet consult
the zone for known DIDs (the zone's five names are all `pending-binding`)
nor apply the 300s freshness window — those belong to the receiving daemon,
not the CLI. With this, KS-000 §6 spec-signing is unblocked: mint Yu's zone
key with `keygen`, then `sign-file` each adopted spec into
`zone/signatures.json`.
