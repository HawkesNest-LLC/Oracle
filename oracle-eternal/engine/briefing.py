"""Captain's morning briefing.

One mobile-readable file, generated from the ledger and the queue.
It reports only what the record shows: discoveries, writings, failures,
decisions awaiting Noah.Physical, costs, and the next proposed
assignment. It never invents findings.
"""

from __future__ import annotations

from . import ledger as ledger_mod


def render(ledger: dict, queue: dict, config: dict, briefing_date: str) -> str:
    entries = ledger["entries"]
    runs = [e for e in entries if e.get("event") == "execution"]
    completed = [e for e in runs if e.get("status") == "completed"]
    abstained = [e for e in runs if e.get("status") == "abstained"]
    failed = [e for e in runs if e.get("status") in ("failed", "blocked")]
    total_cost = sum(float(e.get("cost_usd", 0.0)) for e in runs)
    done_ids = ledger_mod.completed_assignment_ids(ledger)
    nxt = None
    for assignment in queue["assignments"]:
        if assignment["id"] not in done_ids and assignment["status"] == "queued":
            nxt = assignment
            break

    lines = [
        "# Captain's morning briefing",
        "",
        "ORACLE Eternal. Date: %s. Generated from the execution ledger." % briefing_date,
        "",
        "## While you were away",
        "",
    ]
    if completed:
        for entry in completed[-5:]:
            lines.append(
                "- Completed: %s (%s). Artifact: `%s`."
                % (
                    entry.get("artifact_title", entry.get("assignment_id", "?")),
                    entry.get("artifact_id", "?"),
                    entry.get("artifact_path", "?"),
                )
            )
    else:
        lines.append("- No completed executions recorded yet.")
    if abstained:
        for entry in abstained[-3:]:
            lines.append(
                "- Abstained: %s. Reason: %s."
                % (entry.get("assignment_id", "?"), entry.get("reason", "not recorded"))
            )
    if failed:
        for entry in failed[-3:]:
            lines.append(
                "- Failed or blocked: %s. Reason: %s."
                % (entry.get("assignment_id", "?"), entry.get("reason", "not recorded"))
            )
    lines += [
        "",
        "## Why it matters",
        "",
        "Each completed artifact is reviewable in the repository, with its "
        "sources, evidence class, and receipt attached. Nothing here is "
        "canon and nothing was published automatically.",
        "",
        "## New scientific findings",
        "",
        "None recorded by the engine. Findings require a completed, "
        "reviewed artifact that states them; the ledger holds none.",
        "",
        "## Decisions requiring your approval",
        "",
        "- Merge the ORACLE Eternal review branch to activate scheduled execution.",
        "- Any model execution path and its spending limit, before it is enabled.",
        "- Any canon promotion, any private staging, and any public "
        "publication beyond review branches.",
        "",
        "## Operating costs",
        "",
        "Total recorded execution cost: $%.2f. Scheduled runs on the public "
        "repository use free standard GitHub-hosted runner minutes; model "
        "execution is not configured, so no model spend is recorded." % total_cost,
        "",
        "## Tomorrow's proposed assignment",
        "",
    ]
    if nxt:
        lines.append("- %s (%s): %s" % (nxt["title"], nxt["id"], nxt.get("brief", "")))
    else:
        lines.append("- Queue exhausted. No assignment proposed until the queue is extended.")
    lines += [
        "",
        "## Limits in force",
        "",
        "- Maximum %d successful execution(s) per day." % config.get("max_daily_executions", 1),
        "- Manuscript limit: %d words." % config.get("max_words", 5000),
        "- Model execution: %s." % ("configured" if config.get("model_configured") else "not configured; abstention applies"),
        "- Paused: %s." % ("yes" if config.get("paused") else "no"),
        "",
        "Ledger entries: %d. The human keeps the keys. The system keeps the receipts." % len(entries),
        "",
    ]
    return "\n".join(lines)
