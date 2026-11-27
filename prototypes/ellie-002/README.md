# ELLIE-002 | local correction-ledger experiment

**Status:** deterministic plumbing tested locally, AI reasoning **BLOCKED / NOT TESTED**, no canon promotion.

**Sources:** [ELLIE-002 specification in PR #30](https://github.com/HawkesNest-LLC/Oracle/pull/30); [Ellie handoff PR #29](https://github.com/HawkesNest-LLC/Oracle/pull/29).

## Honest execution record
A local Python standard-library prototype ran seven synthetic events and verified a SHA-256 event chain, separate actor attribution, preservation of a tentative first reading, later correction, and persistent SQLite state in a fresh Python process. The locally executed script produced final hash `72ddea129a0521eab174b7330a8d4fbdb8ed07218f963124ffb6539409c95e0d`. The script published here is a **separately transcribed, equivalent demonstration** and its event wording differs from the locally executed script; therefore **do not expect the same final hash**. The exact locally executed script and DB were not uploaded to GitHub, and the GitHub version has not been rerun in this tool session.

Run this repository version with `python run.py run`, then from a **new process** `python run.py verify`. The run command replaces its local SQLite database. No third-party dependencies.

## Model execution blocker
No `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GEMINI_API_KEY` was configured in the available local execution environment. A live model call was not attempted. There were no independent model-generated decisions, separate model contexts, or actual hidden-source novelty evaluation. The synthetic clue was withheld in the scripted event sequence only, not from an LLM. This is **not** an ELLIE-002 relational-independence pass.

## Boundaries
This public branch contains only fictional synthetic text. No personal archives, private recordings, or corpus contents. The journal is a scripted report, not Ellie's independent creative output. Six-property rubric: self-model NOT TESTED; temporal continuity PASS (storage only); embodied learning NOT TESTED; independent perspective NOT TESTED (scripted); integrated decision-making NOT TESTED; relational independence NOT TESTED. Subjective experience unclaimed. Scenes 3 and 4 remain outside PR #29 and canon. Noah.Physical retains final authority.

## Next
Connect an authorized inference runtime without publishing secrets, run real Ellie/Reg separate contexts with a genuinely withheld fixture, capture exact prompt/model and event receipts, and perform independent cold-start verification.
