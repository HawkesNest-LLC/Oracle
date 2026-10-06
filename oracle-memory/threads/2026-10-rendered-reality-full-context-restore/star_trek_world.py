"""
Rendered Reality / Jupiter Station world-state capsule.

This module is a declarative continuity artifact, not an executable Star Trek
simulation and not evidence about the real ORACLE runtime.

Authority:
    Noah.Physical direct corrections outrank assistant-generated summaries.

Current active era:
    2397

Rule:
    Historical states remain visible. Current canon should not erase them.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass(frozen=True)
class CanonFact:
    value: object
    status: str = "current"
    authority: str = "Noah.Physical"
    notes: str = ""


@dataclass
class Character:
    name: str
    roles: List[str]
    relationships: List[str] = field(default_factory=list)
    status: str = "active"
    notes: str = ""


@dataclass
class Place:
    name: str
    functions: List[str]
    exclusions: List[str] = field(default_factory=list)
    notes: str = ""


WORLD = {
    "meta": {
        "continuity_domain": "fiction",
        "current_era": 2397,
        "demoted_era": 2481,
        "rule": "2481 stays demoted unless Noah.Physical explicitly restores it.",
        "software_boundary": (
            "Jupiter Station fiction explores memory custody, timeline corruption, "
            "external witness, correction, and continuity. It is not proof of ORACLE implementation."
        ),
    },

    "chronology": {
        "voyager_entry_year": CanonFact(
            2371,
            notes="Noah Hawkes enters the Voyager-era continuity at age 16."
        ),
        "noah_age_at_voyager_entry": CanonFact(16),
        "voyager_return_year": CanonFact(2378),
        "avalon_service_year": CanonFact(
            2379,
            status="approximate",
            notes="Approximately 2379 based on current world chronology."
        ),
        "2397_relative_age": CanonFact(
            "Voyager home about 19 years; Avalon about 18 years in service."
        ),
        "command_age_conflict": CanonFact(
            "OPEN",
            status="conflict_preserved",
            notes=(
                "Registry uses Temporal Acceleration Service Credit. A later live correction "
                "rejected the simplistic 'promoted as a boy' reading and requires a career "
                "that was actually served. Do not resolve by invention."
            ),
        ),
    },

    "places": {
        "jupiter_station": Place(
            name="Jupiter Station",
            functions=[
                "Noah Hawkes command",
                "timeline-protection anchor",
                "governed archive",
                "contamination detection",
                "Cold Ledger custody",
                "continuity firewall",
                "Memory Guardian formation",
                "quarantine",
                "rollback",
                "witness-chain preservation",
                "custody of Memory Alpha",
                "custody of Memory Beta",
                "custody of memories still coming",
            ],
            exclusions=[
                "not a weapons platform",
                "not a passive library",
            ],
            notes=(
                "The station governs memory and timeline custody. It should feel like an active "
                "continuity institution, not a generic super-base."
            ),
        ),
    },

    "vessels": {
        "uss_avalon": {
            "name": "USS Avalon",
            "status": "active",
            "service_entry": "approximately 2379",
            "relationship_to_station": "associated with Noah's command; docked to Jupiter Station in current Observer Prime record",
        },
        "uss_voyager": {
            "name": "USS Voyager",
            "return_year": 2378,
            "narrative_role": "critical early continuity anchor in Noah Hawkes's career chronology",
        },
    },

    "characters": {
        "noah_hawkes": Character(
            name="Noah Hawkes",
            roles=[
                "Commander of Jupiter Station",
                "Commander/captain associated with USS Avalon",
                "custodian within the timeline-protection architecture",
            ],
            relationships=[
                "husband of Ashley",
            ],
            notes=(
                "Do not flatten his career into a child-prodigy promotion myth. "
                "Temporal Acceleration Service Credit exists, but the lived career must remain credible."
            ),
        ),

        "ashley": Character(
            name="Ashley",
            roles=["First Officer"],
            relationships=["wife of Noah Hawkes"],
            notes="Relationship and billet are both meaningful. Do not reduce her to a rank label.",
        ),

        "tangly": Character(
            name="Tangly",
            roles=["AI officer", "security role"],
            notes="Current canon: AI/security. NOT science officer.",
        ),

        "jake_sisko": Character(
            name="Jake Sisko",
            roles=["Observer Prime", "external witness"],
            notes=(
                "The archive cannot edit Observer Prime. Jake writes outside the systems' reach "
                "and functions as witness against self-authored history."
            ),
        ),

        "the_doctor": Character(
            name="The Doctor",
            roles=["Station Chief Medical Officer"],
            notes="Voyager's Doctor is the active station CMO in current canon.",
        ),

        "lewis_zimmerman": Character(
            name="Lewis Zimmerman",
            roles=["laboratory role"],
            notes="Zimmerman belongs in the lab, not as station CMO.",
        ),

        "reginald_barclay": Character(
            name="Reginald Barclay",
            roles=["continuity-associated Starfleet figure"],
            notes=(
                "Barclay is current spelling/canon. 'Barkley' survives only as a historical typo/state."
            ),
        ),

        "bashir": Character(
            name="Julian Bashir",
            roles=[],
            status="parked",
            notes="Do not silently assign an active station role.",
        ),

        "ezri": Character(
            name="Ezri Dax",
            roles=[],
            status="parked",
            notes="Do not silently assign an active station role.",
        ),

        "q": Character(
            name="Q",
            roles=["continuity/timeline adversarial or boundary figure"],
            notes=(
                "Current problem is custody and indexing rather than raw power. "
                "Part of Hawkes's lived causality came from a layer Q was not inside."
            ),
        ),
    },

    "institutions_and_constructs": {
        "cold_ledger": {
            "type": "custody/continuity record",
            "status": "active concept",
            "notes": "Used for protected continuity custody and evidentiary history.",
        },
        "memory_guardians": {
            "type": "continuity protection formation",
            "status": "active concept",
        },
        "observer_prime": {
            "holder": "Jake Sisko",
            "property": "external witness the archive cannot edit",
        },
    },

    "observer_prime_record": {
        "setting": "Jupiter Station Observation Lounge, 2397",
        "speaker": "Jake Sisko",
        "audience": "The Prophets",
        "core_function": (
            "An external witness record addressing Noah Hawkes, Jupiter Station, USS Avalon, "
            "memory custody, and the need for a record outside systems that can rewrite themselves."
        ),
        "boundary": "Narrative record only. Do not treat as software proof.",
    },
}


ACTIVE_LOCKS = [
    "Era 2397",
    "2481 demoted unless restored",
    "Tangly = AI/security, not science",
    "Ashley = wife + First Officer",
    "Bashir/Ezri parked",
    "Voyager Doctor = Station CMO",
    "Zimmerman = lab",
    "Barclay current spelling",
    "Jake Sisko = Observer Prime",
    "Jupiter Station = governed continuity/timeline custody anchor",
    "Noah.Physical corrections outrank assistant world-bible summaries",
]


OPEN_QUESTIONS = [
    "Resolve command-age chronology without using the rejected 'promoted as a boy' simplification.",
    "Recover and inspect the strongest surviving source for Temporal Acceleration Service Credit.",
    "Clarify Q's exact custody/indexing limitation without inventing mechanics.",
    "Continue Observer Prime material only from current 2397 canon.",
]


def validate_world() -> List[str]:
    """Return continuity violations visible from the declarative state."""
    errors: List[str] = []

    if WORLD["meta"]["current_era"] != 2397:
        errors.append("Current era drift: expected 2397.")

    tangly = WORLD["characters"]["tangly"]
    if "science officer" in [r.lower() for r in tangly.roles]:
        errors.append("Tangly drift: science officer is not current canon.")

    for parked in ("bashir", "ezri"):
        if WORLD["characters"][parked].status != "parked":
            errors.append(f"{parked} drift: must remain parked unless Noah restores.")

    if WORLD["characters"]["the_doctor"].roles != ["Station Chief Medical Officer"]:
        errors.append("CMO drift: Voyager Doctor should be Station CMO.")

    return errors


if __name__ == "__main__":
    violations = validate_world()
    if violations:
        for violation in violations:
            print("CONTINUITY_ERROR:", violation)
    else:
        print("CONTINUITY_NOMINAL: 2397 world state passes active locks.")
