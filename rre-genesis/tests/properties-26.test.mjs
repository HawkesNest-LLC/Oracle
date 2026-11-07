// RRE Genesis v0.1 tests: directive section 26, all 15 properties.
// Each property has at least one named test. Tests use fresh temporary
// databases, one per test, and the Node.js standard library only.

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { readFileSync } from 'node:fs';
import { RREWorld, MUG_ID, ELLIE_LOCATION_ID } from '../src/world.mjs';

const dataRoot = join(import.meta.dirname, '..', 'data');
const worldspec = JSON.parse(readFileSync(join(dataRoot, 'worldspec-deck-nine-v0.1.json'), 'utf8'));
const ellie = JSON.parse(readFileSync(join(dataRoot, 'ellie-genesis.json'), 'utf8'));

function freshWorld() {
  const dir = mkdtempSync(join(tmpdir(), 'rre-test-'));
  return new RREWorld({ dbPath: join(dir, 'test.db'), worldspec, ellie });
}

function moveMug(world, sessionId, toPosition = 'windowsill') {
  const proposal = world.proposeAction({
    proposerType: 'human',
    proposerId: 'Noah.Physical',
    action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition },
    targetObjectId: MUG_ID,
    branchId: 'HOME',
    sessionId,
  });
  return world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
}

test('property 1: ingest a bounded set of actual Noah sources', () => {
  const world = freshWorld();
  try {
    const sources = world.listSources();
    const ids = sources.map((s) => s.id);
    assert.ok(ids.includes('src-ellie-compendium'), 'compendium source ingested');
    assert.ok(ids.includes('src-ellie-canon-merge'), 'canon merge source ingested');
    assert.ok(ids.includes('src-directive-2026-11-06'), 'directive source ingested');
    assert.ok(ids.includes('src-worldspec-deck-nine'), 'worldspec source ingested');
    assert.ok(ids.includes('src-ellie-genesis'), 'ellie genesis source ingested');
    assert.equal(world.countSources(), 8, '3 vendored PR #4 sources plus 5 RRE sources');
  } finally {
    world.close();
  }
});

test('property 2: immutable source identities', () => {
  const world = freshWorld();
  try {
    assert.throws(
      () => world.db.exec("UPDATE sources SET title = 'tampered' WHERE id = 'src-ellie-genesis'"),
      /append-only/,
      'UPDATE on sources is rejected',
    );
    assert.throws(
      () => world.db.exec("DELETE FROM sources WHERE id = 'src-ellie-genesis'"),
      /append-only/,
      'DELETE on sources is rejected',
    );
    assert.ok(world.getSource ? true : world.core.getSource('src-ellie-genesis'), 'source still present');
    assert.equal(world.core.getSource('src-ellie-genesis').title, 'Ellie Genesis Package v0.1');
  } finally {
    world.close();
  }
});

test('property 3: claims with source locators', () => {
  const world = freshWorld();
  try {
    const claim = world.getClaim('bk-02');
    assert.ok(claim, 'bounded knowledge claim bk-02 exists');
    assert.equal(claim.status, 'ESTABLISHED');
    const locators = world.getClaimLocators('bk-02');
    assert.ok(locators.length >= 1, 'claim carries at least one source locator');
    assert.ok(locators[0].locator.includes('Canon Merge'), 'locator names the canon merge');
    const objectClaim = world.getClaim(`claim-${MUG_ID}`);
    assert.ok(objectClaim, 'mug object claim exists');
    assert.equal(objectClaim.status, 'ESTABLISHED');
    assert.ok(world.getClaimLocators(`claim-${MUG_ID}`).length >= 1, 'mug claim carries a locator');
  } finally {
    world.close();
  }
});

test('property 4: preserve UNKNOWN', () => {
  const world = freshWorld();
  try {
    const unknown = world.getClaim('unknown-11');
    assert.ok(unknown, 'Sparrow unknown claim exists');
    assert.equal(unknown.status, 'UNKNOWN');
    assert.deepEqual(unknown.sources, [], 'UNKNOWN claim stands without sources');
    const answer = world.askEllie('What is Sparrow?');
    assert.equal(answer.status, 'UNKNOWN');
    assert.ok(answer.answer.startsWith("I don't know"), 'Ellie says she does not know');
    assert.ok(!answer.answer.includes('bird'), 'no invented answer is supplied');
  } finally {
    world.close();
  }
});

test('property 5: compile one persistent world cell', () => {
  const world = freshWorld();
  try {
    assert.equal(world.countLocationsInCell(), 8, 'eight locations in the Deck Nine cell');
    assert.equal(world.countObjects(), 41, '41 objects in the cell');
    const state = world.getObjectState(MUG_ID, 'HOME');
    assert.ok(state, 'mug has initial state');
    assert.equal(state.locationId, ELLIE_LOCATION_ID);
    assert.equal(state.position, 'desk');
    assert.equal(state.historyKind, 'recovered');
  } finally {
    world.close();
  }
});

test('property 6: visibly distinguish established and generated details', () => {
  const world = freshWorld();
  try {
    const mug = world.getProvenance(MUG_ID);
    assert.equal(mug.provenance, 'ESTABLISHED');
    assert.ok(mug.sourceLocator, 'established object carries a source locator');
    const panels = world.getProvenance('obj-corridor-wall-panels');
    assert.equal(panels.provenance, 'GENERATED_VISUAL');
    assert.equal(panels.sourceLocator, null, 'generated detail carries no source locator');
    const wall = world.getProvenance('obj-ellie-quarters-wall-material');
    assert.equal(wall.provenance, 'UNKNOWN');
    const counts = world.db.prepare(
      'SELECT provenance_id, COUNT(*) n FROM world_objects GROUP BY provenance_id',
    ).all();
    const byProvenance = Object.fromEntries(counts.map((c) => [c.provenance_id, c.n]));
    assert.ok(byProvenance.ESTABLISHED > 0, 'established objects present');
    assert.ok(byProvenance.GENERATED_VISUAL > 0, 'generated objects present');
    assert.ok(byProvenance.UNKNOWN > 0, 'unknown objects present');
    assert.ok(byProvenance.RECONSTRUCTED > 0, 'reconstructed objects present');
  } finally {
    world.close();
  }
});

test('property 7: instantiate Ellie with bounded knowledge', () => {
  const world = freshWorld();
  try {
    const runtime = world.instantiateEllie();
    assert.equal(runtime.runtime_id, 'run-ellie-hawkes');
    assert.equal(runtime.knowledge_scope, 'ellie-genesis-v0.1');
    assert.equal(runtime.location_id, ELLIE_LOCATION_ID);
    assert.equal(world.ellie.bounded_knowledge.length, 34, '34 bounded knowledge entries');
    const where = world.whereIsEllie();
    assert.equal(where.present, true);
    assert.equal(where.locationId, ELLIE_LOCATION_ID);
  } finally {
    world.close();
  }
});

test('property 8: allow Noah.Physical to enter', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const session = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    assert.ok(session.sessionId, 'session created');
    assert.equal(world.isSessionActive(session.sessionId), true);
    assert.equal(world.getActiveSessions('HOME').length, 1);
  } finally {
    world.close();
  }
});

test('property 9: permit a second authenticated human participant', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    const ashley = world.enterHuman('Ashley.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    assert.notEqual(noah.sessionId, ashley.sessionId, 'distinct sessions');
    const active = world.getActiveSessions('HOME').map((s) => s.human_identity);
    assert.ok(active.includes('Noah.Physical'), 'Noah active');
    assert.ok(active.includes('Ashley.Physical'), 'Ashley active');
    assert.equal(active.length, 2, 'two participants in the same world instance');
  } finally {
    world.close();
  }
});

test('property 10: allow shared object interaction', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    const moved = moveMug(world, noah.sessionId);
    assert.equal(moved.ok, true);
    const ashley = world.enterHuman('Ashley.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    assert.ok(ashley.sessionId, 'Ashley entered');
    const seen = world.getObjectState(MUG_ID, 'HOME');
    assert.equal(seen.position, 'windowsill', 'Ashley sees the mug in its moved position');
  } finally {
    world.close();
  }
});

test('property 11: persist the resulting state across cold restart', () => {
  const dir = mkdtempSync(join(tmpdir(), 'rre-test-'));
  const dbPath = join(dir, 'test.db');
  let world = new RREWorld({ dbPath, worldspec, ellie });
  world.instantiateEllie();
  const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
  const moved = moveMug(world, noah.sessionId);
  assert.equal(moved.ok, true);
  const beforeCount = world.countExecutedEvents('HOME');
  world.close();
  world = new RREWorld({ dbPath, worldspec, ellie });
  try {
    const state = world.getObjectState(MUG_ID, 'HOME');
    assert.equal(state.position, 'windowsill', 'mug still moved after cold restart');
    assert.equal(world.countExecutedEvents('HOME'), beforeCount, 'event count unchanged across restart');
    const chain = world.verifyHashChain('HOME');
    assert.equal(chain.ok, true, 'hash chain verifies after restart');
  } finally {
    world.close();
  }
});

test('property 12: Ellie remembers an executed interaction', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    const moved = moveMug(world, noah.sessionId);
    assert.equal(moved.ok, true);
    assert.equal(world.ellieRemembersEvent(moved.eventId), true, 'Ellie remembers the mug move event');
    const memories = world.ellieRecall();
    assert.ok(memories.some((m) => m.event_id === moved.eventId), 'move appears in Ellie recall');
    assert.ok(memories.length >= 1, 'Ellie holds memories');
  } finally {
    world.close();
  }
});

test('property 13: provenance query', () => {
  const world = freshWorld();
  try {
    const provenance = world.getProvenance(MUG_ID);
    assert.equal(provenance.name, 'Mug');
    assert.equal(provenance.provenance, 'ESTABLISHED');
    assert.ok(provenance.sourceLocator.includes('100 statements st. 25'), 'source locator names the statement');
    assert.equal(provenance.currentPosition, 'desk');
    assert.equal(provenance.historyKind, 'recovered');
    assert.equal(world.getProvenance('obj-nonexistent'), null, 'unknown object returns null');
  } finally {
    world.close();
  }
});

test('property 14: source records unchanged', () => {
  const world = freshWorld();
  try {
    const before = world.snapshotSources();
    const claimsBefore = world.countClaims();
    world.instantiateEllie();
    const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    world.askEllie('What is your rank and field?', { askedBySessionId: noah.sessionId });
    const moved = moveMug(world, noah.sessionId);
    assert.equal(moved.ok, true);
    assert.equal(world.snapshotSources(), before, 'source records byte-identical after world activity');
    assert.equal(world.countClaims(), claimsBefore, 'no claims added or changed by world activity');
  } finally {
    world.close();
  }
});

test('property 15: executed events in a separate ledger', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
    const moved = moveMug(world, noah.sessionId);
    assert.equal(moved.ok, true);
    const separation = world.ledgerSeparation();
    assert.equal(separation.separateLedgers, true);
    assert.ok(separation.executedEvents >= 2, 'executed events recorded');
    assert.ok(separation.sources > 0 && separation.claims > 0, 'recovered ledger populated');
    const receipt = world.getEventReceipt(moved.eventId);
    assert.equal(receipt.historyKind, 'executed');
    assert.equal(receipt.actorId, 'Noah.Physical');
    assert.equal(receipt.branchId, 'HOME');
    assert.equal(receipt.whatChanged.to.position, 'windowsill');
    // The executed ledger is a different table from the recovered
    // ledger and from the vendored simulation ledger.
    const tables = world.db.prepare(
      "SELECT name FROM sqlite_master WHERE type = 'table' AND name IN ('executed_events','sources','claims','simulation_events') ORDER BY name",
    ).all().map((r) => r.name);
    assert.deepEqual(tables, ['claims', 'executed_events', 'simulation_events', 'sources']);
    const inRecovered = world.db.prepare(
      "SELECT COUNT(*) n FROM claims WHERE id = 'object_moved'",
    ).get().n;
    assert.equal(inRecovered, 0, 'executed events never appear as recovered claims');
  } finally {
    world.close();
  }
});
