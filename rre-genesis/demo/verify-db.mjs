// RRE Genesis v0.1 verification script.
// Opens the existing demo database file read-only in effect: it runs
// no writes of its own beyond the idempotent seeding the runtime does
// on open, and prints mug state, event counts, head hash, and the
// event receipt answering how the mug got here. Exits non-zero if the
// database file does not exist or the mug is not in its moved position.

import { readFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { RREWorld, MUG_ID } from '../src/world.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const dataRoot = join(here, '..', 'data');
const dbPath = join(here, '..', 'data', 'rre-genesis-v0.1.db');

if (!existsSync(dbPath)) {
  console.log(`Database file not found: ${dbPath}`);
  console.log('Run the demo first: node demo/scenario-27.mjs');
  process.exit(1);
}

const worldspec = JSON.parse(readFileSync(join(dataRoot, 'worldspec-deck-nine-v0.1.json'), 'utf8'));
const ellie = JSON.parse(readFileSync(join(dataRoot, 'ellie-genesis.json'), 'utf8'));
const world = new RREWorld({ dbPath, worldspec, ellie });

const state = world.getObjectState(MUG_ID, 'HOME');
const head = world.db.prepare(
  'SELECT event_hash FROM executed_events WHERE branch_id = ? ORDER BY event_id DESC LIMIT 1',
).get('HOME');
const receipt = world.getEventReceiptForObject(MUG_ID, 'HOME');
const chain = world.verifyHashChain('HOME');
const provenance = world.getProvenance(MUG_ID);

console.log('RRE GENESIS v0.1 DATABASE VERIFICATION');
console.log(`Database: ${dbPath}`);
console.log(`Mug position: ${state.position}`);
console.log(`Mug location: ${state.locationId}`);
console.log(`Mug history kind: ${state.historyKind}`);
console.log(`Mug provenance: ${provenance.provenance}`);
console.log(`Mug source locator: ${provenance.sourceLocator}`);
console.log(`Executed events on HOME: ${world.countExecutedEvents('HOME')}`);
console.log(`Head event hash on HOME: ${head ? head.event_hash : 'none'}`);
console.log(`Hash chain verifies: ${chain.ok} (checked ${chain.checked} events)`);
console.log(`Ellie memories held: ${world.ellieRecall().length}`);
console.log('How did the mug get here?');
console.log(`  What happened: ${receipt.summary}`);
console.log(`  Who did it: ${receipt.actorId} (${receipt.actorType})`);
console.log(`  Who witnessed it: ${receipt.witnesses.join(', ') || 'none recorded'}`);
console.log(`  When: ${receipt.occurredAt}`);
console.log(`  Which branch: ${receipt.branchId}`);
console.log(`  What changed: ${JSON.stringify(receipt.whatChanged)}`);
console.log(`  History kind: ${receipt.historyKind}`);
world.close();

if (state.position !== 'windowsill' || !chain.ok) {
  console.log('VERIFICATION FAILED');
  process.exit(1);
}
console.log('VERIFICATION PASSED');
