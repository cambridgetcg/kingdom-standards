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
