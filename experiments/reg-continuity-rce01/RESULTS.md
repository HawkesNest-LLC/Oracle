# RCE-01 | Local Execution Receipt

**Executed:** November 5, 2026 (America/Chicago; container reported November 6 UTC)  
**Environment:** Node.js v22.16.0; Python 3.13.5; no third-party Node packages  
**Procedure:** Source-grounded synthetic-fixture validation, not real cross-model benchmarking  
**Audience:** Noah.Physical and authorized AI engineering agents

## Actual commands executed

```sh
npm test
node benchmark.mjs doctor cases/synthetic_case.json cases/demo_key.json
node benchmark.mjs prepare cases/synthetic_case.json structured packets/structured.txt 1800
node benchmark.mjs prepare cases/synthetic_case.json linearized packets/linearized.txt 1800
node benchmark.mjs demo
```

## Results

- **23 / 23 automated harness tests passed.** Output: `results/npm-test-output.txt`.
- Doctor validated **14 source records, 10 prompts**, all six dimensions, and separate alpha and beta branches.
- Grounded pre-authored fixture: **10/10** prompts pass.
- Deliberately drifted pre-authored fixture: **4/10** prompts pass; correction, attribution, copied-source inflation, false certainty, branch crossover, and invented beta commitment are caught.
- Both evidence packet modes include all **14** artificial sources. Structured uses **about 500 words**; linearized uses **about 600 words**. Exact counts are preserved in `results/prepare-*.json`.
- The scorer rejects duplicate or unknown prompt IDs, unsupported status, fabricated source IDs, cross-branch evidence, answer omissions, wrong correction state, and hallucinated UNKNOWN conclusions.
- File hashes: `results/SHA256SUMS.txt` includes SHA-256 of core source files and specifications.

## What the receipt does not prove

No real AI model was called during these tests. Fixture outputs were authored to validate the grading function. **10/10 and 4/10 are deliberately constructed test inputs, not measurements of AI capability or evidence that structured memory beats RAG.** There is no verified equal *model-token* budget, no blind human scoring, no statistical result, no production NPC, no deployed holodeck, and no offscreen runtime.

**Status:** HARNESS VERIFIED LOCALLY. CROSS-MODEL FIDELITY DIFFERENCE UNKNOWN.

No extra paid services or API calls were used. The separate 90-day CC-90-001 work remains unchanged.
