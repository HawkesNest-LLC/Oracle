# ADR-001: Dependency-free local reference runtime
**Status:** Accepted for reference prototype; not the final PostgreSQL deployment decision.

**Context:** A runnable proof is needed before cloud provisioning. The target architecture specifies PostgreSQL, but local test infrastructure does not have a running PostgreSQL service.

**Decision:** Implement the first reference API with Node 22 built-in `node:sqlite`, append-only triggers, and an explicit PostgreSQL target migration. Keep schemas and HTTP contracts portable.

**Consequences:** Immediate reproducible tests without cloud spend or credentials. SQLite is not a substitute for PostgreSQL security roles or production multi-user concurrency. PostgreSQL migration execution and role provisioning remain pending.