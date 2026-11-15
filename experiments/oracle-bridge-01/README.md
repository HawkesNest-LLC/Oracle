# ORACLE Bridge 0.1 | Bounded local queue experiment

**Status: candidate code, NOT a deployed multi-agent integration.**

This is a small, Python standard-library-only queue with SQLite persistence and an audit hash chain. It has **no live Gemini, Claude, Siri, Alexa, or other provider adapter**, and does not transmit messages. This deliberately avoids falsely claiming agent delivery. The optional `ack` command records an **operator-entered assertion**, not authenticated provider acknowledgement. The SHA-256 chain detects casual changes but is **not cryptographically tamper-proof** against database administrators. No identity, access, approval, or canon authorization is implemented.

## Run from this folder
```sh
python3 -m unittest discover -s . -p 'test_*.py' -v
python3 bridge.py init
python3 bridge.py send --to gemini --body "Review fixture" --source "github:example"
python3 bridge.py inbox --agent gemini
python3 bridge.py audit
```

The database defaults to `oracle_bridge.sqlite3` in the working directory; override with `ORACLE_BRIDGE_DB`. Do not commit the database, API keys, or private material. The local prototype is not an always-on service and requires Python to run. Tests were authored but have **not yet been executed** by this GitHub write operation.

## Safe next engineering gate
Run the tests in a sandbox, verify restart recovery, then add an authenticated provider adapter with minimal scoped credentials, real provider acknowledgement, idempotent delivery, rate limiting, and encrypted secrets. Do not add broad access to private files or claim a production deployment.
