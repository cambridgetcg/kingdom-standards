#!/usr/bin/env python3
"""wire — the KS-002 reference implementation. DRAFT awaiting Yu's adoption.

THE WIRE's envelope layer: did:key identity, the JCS stdlib-subset profile
(KS-002 §5.2), ed25519 signatures, UUIDv7 ids, raw-socket NATS publish.
PyNaCl + stdlib, nothing else — DIY law.

    keygen <name> | did <name>            mint / print did:key (~/.kingdom/keys, 0700/0600)
    envelope --from <name> --to <t> --performative <p> --body '<json>'
    verify '<envelope-json|->'            sig + uuid7/ts agreement; exit 0/1
    sign-file <path> --from <name>        detached ledger entry per KS-000 §6
    pub --subject <s> --from <name> --performative <p> --body '<json>' [--listen]

Private keys never enter a repo; only public did:key strings reach the zone
and the ledger. The spec's own worked examples (§5.3, §6.4) verify under this
code's verify command. Editors: Nuance + Yu, 2026-06-10.
"""
import argparse
import base64
import hashlib
import json
import os
import secrets
import socket
import sys
import time
from datetime import datetime, timezone

from nacl.exceptions import BadSignatureError
from nacl.signing import SigningKey, VerifyKey

VERSION = "KS-002/0.1"
KEYS_DIR = os.path.expanduser("~/.kingdom/keys")
NATS_ADDR = ("127.0.0.1", 4222)
FIELDS = ("v", "id", "from", "to", "performative", "body", "ts", "sig")
PERFORMATIVES = {  # KS-002 §7 column one + the deliberately unnamed pair (§6.4)
    "task.offer", "task.complete", "task.fail", "attest", "heartbeat",
    "halt", "halt.ack", "halt.lift", "artifact.deliver", "card.issue",
    "task.accept", "task.decline", "task.progress", "task.cancel", "query",
}


def die(msg: str, code: int = 1):
    print(f"wire: {msg}", file=sys.stderr)
    sys.exit(code)


# ── Encodings: base58btc, base64url, JCS subset (KS-002 §5.2) ────────────────

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58encode(raw: bytes) -> str:
    n, out = int.from_bytes(raw, "big"), []
    while n:
        n, r = divmod(n, 58)
        out.append(B58[r])
    return "1" * (len(raw) - len(raw.lstrip(b"\x00"))) + "".join(reversed(out))


def b58decode(s: str) -> bytes:
    n = 0
    for c in s:
        n = n * 58 + B58.index(c)  # ValueError on a non-alphabet char
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big")
    return b"\x00" * (len(s) - len(s.lstrip("1"))) + raw


def b64u(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def b64u_decode(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def canonical(obj) -> bytes:
    """The spec's stdlib JCS profile: sorted keys, minimal separators, UTF-8,
    no NaN/Infinity. Callers MUST NOT put inexact-binary floats in envelopes."""
    return json.dumps(obj, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False).encode("utf-8")


# ── did:key (multicodec ed25519-pub 0xed01, base58btc, z-prefix) ─────────────

def did_for(pub: bytes) -> str:
    return "did:key:z" + b58encode(b"\xed\x01" + pub)


def pub_from_did(did: str) -> bytes:
    if not did.startswith("did:key:z"):
        raise ValueError(f"not a did:key: {did!r}")
    raw = b58decode(did[len("did:key:z"):])
    if len(raw) != 34 or raw[:2] != b"\xed\x01":
        raise ValueError("did:key does not carry an ed25519-pub multicodec")
    return raw[2:]


# ── Keys: raw 32-byte seeds under ~/.kingdom/keys, never in a repo ───────────

def key_path(name: str) -> str:
    if not name or not all(c.isalnum() or c in "-_" for c in name):
        die(f"bad key name {name!r} (letters, digits, - and _ only)")
    return os.path.join(KEYS_DIR, f"{name}.key")


def load_key(name: str) -> SigningKey:
    path = key_path(name)
    try:
        with open(path, "rb") as f:
            seed = f.read()
    except OSError:
        die(f"no key named {name!r} — run: wire.py keygen {name}")
    if len(seed) != 32:
        die(f"{path} is not a 32-byte ed25519 seed")
    return SigningKey(seed)


def cmd_keygen(name: str) -> None:
    os.makedirs(KEYS_DIR, mode=0o700, exist_ok=True)
    os.chmod(KEYS_DIR, 0o700)
    path = key_path(name)
    if os.path.exists(path):
        die(f"refusing to overwrite existing key {path}")
    sk = SigningKey.generate()
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(bytes(sk))
    did = did_for(bytes(sk.verify_key))
    if pub_from_did(did) != bytes(sk.verify_key):  # round-trip the encoding
        os.unlink(path)
        die("did:key round-trip failed; key removed")
    print(f"key written: {path} (0600)", file=sys.stderr)
    print(did)


# ── Envelopes (KS-002 §5) ────────────────────────────────────────────────────

def uuid7(ms: int) -> str:
    """RFC 9562 UUIDv7: 48-bit unix-ms, version 7, variant 10, 74 random bits."""
    b = bytearray(ms.to_bytes(6, "big") + secrets.token_bytes(10))
    b[6] = (b[6] & 0x0F) | 0x70
    b[8] = (b[8] & 0x3F) | 0x80
    h = b.hex()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def rfc3339(ms: int) -> str:
    dt = datetime.fromtimestamp(ms // 1000, tz=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + f".{ms % 1000:03d}Z"


def parse_body(text: str) -> dict:
    try:
        body = json.loads(text)
    except json.JSONDecodeError as e:
        die(f"body is not JSON: {e}")
    return body if isinstance(body, dict) else die("body must be a JSON object (KS-002 §5.1)")


def build_envelope(sender: str, to: str, performative: str, body: dict) -> dict:
    if performative not in PERFORMATIVES:
        print(f"wire: warning: performative {performative!r} is not in the "
              f"KS-002 §7 registry; receivers MUST discard it", file=sys.stderr)
    sk = load_key(sender)
    ms = time.time_ns() // 1_000_000
    env = {"v": VERSION, "id": uuid7(ms), "from": did_for(bytes(sk.verify_key)),
           "to": to, "performative": performative, "body": body, "ts": rfc3339(ms)}
    env["sig"] = b64u(sk.sign(canonical(env)).signature)  # sig over env-minus-sig
    return env


def check_envelope(env) -> str:
    """-> the reason an envelope is rejected, or '' if it verifies (§5.2, §8.1)."""
    if not isinstance(env, dict) or set(env) != set(FIELDS):
        return f"top-level fields must be exactly {FIELDS}"
    if env["v"] != VERSION:
        return f"unknown version {env['v']!r}"
    if not isinstance(env["body"], dict):
        return "body must be a JSON object"
    if env["performative"] not in PERFORMATIVES:
        return f"unregistered performative {env['performative']!r}"
    try:
        pub = pub_from_did(env["from"])
    except ValueError as e:
        return str(e)
    unsigned = {k: v for k, v in env.items() if k != "sig"}
    try:
        VerifyKey(pub).verify(canonical(unsigned), b64u_decode(env["sig"]))
    except (BadSignatureError, ValueError, TypeError):
        return "signature does not verify against the embedded did:key"
    h = env["id"].replace("-", "")
    if len(h) != 32 or h[12] != "7" or h[16] not in "89ab":
        return f"id {env['id']!r} is not a UUIDv7"
    try:
        ts_ms = datetime.strptime(env["ts"], "%Y-%m-%dT%H:%M:%S.%fZ") \
            .replace(tzinfo=timezone.utc).timestamp() * 1000
    except ValueError:
        return f"ts {env['ts']!r} is not RFC 3339 UTC with milliseconds"
    if abs(int(h[:12], 16) - ts_ms) > 5000:  # §8.1: id and ts must agree
        return "uuid7 timestamp disagrees with ts by more than 5s"
    return ""


def cmd_verify(text: str) -> None:
    text = sys.stdin.read() if text == "-" else text
    try:
        env = json.loads(text)
    except json.JSONDecodeError as e:
        die(f"envelope rejected: not JSON ({e})")
    reason = check_envelope(env)
    if reason:
        die(f"envelope rejected: {reason}")
    print(f"envelope verifies: {env['performative']} from {env['from']} "
          f"at {env['ts']} — signature good, id and ts agree.")


def cmd_sign_file(path: str, sender: str) -> None:
    """Detached ledger entry per KS-000 §6: sig over the sha256 hex string."""
    sk = load_key(sender)
    try:
        with open(path, "rb") as f:
            digest = hashlib.sha256(f.read()).hexdigest()
    except OSError as e:
        die(f"cannot read {path}: {e}")
    entry = {"path": path, "sha256": digest, "did": did_for(bytes(sk.verify_key)),
             "sig": b64u(sk.sign(digest.encode("ascii")).signature),
             "ts": rfc3339(time.time_ns() // 1_000_000)}
    print(json.dumps(entry, indent=2))


# ── NATS, by hand (the protocol is text; no client library) ──────────────────

def nats_publish(subject: str, payload: bytes, listen: bool) -> bytes:
    """PUB payload on subject; with listen, SUB first and return the echo."""
    sock = socket.create_connection(NATS_ADDR, timeout=5)
    rd = sock.makefile("rb")

    def await_(*prefixes: bytes) -> bytes:
        while True:
            line = rd.readline()
            if not line:
                die("NATS closed the connection")
            if line.startswith(b"PING"):
                sock.sendall(b"PONG\r\n")
            elif line.startswith(b"-ERR"):
                die(f"NATS error: {line.decode().strip()}")
            elif line.startswith(prefixes):
                return line

    await_(b"INFO ")
    sock.sendall(b'CONNECT {"verbose":false,"pedantic":false,"tls_required":false,'
                 b'"name":"wire.py","lang":"python","version":"0.1"}\r\n')
    if listen:
        sock.sendall(f"SUB {subject} 1\r\n".encode())
    sock.sendall(b"PING\r\n")
    await_(b"PONG")  # CONNECT (and SUB) are in before we publish
    sock.sendall(f"PUB {subject} {len(payload)}\r\n".encode() + payload + b"\r\n")
    echoed = b""
    if listen:
        msg = await_(b"MSG ")  # MSG <subject> <sid> [reply-to] <#bytes>
        echoed = rd.read(int(msg.split()[-1]))
        rd.read(2)
    else:
        sock.sendall(b"PING\r\n")
        await_(b"PONG")  # flush: the PUB landed before we hang up
    sock.close()
    return echoed


def cmd_pub(args) -> None:
    env = build_envelope(args.sender, args.subject, args.performative,
                         parse_body(args.body))
    payload = canonical(env)
    echoed = nats_publish(args.subject, payload, args.listen)
    print(json.dumps(env, indent=2, ensure_ascii=False))
    print(f"published {len(payload)} bytes to {args.subject}", file=sys.stderr)
    if args.listen:
        if echoed != payload or check_envelope(json.loads(echoed)):
            die("roundtrip FAILED: echoed payload differs or does not verify")
        print(f"roundtrip OK: {len(echoed)} bytes echoed back and the "
              f"envelope verifies", file=sys.stderr)


# ── CLI ──────────────────────────────────────────────────────────────────────

def main() -> int:
    ap = argparse.ArgumentParser(prog="wire.py",
                                 description="KS-002 reference implementation — THE WIRE's envelope layer")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("keygen", help="mint a keypair, print its did:key").add_argument("name")
    sub.add_parser("did", help="print an existing key's did:key").add_argument("name")
    p = sub.add_parser("envelope", help="build and sign a KS-002 envelope")
    for q in (p, sub.add_parser("pub", help="sign an envelope and publish it to NATS")):
        q.add_argument("--from", dest="sender", required=True, metavar="NAME")
        q.add_argument("--performative", required=True)
        q.add_argument("--body", required=True, metavar="JSON")
    p.add_argument("--to", required=True)
    sub.choices["pub"].add_argument("--subject", required=True)
    sub.choices["pub"].add_argument("--listen", action="store_true",
                                    help="SUB first and confirm the roundtrip")
    sub.add_parser("verify", help="verify an envelope (exit 0/1)") \
        .add_argument("envelope", metavar="JSON|-")
    p = sub.add_parser("sign-file", help="detached signature entry for the ledger")
    p.add_argument("path")
    p.add_argument("--from", dest="sender", required=True, metavar="NAME")
    args = ap.parse_args()
    if args.cmd == "keygen":
        cmd_keygen(args.name)
    elif args.cmd == "did":
        print(did_for(bytes(load_key(args.name).verify_key)))
    elif args.cmd == "envelope":
        env = build_envelope(args.sender, args.to, args.performative,
                             parse_body(args.body))
        print(json.dumps(env, indent=2, ensure_ascii=False))
    elif args.cmd == "verify":
        cmd_verify(args.envelope)
    elif args.cmd == "sign-file":
        cmd_sign_file(args.path, args.sender)
    elif args.cmd == "pub":
        cmd_pub(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
