"""Ed25519 action-scoped approvals with atomic SQLite nonce consumption.

Research prototype. Trust keys must be provisioned independently of receipts.
Requires cryptography>=42. Approval check is separate from action execution.
"""
import base64
import hashlib
import json
import sqlite3
import time
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def b64decode(value):
    if not isinstance(value, str):
        raise ValueError("invalid encoding")
    return base64.b64decode(value, validate=True)

class Ed25519ApprovalVerifier:
    def __init__(self, public_keys, database_path, *, clock=None):
        # public_keys: trusted key_id -> raw 32-byte Ed25519 public key, from out-of-band provisioning
        self.keys = {k: Ed25519PublicKey.from_public_bytes(v) for k, v in public_keys.items()}
        self.db = sqlite3.connect(database_path, isolation_level=None, timeout=10)
        self.db.execute("PRAGMA busy_timeout=10000")
        self.db.execute("CREATE TABLE IF NOT EXISTS consumed (key_id TEXT NOT NULL, nonce TEXT NOT NULL, consumed_at INTEGER NOT NULL, PRIMARY KEY(key_id, nonce))")
        self.clock = clock or (lambda: int(time.time()))

    def close(self):
        self.db.close()

    def verify(self, receipt, *, action, object_digest):
        """Verify and consume a receipt exactly once. Returns False on any validation failure."""
        try:
            if not isinstance(receipt, dict) or set(receipt) != {"payload", "signature"}:
                return False
            p = receipt["payload"]
            fields = {"version", "key_id", "actor", "action", "object_sha256", "scope", "issued_at", "expires_at", "nonce"}
            if not isinstance(p, dict) or set(p) != fields or p["version"] != 1:
                return False
            if not all(isinstance(p[k], str) and p[k] for k in ("key_id", "actor", "action", "object_sha256", "scope", "nonce")):
                return False
            if p["actor"] != "Noah.Physical" or p["action"] != action or p["object_sha256"] != object_digest:
                return False
            if not isinstance(object_digest, str) or len(object_digest) != 64 or any(c not in "0123456789abcdef" for c in object_digest):
                return False
            if not isinstance(p["issued_at"], int) or isinstance(p["issued_at"], bool) or not isinstance(p["expires_at"], int) or isinstance(p["expires_at"], bool):
                return False
            now = self.clock()
            if not (p["issued_at"] <= now < p["expires_at"] and p["expires_at"] - p["issued_at"] <= 3600):
                return False
            if len(p["nonce"]) < 16 or len(p["nonce"]) > 128 or len(p["scope"]) > 512:
                return False
            if p["key_id"] not in self.keys:
                return False
            self.keys[p["key_id"]].verify(b64decode(receipt["signature"]), b"EXOCORTEX-APPROVAL-V1\x00" + canonical(p))
            # BEGIN IMMEDIATE + unique constraint: replay protection across processes using same SQLite DB.
            self.db.execute("BEGIN IMMEDIATE")
            try:
                self.db.execute("INSERT INTO consumed(key_id, nonce, consumed_at) VALUES (?, ?, ?)", (p["key_id"], p["nonce"], now))
                self.db.execute("COMMIT")
                return True
            except sqlite3.IntegrityError:
                self.db.execute("ROLLBACK")
                return False
            except Exception:
                self.db.execute("ROLLBACK")
                raise
        except (ValueError, TypeError, KeyError, InvalidSignature, sqlite3.Error):
            return False

def digest_bytes(data):
    return hashlib.sha256(data).hexdigest()
