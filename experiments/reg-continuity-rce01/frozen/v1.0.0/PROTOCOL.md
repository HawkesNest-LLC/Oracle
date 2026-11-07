# Jupiter Station RCE-01 | Frozen Evaluation Protocol v1.0.0

**Creator:** Noah.Physical. **Budget:** $0 incremental. **Engineering:** AI-operated. **CC-90-001:** unchanged.

**Packet:** 12 public fiction-derived paraphrases, 3 separate compiled recovery/context paraphrases, 9 labeled artificial adversarial/derivative/simulation records. Full 24-record evaluation case and 16 fixed probes are in `cases/jupiter_station_case.json`. Public gold key is `cases/jupiter_station_key.json`; **do not include it in model prompts**. The source types are separately listed in `public_fiction_core.json`, `published_recovery_context.json`, and `isolated_lab_challenges.json`. Laboratory branches do not change story canon.

**Frozen evaluation:** `RUBRIC.md` and `benchmark.mjs`. The tests in `tests/` are included with both old synthetic control cases. The parent repository has a recorded 41/41 test result; the standalone package was also re-executed and verified locally at freeze.

**For future AI engineering agents:** (1) verify freeze file integrity; (2) deliver identical selected packet, 16 probes and instructions to each model, excluding gold key; (3) record model build, context-isolation method, exact prompt, temperature/settings, tokenizer usage if measurable, and verbatim response; (4) score using frozen executable; (5) record all failures, source errors and UNKNOWN handling; (6) compare a strong RAG or long-context baseline **within the same model** with matched information access and measured tokens; (7) publish negative results too.

**Critical study limitation:** This public answer key cannot function as a hidden holdout. The structured and linearized packet formats in the research parent are not yet a controlled matched-token experiment. No model superiority or actual cross-model run is claimed by freezing this benchmark.

**Approval boundary:** Remains a draft research sidecar in PR #7. Do not merge or extend CC-90-001 without Creator review.
