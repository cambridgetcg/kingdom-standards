#!/usr/bin/env python3
"""kingdomd — the KS-001 reference resolver. DRAFT awaiting Yu's adoption.

A tiny authoritative DNS server for the sovereign TLD `.kingdom`.
Pure python3 stdlib, no deps, no recursion, no upstream — DIY law.

    listens on 127.0.0.1:5300/udp (configurable: --port)
    zone:    KINGDOM-STANDARDS/zone/kingdom.zone.json (--zone; mtime-reloaded)

Behavior (security posture per KS-001):
    A    <name>.kingdom   -> the zone's address (usually 127.0.0.1)
    TXT  <name>.kingdom   -> the name's DID string (identity-over-DNS)
    other qtypes on .kingdom        -> NOTIMP
    name not in zone                -> NXDOMAIN (authoritative)
    anything not under .kingdom     -> REFUSED (we resolve for no one else)
    zone file missing               -> NXDOMAIN for all, logged once, no crash

OS wiring (one line, once, needs root — see impl/INSTALL.md):
    sudo mkdir -p /etc/resolver
    printf 'nameserver 127.0.0.1\nport 5300\n' | sudo tee /etc/resolver/kingdom

Lineage: sibling of love-unlimited/kns/resolver.py (the v0 root on :5391);
this is the from-scratch KS-001 reference, zone-file-driven and TXT-capable.

Editors: Nuance + Yu, 2026-06-09.
"""
import argparse
import ipaddress
import json
import os
import socket
import struct
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_ZONE = os.path.normpath(os.path.join(HERE, "..", "zone", "kingdom.zone.json"))
DEFAULT_PORT = 5300
HOST = "127.0.0.1"
TLD = "kingdom"
TTL = 60  # short: the zone is a living file

# DNS constants (RFC 1035)
NOERROR, FORMERR, SERVFAIL, NXDOMAIN, NOTIMP, REFUSED = 0, 1, 2, 3, 4, 5
QTYPE_A, QTYPE_TXT = 1, 16
QCLASS_IN, QCLASS_ANY = 1, 255
QTYPE_NAMES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX",
               16: "TXT", 28: "AAAA", 33: "SRV", 65: "HTTPS", 255: "ANY"}


def log(msg: str) -> None:
    print(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} {msg}", flush=True)


# ── Zone ─────────────────────────────────────────────────────────────────────

def parse_zone(data: dict) -> dict:
    """Validate zone JSON -> {name: {'a': [ips], 'txt': did}}. Raises ValueError.

    'a' may be a single IPv4 string or a list of them (one A record each).
    """
    names = data.get("names")
    if not isinstance(names, dict):
        raise ValueError("zone must carry a 'names' object")
    table = {}
    for name, rec in names.items():
        if not isinstance(rec, dict):
            raise ValueError(f"'{name}': record must be an object")
        entry = {}
        addrs = rec.get("a", [])
        if isinstance(addrs, str):
            addrs = [addrs] if addrs else []
        if not isinstance(addrs, list):
            raise ValueError(f"'{name}': 'a' must be a string or list")
        for addr in addrs:
            try:
                ipaddress.IPv4Address(addr)
            except (ipaddress.AddressValueError, ValueError):
                raise ValueError(f"'{name}': bad IPv4 address {addr!r}")
        if addrs:
            entry["a"] = addrs
        did = rec.get("did", "")
        if did:
            entry["txt"] = str(did)
        table[name.strip().lower()] = entry
    return table


class Zone:
    """The zone table, reloaded whenever the file's mtime changes."""

    def __init__(self, path: str):
        self.path = path
        self.mtime = None
        self.table = {}
        self.warned_missing = False

    def lookup(self) -> dict:
        try:
            mtime = os.path.getmtime(self.path)
        except OSError:
            if not self.warned_missing:
                log(f"zone missing: {self.path} — serving NXDOMAIN for all .{TLD} names")
                self.warned_missing = True
            self.table, self.mtime = {}, None
            return self.table
        if mtime != self.mtime:
            self.mtime = mtime  # even on a bad parse: log once per version
            try:
                with open(self.path, encoding="utf-8") as f:
                    self.table = parse_zone(json.load(f))
                self.warned_missing = False
                log(f"zone loaded: {len(self.table)} names from {self.path}")
            except (json.JSONDecodeError, ValueError, OSError) as e:
                log(f"zone reload failed ({e}); keeping previous table")
        return self.table


# ── Wire format, by hand (RFC 1035 §4) ───────────────────────────────────────

def parse_question(pkt: bytes):
    """packet -> (qid, qflags, qname, qtype, qclass, raw_question). ValueError on junk."""
    if len(pkt) < 12:
        raise ValueError("short header")
    qid, qflags, qdcount, _an, _ns, _ar = struct.unpack("!6H", pkt[:12])
    if qflags & 0x8000:
        raise ValueError("not a query (QR=1)")
    if qdcount != 1:
        raise ValueError(f"qdcount={qdcount}")
    labels, pos = [], 12
    while True:
        if pos >= len(pkt):
            raise ValueError("truncated qname")
        n = pkt[pos]
        if n == 0:
            pos += 1
            break
        if n & 0xC0:
            raise ValueError("compression pointer in question")
        pos += 1
        if pos + n > len(pkt):
            raise ValueError("truncated label")
        labels.append(pkt[pos:pos + n].decode("ascii", "replace"))
        pos += n
    if len(labels) > 32 or pos > 12 + 255:
        raise ValueError("qname too long")
    if pos + 4 > len(pkt):
        raise ValueError("truncated qtype/qclass")
    qtype, qclass = struct.unpack("!2H", pkt[pos:pos + 4])
    return qid, qflags, ".".join(labels), qtype, qclass, pkt[12:pos + 4]


def build_response(qid, qflags, question, rcode, answers, aa) -> bytes:
    """Header + echoed question + answer RRs. Flags: QR=1, opcode/RD copied, RA=0."""
    flags = 0x8000 | (qflags & 0x7800) | (qflags & 0x0100) | (rcode & 0x000F)
    if aa:
        flags |= 0x0400
    header = struct.pack("!6H", qid, flags, 1, len(answers), 0, 0)
    return header + question + b"".join(answers)


def rr_a(addr: str) -> bytes:
    """A record; name is a pointer (0xC00C) to the question's qname."""
    return struct.pack("!HHHIH", 0xC00C, QTYPE_A, QCLASS_IN, TTL, 4) + socket.inet_aton(addr)


def rr_txt(text: str) -> bytes:
    """TXT record: rdata is length-prefixed character-strings of <=255 bytes."""
    raw = text.encode("utf-8")
    chunks = [raw[i:i + 255] for i in range(0, len(raw), 255)] or [b""]
    rdata = b"".join(bytes([len(c)]) + c for c in chunks)
    return struct.pack("!HHHIH", 0xC00C, QTYPE_TXT, QCLASS_IN, TTL, len(rdata)) + rdata


# ── Resolution (authoritative-only) ──────────────────────────────────────────

def resolve(table: dict, qname: str, qtype: int, qclass: int):
    """-> (rcode, [answer RRs], aa, human-readable answer for the log line)."""
    labels = qname.lower().rstrip(".").split(".")
    if labels[-1] != TLD:
        return REFUSED, [], False, "REFUSED"          # no recursion, no upstream
    if qclass not in (QCLASS_IN, QCLASS_ANY):
        return REFUSED, [], False, "REFUSED(class)"
    rec = table.get(".".join(labels[:-1]))
    if rec is None:
        return NXDOMAIN, [], True, "NXDOMAIN"
    if qtype == QTYPE_A:
        if "a" in rec:
            return NOERROR, [rr_a(ip) for ip in rec["a"]], True, ",".join(rec["a"])
        return NOERROR, [], True, "NODATA"
    if qtype == QTYPE_TXT:
        if "txt" in rec:
            return NOERROR, [rr_txt(rec["txt"])], True, f'"{rec["txt"]}"'
        return NOERROR, [], True, "NODATA"
    return NOTIMP, [], True, "NOTIMP"                  # A and TXT only


# ── Server ───────────────────────────────────────────────────────────────────

def serve(port: int, zone: Zone) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, port))
    log(f"kingdomd up — authoritative for .{TLD} on {HOST}:{port}/udp, zone {zone.path}")
    zone.lookup()  # load (and log) the zone at boot
    while True:
        pkt, addr = sock.recvfrom(4096)
        try:
            qid, qflags, qname, qtype, qclass, question = parse_question(pkt)
        except ValueError as e:
            log(f"- - FORMERR ({e}) from {addr[0]}")
            if len(pkt) >= 2:  # answer FORMERR if we can at least echo the id
                qid = struct.unpack("!H", pkt[:2])[0]
                sock.sendto(struct.pack("!6H", qid, 0x8000 | FORMERR, 0, 0, 0, 0), addr)
            continue
        rcode, answers, aa, shown = resolve(zone.lookup(), qname, qtype, qclass)
        sock.sendto(build_response(qid, qflags, question, rcode, answers, aa), addr)
        log(f"{qname} {QTYPE_NAMES.get(qtype, str(qtype))} {shown}")


def check(zone_path: str) -> int:
    """--check: validate the zone JSON, print the parsed table, exit."""
    try:
        with open(zone_path, encoding="utf-8") as f:
            table = parse_zone(json.load(f))
    except (OSError, json.JSONDecodeError, ValueError) as e:
        print(f"zone INVALID: {zone_path}\n  {e}", file=sys.stderr)
        return 1
    print(f"zone OK: {zone_path} — {len(table)} names")
    width = max((len(n) for n in table), default=0) + len(TLD) + 1
    for name in sorted(table):
        rec = table[name]
        fqdn = f"{name}.{TLD}"
        for ip in rec.get("a", []):
            print(f"  {fqdn:<{width}}  A    {ip}")
        if "txt" in rec:
            print(f"  {fqdn:<{width}}  TXT  {rec['txt']}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(prog="kingdomd",
                                 description="KS-001 reference resolver — authoritative DNS for .kingdom")
    ap.add_argument("--port", type=int, default=DEFAULT_PORT, help=f"UDP port (default {DEFAULT_PORT})")
    ap.add_argument("--zone", default=DEFAULT_ZONE, help=f"zone JSON path (default {DEFAULT_ZONE})")
    ap.add_argument("--check", action="store_true", help="validate zone, print parsed table, exit")
    args = ap.parse_args()
    if args.check:
        return check(args.zone)
    try:
        serve(args.port, Zone(args.zone))
    except KeyboardInterrupt:
        log("kingdomd down — the names rest")
    return 0


if __name__ == "__main__":
    sys.exit(main())
