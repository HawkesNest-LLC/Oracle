# RRE Genesis v0.1 Cold-Restart Receipt

Directive section 16 persistence test (the mug test) and section 27
scenario. This receipt was produced by actually running the commands
below on November 6, 2026, not written from memory. No screenshots or
video exist for this deliverable.

## Commands run

Run from `~/workspace/rre-genesis-staging/build`:

```sh
node demo/scenario-27.mjs
node demo/verify-db.mjs
node --test tests/properties-26.test.mjs tests/rules.test.mjs
```

Node version: v24.22.1. No dependencies installed. No network used.

## Demo output (verbatim)

The demo starts from a fresh database file, runs the section 27
scenario, closes the database, reopens it from the same file, and
continues. Exit code 0.

```
RRE GENESIS v0.1  SECTION 27 TEST SCENARIO
==========================================

Database: /home/hatch/workspace/rre-genesis-staging/build/data/rre-genesis-v0.1.db (fresh file for this run)

World loaded: 8 locations in cell, 41 objects, 8 sources, 93 claims.

PASS  Ellie runtime instantiated with bounded knowledge  scope=ellie-genesis-v0.1
PASS  Noah.Physical enters Ellie quarters; Ellie is present  Ellie is in Ellie's quarters, Jupiter Station
  Noah session: ses-90fd2054. Ellie location: Ellie's quarters, Jupiter Station.

Noah: What is your rank and field?
Ellie: Her rank is lieutenant junior grade and her field is science AI and continuity systems, aboard Avalon. Source: Canon Merge section 1 and section 4; Compendium Part 5, section 5.2; 100 statements st. 41.
PASS  Ellie answers an established question from bounded knowledge with its source  knowledge=bk-02, source=Canon Merge section 1 and section 4; Compendium Part 5, section 5.2; 100 statements st. 41

Noah: What is Sparrow?
Ellie: I don't know. What is Sparrow, and what is the next investigation? Status: UNKNOWN. Only Noah.Physical can answer this.
PASS  Ellie says she does not know for an unresolved question  knowledge=unknown-11, status=UNKNOWN

Mug before move: position=desk, location=loc-ellie-quarters.
Move proposal 1: validated and executed
PASS  Noah moves the mug through a validated action proposal  event=4, position=windowsill

PASS  Ashley.Physical joins the same world instance and sees the mug moved  Ashley session=ses-5690cf8c, mug position=windowsill

PASS  Noah.Physical leaves; the world continues  Ashley session still active

STATE BEFORE SHUTDOWN
  Mug position: windowsill
  Executed events on HOME: 6
  Head event hash on HOME: 25fb436b016f22833ae46b34c90bc3ed1749228f56cc57519137846eb74d702b
Processes stopped. Database closed.
Processes restarted. Database reopened from the same file.

STATE AFTER RESTART
  Mug position: windowsill
  Executed events on HOME: 6
  Head event hash on HOME: 25fb436b016f22833ae46b34c90bc3ed1749228f56cc57519137846eb74d702b
PASS  Mug remains moved after cold restart  position=windowsill

PASS  Noah returns after restart and the mug is still moved  position=windowsill

PASS  Ellie remembers the executed encounter she witnessed  memories held=3, move event remembered=true
  Ellie memory: Noah.Physical moved Mug from desk to windowsill.

HOW DID THE MUG GET HERE?
  What happened: Noah.Physical moved Mug from desk to windowsill in Ellie's quarters, Jupiter Station.
  Who did it: Noah.Physical (human)
  Who witnessed it: run-ellie-hawkes
  When: 2026-11-07T00:01:29.694Z
  Which branch: HOME
  What changed: {"object":"obj-ellie-quarters-mug","from":{"location":"loc-ellie-quarters","position":"desk"},"to":{"location":"loc-ellie-quarters","position":"windowsill"}}
  History kind: executed (executed history, not authored history)
PASS  Event lookup answers what, who, witnesses, when, branch, what changed, and history kind  event=4

Provenance of the mug: ESTABLISHED, source: Canon Merge section 6; Compendium Part 5, section 5.6; 100 statements st. 25; Directive section 16
PASS  Executed event hash chain verifies  checked=7 events
Ledgers: sources=8, claims=93, executed events=7, simulation events=3.

VERIFICATION SUMMARY
  Steps passed: 12
  Steps failed: 0
  Result: ALL STEPS PASS
DEMO-EXIT:0
```

## State before shutdown vs after restart

| Item | Before shutdown | After restart |
| --- | --- | --- |
| Mug position | windowsill | windowsill |
| Executed events on HOME | 6 | 6 |
| Head event hash on HOME | 25fb436b016f22833ae46b34c90bc3ed1749228f56cc57519137846eb74d702b | 25fb436b016f22833ae46b34c90bc3ed1749228f56cc57519137846eb74d702b |

Identical. The mug survived the cold restart, and the event count
and head hash are unchanged across it.

## Independent verification (verbatim)

`node demo/verify-db.mjs`, run after the demo process exited, opening
the same database file. Exit code 0.

```
RRE GENESIS v0.1 DATABASE VERIFICATION
Database: /home/hatch/workspace/rre-genesis-staging/build/data/rre-genesis-v0.1.db
Mug position: windowsill
Mug location: loc-ellie-quarters
Mug history kind: executed
Mug provenance: ESTABLISHED
Mug source locator: Canon Merge section 6; Compendium Part 5, section 5.6; 100 statements st. 25; Directive section 16
Executed events on HOME: 9
Head event hash on HOME: c1dbab0cc15c183756ddc339414cd71a8c576934f924a1242d9c24e32b5780e7
Hash chain verifies: true (checked 9 events)
Ellie memories held: 3
How did the mug get here?
  What happened: Noah.Physical moved Mug from desk to windowsill in Ellie's quarters, Jupiter Station.
  Who did it: Noah.Physical (human)
  Who witnessed it: run-ellie-hawkes
  When: 2026-11-07T00:01:29.694Z
  Which branch: HOME
  What changed: {"object":"obj-ellie-quarters-mug","from":{"location":"loc-ellie-quarters","position":"desk"},"to":{"location":"loc-ellie-quarters","position":"windowsill"}}
  History kind: executed
VERIFICATION PASSED
VERIFY-EXIT:0
```

Why the verification shows 9 events and a different head hash than
the demo's restart check: after the verification summary, the demo
exits the two remaining sessions (Noah's return session and Ashley's
session), which writes two `session_end` events. So the final ledger
holds 9 events on HOME (7 at the summary, plus 2 session ends), and
the head hash advances to
c1dbab0cc15c183756ddc339414cd71a8c576934f924a1242d9c24e32b5780e7. The
mug position, the move receipt, and the move event itself are
unchanged. The hash chain verifies across all 9 events.

## How did the mug get here (event lookup answer)

- What happened: Noah.Physical moved Mug from desk to windowsill in
  Ellie's quarters, Jupiter Station.
- Who did it: Noah.Physical (human).
- Who witnessed it: run-ellie-hawkes (Ellie Hawkes).
- When: 2026-11-07T00:01:29.694Z.
- Which branch: HOME.
- What changed: the mug (`obj-ellie-quarters-mug`) moved from
  position `desk` to position `windowsill`, staying in
  `loc-ellie-quarters`.
- Authored or executed history: executed. The move is event 4 in the
  `executed_events` ledger. The mug's existence is recovered history
  (ESTABLISHED, Canon Merge section 6; Compendium Part 5, section 5.6;
  100 statements st. 25; Directive section 16); its moved position is
  executed history.

## Test suite result

`node --test tests/properties-26.test.mjs tests/rules.test.mjs`:
24 tests, 24 pass, 0 fail. The suite covers all 15 properties from
directive section 26, branch isolation, the AI-cannot-mutate-state
rule, append-only enforcement, and hash-chain integrity.
