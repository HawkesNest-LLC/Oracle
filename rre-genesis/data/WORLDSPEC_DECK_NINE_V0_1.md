# WorldSpec Deck Nine v0.1

First WorldSpec for the RRE Genesis vertical slice, compiled November 6,
2026, by Merlin, schema and data designer for RRE Genesis v0.1, at the
direction of the Rendered Reality Open World directive issued by
Noah.Physical the same day.

Status: DRAFT. Not approved. Not canon. This WorldSpec is a draft for
Noah's review. It does not authorize a build on its own.

File: `worldspec-deck-nine-v0.1.json` (this document explains that file).

## The cell

The initial world cell is directive section 21, eight locations:

1. Hawkes family quarters on Deck Nine
2. Ellie's quarters
3. Adjacent residential corridor
4. Ellie's observation alcove
5. Turbolift
6. Station command access
7. Avalon docking connection
8. Avalon's bridge

One further location is listed for reference only and is flagged
`in_cell: false`: Ellie's small cabin aboard Avalon. Its contents are
established by Noah's November 1 record, but the cabin is not on Deck
Nine, so it is not part of the v0.1 cell. It is included because the cell
includes the docking connection to Avalon, and a reader of the cell
should be able to find the cabin contents without mistaking them for
Deck Nine contents.

## The provenance standard

Every rendered object must answer "where did you come from?" Every
location and every object in this WorldSpec carries an id, a location, a
provenance value, a source locator, and notes. A rendered object with no
provenance value is not a valid object in this WorldSpec.

The four provenance values:

- **ESTABLISHED**: a source establishes this thing. The source locator
  names the source and the precise pointer, for example "100 statements
  st. 25" or "Canon Merge section 6". The mug, the books left open, the
  sweater over a chair, the plant near the window, the antique desk, the
  basil, the citrus tree, the journal, the door chime, the two alcove
  seats, the turbolift car, and the Avalon cabin contents are ESTABLISHED
  this way.
- **RECONSTRUCTED**: compiled from evidence by FORGE. The source locator
  names the evidence. The Hawkes quarters details from directive
  section 21 are RECONSTRUCTED, not ESTABLISHED, because the directive
  lists them as recovered details without citing the underlying primary
  source for each one. They are real recovered claims, and the directive
  is a Noah-issued document, but the directive itself says to treat exact
  details according to their source status and not to convert prose
  automatically into canon geometry without provenance. So each detail
  is recorded with the directive as its locator and a note stating that
  the underlying primary source is not cited. The science AI station on
  the bridge and the berth twelve marker are RECONSTRUCTED the same way.
- **GENERATED_VISUAL**: FORGE or LACUNA generated this detail so the
  room can render. There is no source locator, and the notes must state
  the gap and name the generator. Corridor wall panels, corridor
  lighting, turbolift controls, the station command access terminal, the
  docking umbilical, and the bridge seating are GENERATED_VISUAL in this
  WorldSpec.
- **UNKNOWN**: not established. The gap is preserved as a successful
  result, not filled with plausible invention. The wall materials in
  both quarters are UNKNOWN. The exact layout and dimensions of both
  quarters are UNKNOWN. The full list is in the UNKNOWN section below
  and in the JSON `unknown_items` array.

## The FORGE and LACUNA labeling rules

FORGE is the world compiler. It converts source evidence into a
WorldSpec. LACUNA is the governed gap-filling engine. It generates
details necessary to produce a coherent world when the corpus is
incomplete, constrained by established architecture, period, style,
nearby evidence, physical plausibility, story branch, cultural context,
privacy rules, and existing canon.

The labeling rules, applied to every object in this WorldSpec:

1. A detail a source establishes is labeled ESTABLISHED, with the
   source locator.
2. A detail compiled from evidence is labeled RECONSTRUCTED, with the
   source locator and a note saying what was compiled and from what.
3. A detail generated so the room can render is labeled
   GENERATED_VISUAL, with a LACUNA note and no source locator. The note
   names the generator (FORGE or LACUNA) and the constraints it
   respected. A generated detail is never canon.
4. A detail no source establishes and no generator has filled is labeled
   UNKNOWN, with the gap stated.
5. A generated detail is never labeled ESTABLISHED or RECONSTRUCTED.
   Generation is not evidence.
6. Repeated generation is never corroboration. Generating the same wall
   texture twice does not make it established. It makes it generated
   twice.
7. Privacy rules bind the generators. The journal exists in the world;
   its contents are private and are not a runtime resource. No generator
   may fill its pages. The holographic backyard program's contents are
   not a license to render private family life.

## The GENERATED to CREATOR_APPROVED transition

A generated choice can later become creator-approved if Noah explicitly
adopts it. The transition is:

GENERATED to CREATOR_APPROVED

It is recorded, never automatic, and never by repetition. In the
database schema (`rre-genesis-schema.sql`), the transition is a new
assertion with status ESTABLISHED and authority Creator, plus a revision
row carrying the reason, recorded by the continuity_creator role. The
earlier GENERATED_VISUAL state stays in the record; it is not deleted or
overwritten. Until that recorded transition exists, a generated detail
stays generated, however often it has been rendered and however good it
looks.

No generated detail in this WorldSpec has made that transition. Every
GENERATED_VISUAL object in the JSON is still generated.

## The persistence test object

The mug in Ellie's quarters (`obj-ellie-quarters-mug`) is the persistence
test object. It is ESTABLISHED by Noah's November 1 record: a mug she
repeatedly carries into the wrong room. Its position is authoritative
world state. Every move is an executed event with a receipt: what
happened, who did it, who witnessed it, when, which branch, what changed,
and whether it came from authored history or executed history. The test
procedure is recorded in the JSON under `persistence_test` and follows
directive sections 16 and 27: place the mug, record its position, cold
restart, return, and ask how the mug got here.

The mug's color, size, and contents are not established. Its position is
authoritative state; its appearance is a rendering choice, not canon.

## What is ESTABLISHED in this cell, and what is not

ESTABLISHED, with source locators: Ellie's quarters and their contents
(books left open, sweater over a chair, plant near the window, mug,
antique desk, basil, citrus tree, journal, door chime, blanket, window
facing the ship berths); the observation alcove with its two seats and
imperfect view of Jupiter; the turbolift car; the Avalon bridge as a
place where Ellie serves; the Avalon cabin contents (reference only).

RECONSTRUCTED, with the directive or the episode as locator: the Hawkes
quarters and their listed details (curved residential geometry, warm
domestic lighting, Jupiter dominating the windows, Avalon visible
outside, station life visible outside, wood-grain cabinet fronts,
functional kitchen, family objects, animal feeding area, holographic
backyard threshold, patio, grass and trees inside the program, domestic
clutter); the adjacent residential corridor; the station command access
as a location; the Avalon docking connection and berth twelve marker;
the science AI station on the bridge.

GENERATED_VISUAL, with LACUNA notes: corridor wall panels and lighting,
turbolift controls, station command access terminal, docking umbilical
and airlock, bridge seating.

UNKNOWN, with gaps stated: see the list below.

## List of UNKNOWN items in the cell

- Exact wall materials, both quarters. No source specifies them. FORGE
  may generate a texture; it stays GENERATED_VISUAL.
- Exact layout and dimensions of the Hawkes family quarters and Ellie's
  quarters. No plan, dimension, or room count is given.
- Individual family objects and domestic clutter items. No individual
  item is named in the directive. Each must be added with its own source
  locator.
- Hawkes quarters lighting fixtures. No fixture, color temperature, or
  control is specified.
- Hawkes quarters window count, size, and placement.
- Holographic backyard program details. Program name, trigger, and
  boundary behavior are not established.
- Residential corridor geometry. No source read for this package
  describes the corridor's position relative to the two quarters, its
  length, or its fixtures.
- Station command access geometry and equipment. The authority fact
  (Ashley commands the station) is established; the room is not.
- Avalon docking connection geometry. Airlock configuration and
  umbilical layout are not established.
- Avalon bridge layout. No source read for this package describes the
  bridge layout, station positions, or fixtures beyond the science AI
  station.
- Mug appearance. Color, size, and contents are not established.
- Citrus tree species and plant placement. Species of citrus, pot, and
  placement are not established. The first plant's species is also not
  stated.
- Family photograph contents. Who is in the photograph, its size, and
  its framing are not established.
- Journal contents. Private by design. Its existence is established;
  its text is UNKNOWN and must stay that way.
- Avalon cabin personal things, itemized. No source read for this
  package names the contents beyond desk, bed, a few personal things,
  and a photograph of the family.

## What this WorldSpec does not do

- It does not promote candidate fiction into canon. The Unbreakable
  Tether doctrine, the Room That Remembers biobed scene, and The
  Unbroken Chorus do not appear in this WorldSpec at all, and no
  candidate material is marked ESTABLISHED anywhere in it.
- It does not settle the broader canon-order question (repo commit
  7be9dda, November 5, 2026). Unverified, awaiting Noah's ruling.
- It does not settle the registry question (NCC-75154 versus
  NCC-75154-JS). Open. The WorldSpec uses the base registry NCC-75154
  in the Ellie package and flags the series styling as open.
- It does not use the trajectory model. Trajectory is pending Creator
  approval and is not the governing architecture. No trajectory field
  is present.
- It does not render the journal's pages, expose its text, or treat
  private memory as a bridge resource.
- It does not claim the Hawkes quarters details are established canon
  geometry. They are RECONSTRUCTED from the directive's listing, and
  each carries a note saying the underlying primary source is not cited.
  A primary source locator for each detail is still needed before any
  of them can become ESTABLISHED.

## What Noah is being asked, when he is ready

1. That the provenance marking in this WorldSpec is correct: that the
   ESTABLISHED items are established, the RECONSTRUCTED items are
   honestly marked as reconstructions, the GENERATED_VISUAL items are
   labeled generated, and the UNKNOWN items are gaps, not oversights.
2. The UNKNOWN items above, which only he or a primary source he names
   can resolve.
3. Whether the Hawkes quarters details from directive section 21 should
   stay RECONSTRUCTED, be promoted with primary source locators, or be
   corrected.
4. Whether the cell, as a draft, is the right starting state for the
   first runtime version.
