# Reg Continuity Experiment | RCE-01

**Captain's brief:** We built a tiny, inspectable research instrument that can tell the difference between a system that preserves a corrected, sourced history and one that quietly makes things up. It uses imaginary crew logs. It does not require Noah to program or pay for anything.

**Current verdict:** Harness tested, cross-model hypothesis not yet tested.

- 14 artificial source records and 10 evidence questions.
- All six continuity dimensions covered, plus branch and commitment/trajectory checks.
- Two sample answer sets: deliberately grounded and deliberately drifted. Both are fixtures, not model outputs.
- Independent Node.js tests and exact diagnostic reports. No external packages, API keys, or cloud services.
- `SPEC.md` defines the real future study, controls, acceptance criteria, and hard limits of the current pilot.

## Project layout

```text
benchmark.mjs                   Deterministic source and branch scorer
cases/synthetic_case.json       Model-facing synthetic evidence and questions
cases/demo_key.json             Development key (never send to tested model)
samples/grounded.json           Correct example (not a model response)
samples/drifted.json            Intentionally corrupted example (not a model response)
packets/structured.txt          Generated packet for one format
packets/linearized.txt          Generated packet for control format
results/demo_*.json             Actual local fixture-scoring output
tests/benchmark.test.mjs        Automated harness tests
SPEC.md                         Formal study protocol
RESULTS.md                      Actual local test and integrity receipt
```

## For AI engineering agents, not Noah

Requires Node.js 22; dependencies: none.

```sh
npm test
npm run doctor
npm run demo
node benchmark.mjs prepare cases/synthetic_case.json structured packets/structured.txt 1800
node benchmark.mjs prepare cases/synthetic_case.json linearized packets/linearized.txt 1800
node benchmark.mjs score cases/synthetic_case.json cases/demo_key.json samples/grounded.json results/check.json
```

The packet contains all synthetic records, but no hidden expected-answer object. It remains a pilot: the `1800` value is a **word cap**, not a true per-model token budget. For real research, report actual tokenizer usage and use genuinely independent, held-out tasks. Do not assert model gains from the pre-authored answer fixtures.

**Existing CC-90-001 remains the engineering priority.** This branch is a no-cost research sidecar for review, not a replacement for Brakk's browser/SQLite reconciliation repair.
