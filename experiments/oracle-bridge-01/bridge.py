"""ORACLE Bridge 0.1: local durable inbox/outbox, no external API claims.

Standard library only. Never executes AI requests or promotes canon.
Usage:
  python bridge.py init
  python bridge.py send --to gemini --body "Review source 42" --source "github:..."
  python bridge.py inbox --agent gemini
  python bridge.py ack --id <uuid> --agent gemini --receipt "provider:..."
  python bridge.py audit
"""
import argparse
import hashlib
import json
import os
import sqlite3
import sys
import uuid
from datetime import datetime, timezone

DB = os.environ.get("ORACLE_BRIDGE_DB", "oracle_bridge.sqlite3")
AGENTS = {"chatgpt", "gemini", "claude", "codex", "grok", "copilot", "meta", "siri", "alexa", "human"}
SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
 id TEXT PRIMARY KEY, created_at TEXT NOT NULL, sender TEXT NOT NULL,
 recipient TEXT NOT NULL, body TEXT NOT NULL, source TEXT NOT NULL,
 body_sha256 TEXT NOT NULL, status TEXT NOT NULL DEFAULT 'QUEUED',
 ack_agent TEXT, ack_at TEXT, receipt TEXT
);
CREATE TABLE IF NOT EXISTS events (
 seq INTEGER PRIMARY KEY AUTOINCREMENT, timestamp TEXT NOT NULL,
 message_id TEXT NOT NULL, event_type TEXT NOT NULL,
 detail TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL
);
"""
def now():
    return datetime.now(timezone.utc).isoformat()
def connect():
    db = sqlite3.connect(DB)
    db.execute("PRAGMA busy_timeout=5000")
    db.executescript(SCHEMA)
    return db
def event(db, mid, kind, detail):
    prev = db.execute("SELECT event_hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
    parent = prev[0] if prev else "GENESIS"
    t = now()
    data = json.dumps([t, mid, kind, detail, parent], separators=(",", ":"))
    digest = hashlib.sha256(data.encode()).hexdigest()
    db.execute("INSERT INTO events(timestamp,message_id,event_type,detail,previous_hash,event_hash) VALUES(?,?,?,?,?,?)",
               (t, mid, kind, detail, parent, digest))
def send(db, recipient, body, source, sender="human"):
    if recipient not in AGENTS or sender not in AGENTS:
        raise ValueError("unknown agent")
    if not body.strip() or not source.strip():
        raise ValueError("body and source are required")
    mid = str(uuid.uuid4())
    digest = hashlib.sha256(body.encode()).hexdigest()
    with db:
        db.execute("INSERT INTO messages(id,created_at,sender,recipient,body,source,body_sha256,status) VALUES(?,?,?,?,?,?,?,?)",
                   (mid, now(), sender, recipient, body, source, digest, "QUEUED"))
        event(db, mid, "QUEUED", "Local queue only; not delivered")
    return mid
def inbox(db, agent):
    if agent not in AGENTS:
        raise ValueError("unknown agent")
    rows = db.execute("SELECT id,created_at,sender,body,source,status FROM messages WHERE recipient=? ORDER BY created_at", (agent,))
    return [dict(zip(("id","created_at","sender","body","source","status"), row)) for row in rows]
def ack(db, mid, agent, receipt):
    if not receipt.strip():
        raise ValueError("External receipt required")
    row = db.execute("SELECT recipient,status FROM messages WHERE id=?", (mid,)).fetchone()
    if not row or row[0] != agent or row[1] != "QUEUED":
        raise ValueError("Message not found, wrong agent, or already acknowledged")
    with db:
        db.execute("UPDATE messages SET status='ACKNOWLEDGED',ack_agent=?,ack_at=?,receipt=? WHERE id=?",
                   (agent, now(), receipt, mid))
        event(db, mid, "ACKNOWLEDGED", "Operator-entered receipt: "+receipt)
def audit(db):
    """Check local chain and message/event state invariants; NOT authenticated provenance."""
    prev = "GENESIS"
    histories = {}
    for t, mid, kind, detail, parent, digest in db.execute(
        "SELECT timestamp,message_id,event_type,detail,previous_hash,event_hash FROM events ORDER BY seq"):
        raw = json.dumps([t, mid, kind, detail, parent], separators=(",", ":"))
        if parent != prev or hashlib.sha256(raw.encode()).hexdigest() != digest:
            return False
        prev = digest
        histories.setdefault(mid, []).append((t, kind, detail))

    messages = list(db.execute(
        "SELECT id,created_at,recipient,body,body_sha256,status,ack_agent,ack_at,receipt FROM messages"))
    if set(histories) != {row[0] for row in messages}:
        return False

    for mid, created, recipient, body, digest, status, agent, ack_at, receipt in messages:
        if hashlib.sha256(body.encode()).hexdigest() != digest:
            return False
        history = histories[mid]
        if (not history or history[0][1:] != ("QUEUED", "Local queue only; not delivered")
                or history[0][0] < created):
            return False
        if status == "QUEUED":
            if len(history) != 1 or any(x is not None for x in (agent, ack_at, receipt)):
                return False
        elif status == "ACKNOWLEDGED":
            if len(history) != 2 or history[1][1] != "ACKNOWLEDGED":
                return False
            if agent != recipient or not isinstance(ack_at, str) or not ack_at.strip():
                return False
            if not isinstance(receipt, str) or not receipt.strip():
                return False
            if history[1][2] != "Operator-entered receipt: " + receipt:
                return False
            if history[1][0] < created or ack_at < created:
                return False
        else:
            return False
    return True
def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    s = sub.add_parser("send")
    s.add_argument("--to", required=True, choices=sorted(AGENTS))
    s.add_argument("--body", required=True)
    s.add_argument("--source", required=True)
    s.add_argument("--from-agent", default="human", choices=sorted(AGENTS))
    i = sub.add_parser("inbox")
    i.add_argument("--agent", required=True, choices=sorted(AGENTS))
    a = sub.add_parser("ack")
    a.add_argument("--id", required=True)
    a.add_argument("--agent", required=True, choices=sorted(AGENTS))
    a.add_argument("--receipt", required=True)
    sub.add_parser("audit")
    args = p.parse_args()
    db = connect()
    if args.command == "send":
        print(send(db, args.to, args.body, args.source, args.from_agent))
    elif args.command == "inbox":
        print(json.dumps(inbox(db, args.agent), indent=2))
    elif args.command == "ack":
        ack(db, args.id, args.agent, args.receipt)
        print("Recorded operator-entered acknowledgement")
    elif args.command == "audit":
        print("LOCAL HASH CHECK OK" if audit(db) else "LOCAL HASH CHECK FAILED")
        sys.exit(0 if audit(db) else 1)
    else:
        print("Initialized local SQLite bridge")
if __name__ == "__main__":
    main()
