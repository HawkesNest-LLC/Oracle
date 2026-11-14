"""Continuity Legacy Kernel v0.1: synthetic-data prototype, NOT an estate release service."""
import base64
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


class Rejected(Exception):
    pass


class Kernel:
    def __init__(self, path):
        self.db = sqlite3.connect(str(path))
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.execute("CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, payload TEXT NOT NULL, previous_hash TEXT NOT NULL, event_hash TEXT NOT NULL UNIQUE)")
        self.db.execute("CREATE TABLE IF NOT EXISTS keys (key_id TEXT PRIMARY KEY, public_key BLOB NOT NULL, revoked_at INTEGER)")
        self.db.execute("CREATE TABLE IF NOT EXISTS approvals (approval_id TEXT PRIMARY KEY, key_id TEXT NOT NULL, action TEXT NOT NULL, target TEXT NOT NULL, target_version TEXT NOT NULL, expires_at INTEGER NOT NULL, signature BLOB NOT NULL, used INTEGER NOT NULL DEFAULT 0)")
        self.db.commit()

    def register_key(self, key_id, public_key_bytes):
        if len(public_key_bytes) != 32:
            raise Rejected("Invalid Ed25519 public key")
        with self.db:
            self.db.execute("INSERT INTO keys(key_id,public_key) VALUES (?,?)", (key_id, public_key_bytes))

    def revoke_key(self, key_id, now):
        with self.db:
            row = self.db.execute("UPDATE keys SET revoked_at=? WHERE key_id=? AND revoked_at IS NULL", (now, key_id))
            if row.rowcount != 1:
                raise Rejected("Key absent or already revoked")

    def add_approval(self, approval, signature):
        required = {"approval_id", "key_id", "action", "target", "target_version", "expires_at"}
        if set(approval) != required or not isinstance(approval["expires_at"], int):
            raise Rejected("Invalid approval shape")
        row = self.db.execute("SELECT public_key,revoked_at FROM keys WHERE key_id=?", (approval["key_id"],)).fetchone()
        if not row or row[1] is not None:
            raise Rejected("Unknown or revoked key")
        try:
            Ed25519PublicKey.from_public_bytes(row[0]).verify(signature, canonical(approval))
        except (InvalidSignature, ValueError) as exc:
            raise Rejected("Invalid approval signature") from exc
        with self.db:
            self.db.execute("INSERT INTO approvals(approval_id,key_id,action,target,target_version,expires_at,signature) VALUES (?,?,?,?,?,?,?)",
                            (approval["approval_id"], approval["key_id"], approval["action"], approval["target"], approval["target_version"], approval["expires_at"], signature))

    def append(self, event, approval_id=None, now=None):
        now = int(datetime.now(timezone.utc).timestamp()) if now is None else now
        if set(event) != {"type", "target", "version", "body", "source"}:
            raise Rejected("Event must include type,target,version,body,source")
        if event["type"] not in ("SOURCE", "PROPOSAL", "CORRECTION", "PROMOTION", "REVOCATION"):
            raise Rejected("Unknown event type")
        if not all(isinstance(event[k], str) and event[k] for k in ("target", "version", "body", "source")):
            raise Rejected("Invalid event fields")
        if event["type"] in ("CORRECTION", "PROMOTION", "REVOCATION"):
            if not approval_id:
                raise Rejected("Human approval required")
        with self.db:
            if approval_id:
                row = self.db.execute("""SELECT a.key_id,a.action,a.target,a.target_version,a.expires_at,a.used,k.revoked_at
                   FROM approvals a JOIN keys k ON a.key_id=k.key_id WHERE a.approval_id=?""", (approval_id,)).fetchone()
                if not row or row[4] < now or row[5] or row[6] is not None:
                    raise Rejected("Missing, expired, consumed, or revoked approval")
                if (row[1],row[2],row[3]) != (event["type"],event["target"],event["version"]):
                    raise Rejected("Approval scope/version mismatch")
                self.db.execute("UPDATE approvals SET used=1 WHERE approval_id=? AND used=0", (approval_id,))
            prior = self.db.execute("SELECT event_hash FROM events ORDER BY seq DESC LIMIT 1").fetchone()
            previous_hash = prior[0] if prior else "GENESIS"
            record = {"event": event, "approval_id": approval_id, "timestamp": now}
            event_hash = digest({"previous_hash": previous_hash, "record": record})
            self.db.execute("INSERT INTO events(payload,previous_hash,event_hash) VALUES (?,?,?)",
                            (canonical(record).decode("utf-8"), previous_hash, event_hash))
        return {"event_hash": event_hash, "previous_hash": previous_hash, "record": record}

    def verify_chain(self):
        previous = "GENESIS"
        for payload, stored_prev, event_hash in self.db.execute("SELECT payload,previous_hash,event_hash FROM events ORDER BY seq"):
            if stored_prev != previous or digest({"previous_hash": previous, "record": json.loads(payload)}) != event_hash:
                return False
            previous = event_hash
        return True

    def receipt(self, event_hash):
        row = self.db.execute("SELECT payload,previous_hash,event_hash FROM events WHERE event_hash=?", (event_hash,)).fetchone()
        if not row:
            raise Rejected("Receipt not found")
        return {"record": json.loads(row[0]), "previous_hash": row[1], "event_hash": row[2],
                "chain_valid": self.verify_chain(), "source_verified": False,
                "source_verification_status": "UNKNOWN: source URI/content not independently checked"}

    def close(self):
        self.db.close()
