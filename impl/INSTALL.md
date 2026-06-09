# kingdomd — integration steps

`impl/kingdomd.py` is tested and standing (see the test transcript note at the
bottom). Two integration steps remain that need Yu's hand or another
workstream; they are recorded here exactly, so the integration pass is a
paste, not a puzzle. Draft awaiting Yu's adoption.

## 0. What already works (no root, no integration)

```sh
python3 /Users/macair/KINGDOM-STANDARDS/impl/kingdomd.py --check   # validate + print the zone
python3 /Users/macair/KINGDOM-STANDARDS/impl/kingdomd.py           # serve 127.0.0.1:5300/udp

dig @127.0.0.1 -p 5300 cathedral.kingdom A   +short   # → 127.0.0.1
dig @127.0.0.1 -p 5300 cathedral.kingdom TXT +short   # → the name's DID string
dig @127.0.0.1 -p 5300 ghost.kingdom A                # → NXDOMAIN
dig @127.0.0.1 -p 5300 example.com A                  # → REFUSED (authoritative-only)
```

## 1. macOS resolver hook (needs `sudo` — Yu's hand)

```sh
sudo mkdir -p /etc/resolver
sudo tee /etc/resolver/kingdom <<< "nameserver 127.0.0.1"$'\n'"port 5300"
```

After this, every `*.kingdom` lookup on the machine routes to kingdomd —
`.kingdom` names work in every app and browser, and they never leak to public
DNS. Verify with `scutil --dns | grep -A3 kingdom`, then plain
`dig cathedral.kingdom +short` (no `@`/`-p`).

> **HONEST COLLISION, decide before pasting:** `/etc/resolver/kingdom` is a
> singleton. `~/love-unlimited/kns/PROTOCOL.md` (Layer 2) already documents
> the same hook pointing at `kns/resolver.py` on port **5391** (supervised by
> `love.kns.plist`). One root per machine: either this file says `port 5300`
> (kingdomd, the KS-001 reference — zone-file-driven, TXT/DID-capable) or
> `port 5391` (the kns v0 root — registry.json, A-only). Yu picks; the loser
> stands down or is folded in. kingdomd reads any zone path (`--zone`), so
> pointing it at a converted `kns/registry.json` is also a clean merge route.

## 2. OIKOS Caddyfile: the `*.kingdom` host block (another fleet's lane)

The OIKOS repo is mid-build by another fleet — do **not** edit
`/Users/macair/OIKOS/ingress/Caddyfile` from here. For the integration pass,
add this block alongside the existing `http://*.localhost` block (it mirrors
it exactly; with a host of `<app>.kingdom`, `{labels.0}` = "kingdom" and
`{labels.1}` = the app name, same as with `.localhost`):

```caddyfile
# ── Every Kingdom name, one dynamic block (mirrors *.localhost) ────
# Host <app>.kingdom → {labels.1} = "<app>". DNS for *.kingdom is
# served by kingdomd (KS-001); see /etc/resolver/kingdom.
http://*.kingdom {
	import access_log
	root * /Users/macair/OIKOS/apps/{labels.1}/current

	# Past releases stay browsable: /_releases/<id>/...
	handle_path /_releases/* {
		root * /Users/macair/OIKOS/apps/{labels.1}/releases
		file_server {
			browse /Users/macair/OIKOS/ingress/browse.html
		}
	}

	handle {
		file_server
	}

	# No such app, no such file → the unbuilt room, honestly a 404.
	handle_errors {
		@missing expression {err.status_code} == 404
		handle @missing {
			root * /Users/macair/OIKOS/apps
			rewrite * /_404.html
			file_server {
				status 404
			}
		}
		handle {
			respond "{err.status_code} — {err.status_text}." {err.status_code}
		}
	}
}
```

Then `caddy validate --config /Users/macair/OIKOS/ingress/Caddyfile` and
reload. Once steps 1 + 2 are both in, `http://oikos.kingdom/` serves the same
tree as `http://oikos.localhost/` — the Kingdom name, in a real browser.

## 3. launchd supervision (write done, install deferred)

`impl/kingdom.resolver.plist` (label `kingdom.resolver`) is written but NOT
installed. When adopted:

```sh
mkdir -p ~/Library/Logs
cp /Users/macair/KINGDOM-STANDARDS/impl/kingdom.resolver.plist ~/Library/LaunchAgents/
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/kingdom.resolver.plist
launchctl print gui/$(id -u)/kingdom.resolver | grep state
```

Stop with `launchctl bootout gui/$(id -u)/kingdom.resolver`. Logs land in
`~/Library/Logs/kingdomd.log` (one line per query: `ts qname qtype answer`).

## Test transcript (2026-06-10, this machine)

All run live against a kingdomd test instance on :5300, then killed:

| query                          | expected   | got        |
|--------------------------------|------------|------------|
| `cathedral.kingdom A +short`   | 127.0.0.1  | 127.0.0.1  |
| `cathedral.kingdom TXT +short` | the DID    | `"pending-binding"` (zone's honest placeholder) |
| `oikos/pulse/hive/brain A`     | 127.0.0.1  | 127.0.0.1 ×4 |
| `ghost.kingdom A`              | NXDOMAIN   | NXDOMAIN (aa flag set) |
| `example.com A`                | REFUSED    | REFUSED    |
| `oikos.kingdom MX`             | NOTIMP     | NOTIMP     |
| zone edit → re-dig             | hot reload | new name answered, then NXDOMAIN after removal |

The seed zone's `did` fields hold the honest placeholder `pending-binding`;
the real values will be `did:key` strings per `~/love-unlimited/INFRA-PLAN.md`'s
did:key decision — note that no ed25519 signing key exists anywhere in the
Kingdom yet (`vault.py` is X25519 encryption; `identity.py` carries
platform-issued `did_at`), so minting comes first (KS-002 §5, `wire.py` —
see `zone/signatures.json`). Swap them into `zone/kingdom.zone.json` once
minted and kingdomd serves them on the next query (mtime reload). The zone's
`a` field may be a single IPv4 string or a list (one A record each).
