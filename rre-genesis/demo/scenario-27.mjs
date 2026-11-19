// RRE Genesis v0.1 demo: directive section 27 test scenario.
// Runs end to end, prints a readable transcript plus a verification
// summary, and exits non-zero if any step fails. Prints PASS/FAIL per
// step. No em dashes are used in this file.
//
// The script closes the database, reopens it from the same file, and
// continues. That is the cold restart inside this run.

import { readFileSync, existsSync, rmSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { RREWorld, MUG_ID, ELLIE_LOCATION_ID } from '../src/world.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const dataRoot = join(here, '..', 'data');
const dbPath = join(here, '..', 'data', 'rre-genesis-v0.1.db');
const worldspec = JSON.parse(readFileSync(join(dataRoot, 'worldspec-deck-nine-v0.1.json'), 'utf8'));
const ellie = JSON.parse(readFileSync(join(dataRoot, 'ellie-genesis.json'), 'utf8'));

const results = [];
function check(name, passed, detail) {
  results.push({ name, passed: Boolean(passed) });
  console.log(`${passed ? 'PASS' : 'FAIL'}  ${name}${detail ? '  ' + detail : ''}`);
  return Boolean(passed);
}

function headHash(world, branchId = 'HOME') {
  const row = world.db.prepare(
    'SELECT event_hash FROM executed_events WHERE branch_id = ? ORDER BY event_id DESC LIMIT 1',
  ).get(branchId);
  return row ? row.event_hash : null;
}

console.log('RRE GENESIS v0.1  SECTION 27 TEST SCENARIO');
console.log('==========================================');
console.log('');

// Start from a clean database file so the run is reproducible.
for (const suffix of ['', '-wal', '-shm']) {
  const file = dbPath + suffix;
  if (existsSync(file)) rmSync(file);
}
console.log(`Database: ${dbPath} (fresh file for this run)`);
console.log('');

let world = new RREWorld({ dbPath, worldspec, ellie });
console.log(`World loaded: ${world.countLocationsInCell()} locations in cell, ${world.countObjects()} objects, ${world.countSources()} sources, ${world.countClaims()} claims.`);
console.log('');

const ellieRuntime = world.instantiateEllie();
check('Ellie runtime instantiated with bounded knowledge', ellieRuntime.knowledge_scope === 'ellie-genesis-v0.1', `scope=${ellieRuntime.knowledge_scope}`);

// Step 1: Noah enters Ellie's quarters. Ellie is present.
const noah = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
const ellieWhere = world.whereIsEllie();
check(
  'Noah.Physical enters Ellie quarters; Ellie is present',
  ellieWhere.present && ellieWhere.locationId === ELLIE_LOCATION_ID,
  `Ellie is in ${ellieWhere.locationName}`,
);
console.log(`  Noah session: ${noah.sessionId}. Ellie location: ${ellieWhere.locationName}.`);
console.log('');

// Step 2: established question.
const established = world.askEllie('What is your rank and field?', { askedBySessionId: noah.sessionId });
console.log(`Noah: What is your rank and field?`);
console.log(`Ellie: ${established.answer}`);
check(
  'Ellie answers an established question from bounded knowledge with its source',
  established.status === 'ESTABLISHED' && established.knowledgeId === 'bk-02' && Boolean(established.sourceLocator),
  `knowledge=${established.knowledgeId}, source=${established.sourceLocator}`,
);
console.log('');

// Step 3: unresolved question.
const unresolved = world.askEllie('What is Sparrow?', { askedBySessionId: noah.sessionId });
console.log(`Noah: What is Sparrow?`);
console.log(`Ellie: ${unresolved.answer}`);
check(
  'Ellie says she does not know for an unresolved question',
  unresolved.status === 'UNKNOWN' && unresolved.answer.startsWith("I don't know"),
  `knowledge=${unresolved.knowledgeId}, status=${unresolved.status}`,
);
console.log('');

// Step 4: Noah moves the mug through a validated action proposal.
const mugBefore = world.getObjectState(MUG_ID, 'HOME');
console.log(`Mug before move: position=${mugBefore.position}, location=${mugBefore.locationId}.`);
const proposal = world.proposeAction({
  proposerType: 'human',
  proposerId: 'Noah.Physical',
  action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
  targetObjectId: MUG_ID,
  branchId: 'HOME',
  sessionId: noah.sessionId,
});
const move = world.validateAndExecute(proposal.proposalId, { decidedBy: 'RREWorld validation' });
console.log(`Move proposal ${proposal.proposalId}: ${move.ok ? 'validated and executed' : 'rejected: ' + move.reason}`);
const mugAfterMove = world.getObjectState(MUG_ID, 'HOME');
check(
  'Noah moves the mug through a validated action proposal',
  move.ok && mugAfterMove.position === 'windowsill',
  `event=${move.eventId}, position=${mugAfterMove.position}`,
);
console.log('');

// Step 5: Ashley joins the same world instance and sees the moved mug.
const ashley = world.enterHuman('Ashley.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
const mugSeenByAshley = world.getObjectState(MUG_ID, 'HOME');
check(
  'Ashley.Physical joins the same world instance and sees the mug moved',
  mugSeenByAshley.position === 'windowsill',
  `Ashley session=${ashley.sessionId}, mug position=${mugSeenByAshley.position}`,
);
console.log('');

// Step 6: Noah leaves.
world.exitHuman(noah.sessionId);
check('Noah.Physical leaves; the world continues', world.isSessionActive(ashley.sessionId), 'Ashley session still active');
console.log('');

// Step 7: cold restart. Record state before shutdown, close, reopen.
const beforeShutdown = {
  mugPosition: world.getObjectState(MUG_ID, 'HOME').position,
  eventCount: world.countExecutedEvents('HOME'),
  headHash: headHash(world, 'HOME'),
};
console.log('STATE BEFORE SHUTDOWN');
console.log(`  Mug position: ${beforeShutdown.mugPosition}`);
console.log(`  Executed events on HOME: ${beforeShutdown.eventCount}`);
console.log(`  Head event hash on HOME: ${beforeShutdown.headHash}`);
world.close();
console.log('Processes stopped. Database closed.');
world = new RREWorld({ dbPath, worldspec, ellie });
console.log('Processes restarted. Database reopened from the same file.');
console.log('');
const afterRestart = {
  mugPosition: world.getObjectState(MUG_ID, 'HOME').position,
  eventCount: world.countExecutedEvents('HOME'),
  headHash: headHash(world, 'HOME'),
};
console.log('STATE AFTER RESTART');
console.log(`  Mug position: ${afterRestart.mugPosition}`);
console.log(`  Executed events on HOME: ${afterRestart.eventCount}`);
console.log(`  Head event hash on HOME: ${afterRestart.headHash}`);
check(
  'Mug remains moved after cold restart',
  afterRestart.mugPosition === 'windowsill'
    && afterRestart.eventCount === beforeShutdown.eventCount
    && afterRestart.headHash === beforeShutdown.headHash,
  `position=${afterRestart.mugPosition}`,
);
console.log('');

// Step 8: Noah returns.
const noahReturn = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID });
const mugOnReturn = world.getObjectState(MUG_ID, 'HOME');
check(
  'Noah returns after restart and the mug is still moved',
  mugOnReturn.position === 'windowsill',
  `position=${mugOnReturn.position}`,
);
console.log('');

// Step 9: Ellie remembers the executed encounter.
const memories = world.ellieRecall();
const remembersMove = world.ellieRemembersEvent(move.eventId);
const moveMemory = memories.find((m) => m.event_id === move.eventId);
check(
  'Ellie remembers the executed encounter she witnessed',
  remembersMove && Boolean(moveMemory),
  `memories held=${memories.length}, move event remembered=${remembersMove}`,
);
if (moveMemory) console.log(`  Ellie memory: ${moveMemory.summary}`);
console.log('');

// Step 10: the system answers how the mug got here.
const receipt = world.getEventReceiptForObject(MUG_ID, 'HOME');
console.log('HOW DID THE MUG GET HERE?');
console.log(`  What happened: ${receipt.summary}`);
console.log(`  Who did it: ${receipt.actorId} (${receipt.actorType})`);
console.log(`  Who witnessed it: ${receipt.witnesses.join(', ') || 'none recorded'}`);
console.log(`  When: ${receipt.occurredAt}`);
console.log(`  Which branch: ${receipt.branchId}`);
console.log(`  What changed: ${JSON.stringify(receipt.whatChanged)}`);
console.log(`  History kind: ${receipt.historyKind} (executed history, not authored history)`);
check(
  'Event lookup answers what, who, witnesses, when, branch, what changed, and history kind',
  receipt.historyKind === 'executed'
    && receipt.actorId === 'Noah.Physical'
    && receipt.branchId === 'HOME'
    && receipt.whatChanged.to.position === 'windowsill'
    && receipt.whatChanged.from.position === 'desk'
    && receipt.witnesses.includes('run-ellie-hawkes'),
  `event=${receipt.eventId}`,
);
console.log('');

// Provenance and ledger checks.
const provenance = world.getProvenance(MUG_ID);
console.log(`Provenance of the mug: ${provenance.provenance}, source: ${provenance.sourceLocator}`);
const chain = world.verifyHashChain('HOME');
check('Executed event hash chain verifies', chain.ok, `checked=${chain.checked} events`);
const separation = world.ledgerSeparation();
console.log(`Ledgers: sources=${separation.sources}, claims=${separation.claims}, executed events=${separation.executedEvents}, simulation events=${separation.simulationEvents}.`);
console.log('');

world.exitHuman(noahReturn.sessionId);
world.exitHuman(ashley.sessionId);
world.close();

const passed = results.filter((r) => r.passed).length;
const failed = results.filter((r) => !r.passed).length;
console.log('VERIFICATION SUMMARY');
console.log(`  Steps passed: ${passed}`);
console.log(`  Steps failed: ${failed}`);
console.log(`  Result: ${failed === 0 ? 'ALL STEPS PASS' : 'FAILURES PRESENT'}`);
process.exit(failed === 0 ? 0 : 1);
