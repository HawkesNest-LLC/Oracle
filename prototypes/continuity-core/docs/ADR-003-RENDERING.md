# ADR-003: Render first as a mobile blockout
**Status:** Implemented as an interim 2D schematic.

**Decision:** Use a dependency-free browser interface for the first proof. It supports scene navigation, evidence drill-down, era switching, branch mode, and persistence. A later React/Three.js version can replace the renderer without changing the source or event model.

**Consequence:** The current scene is not 3D and does not satisfy the final visual milestone. It proves navigation and provenance interactions while keeping the first iteration auditable.