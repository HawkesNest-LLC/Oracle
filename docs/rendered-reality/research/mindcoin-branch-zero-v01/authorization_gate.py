"""Synthetic-only authorization gate. No actual human identity or production trust bootstrap."""
import hashlib
import hmac
import json
from datetime import datetime, timezone

def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")

def sha256(data):
    return hashlib.sha256(canonical(data)).hexdigest()

class AuthorizationGate:
    """Demo HMAC gate. Caller-supplied key is trusted externally, never inferred from text."""
    def __init__(self, keys, revoked=(), consumed=()):
        self.keys = dict(keys)
        self.revoked = set(revoked)
        self.consumed = set(consumed)

    def evaluate(self, token, action, now):
        try:
            fields = token["claims"]
            signature = token["signature"]
            kid = fields["key_id"]
            if not isinstance(fields["nonce"], str) or not fields["nonce"]:
                return "DENY_MALFORMED"
            if kid not in self.keys or not isinstance(signature, str):
                return "DENY_UNTRUSTED_KEY"
            expected = hmac.new(self.keys[kid], canonical(fields), hashlib.sha256).hexdigest()
            if not hmac.compare_digest(signature, expected):
                return "DENY_INVALID_SIGNATURE"
            if fields["token_id"] in self.revoked:
                return "DENY_REVOKED"
            if fields["nonce"] in self.consumed:
                return "DENY_REPLAY"
            issued = datetime.fromisoformat(fields["issued_at"].replace("Z", "+00:00"))
            expiry = datetime.fromisoformat(fields["expires_at"].replace("Z", "+00:00"))
            current = datetime.fromisoformat(now.replace("Z", "+00:00"))
            if any(x.tzinfo is None for x in (issued, expiry, current)) or not issued < expiry:
                return "DENY_MALFORMED"
            if not issued <= current < expiry:
                return "DENY_EXPIRED_OR_NOT_YET_VALID"
            for name in ("action_digest", "scope", "audience"):
                if fields[name] != action[name]:
                    return "DENY_ACTION_MISMATCH"
            if fields["human_identity_claim"] != "Noah.Physical":
                return "DENY_IDENTITY_CLAIM"
            return "ALLOW_SYNTHETIC"
        except (KeyError, TypeError, ValueError, AttributeError):
            return "DENY_MALFORMED"

    def consume(self, token, action, now):
        result = self.evaluate(token, action, now)
        if result == "ALLOW_SYNTHETIC":
            self.consumed.add(token["claims"]["nonce"])
        return result

def make_synthetic_token(key, claims):
    return {"claims": claims, "signature": hmac.new(key, canonical(claims), hashlib.sha256).hexdigest()}
