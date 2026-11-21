# ADR-002: Canon and simulation isolation
**Status:** Implemented in reference runtime.

**Decision:** Canonical claims and assertions live in immutable tables. Simulation events live in a separate append-only event table, require `sim-` branch IDs, and cannot write assertions. The reference HTTP API has no enabled canon-promotion route.

**Consequence:** Simulated visits are durable but do not modify canon. A future Creator review workflow must use verified identity and explicit approval, not a client-supplied authority string.