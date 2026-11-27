// RRE Genesis v0.1 tests: branch isolation, the AI-cannot-mutate
// rule, append-only enforcement, and hash-chain integrity.

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

function enterNoah(world, branchId = 'HOME') {
  return world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID, branchId });
}

test('branch isolation: a SANDBOX move does not change HOME', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noahHome = enterNoah(world, 'HOME');
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk');
    const sandboxSession = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID, branchId: 'SANDBOX' });
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'SANDBOX',
      sessionId: sandboxSession.sessionId,
    });
    const moved = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(moved.ok, true, 'sandbox move executes on its own branch');
    assert.equal(world.getObjectState(MUG_ID, 'SANDBOX').position, 'windowsill', 'sandbox sees the moved mug');
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'HOME is untouched');
    assert.equal(world.countExecutedEvents('HOME'), 1, 'no executed event landed on HOME for the sandbox move');
    assert.ok(noahHome.sessionId, 'home session still valid');
  } finally {
    world.close();
  }
});

test('branch isolation: a keep it produces a reviewable merge proposal, not a silent merge', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const sandboxSession = world.enterHuman('Noah.Physical', { device: 'VR headset', locationId: ELLIE_LOCATION_ID, branchId: 'SANDBOX' });
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'SANDBOX',
      sessionId: sandboxSession.sessionId,
    });
    const moved = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(moved.ok, true);
    const merge = world.requestMerge({
      sourceBranchId: 'SANDBOX',
      targetBranchId: 'HOME',
      summary: 'Keep the sandbox mug move.',
      proposedBy: 'Noah.Physical',
      whatChanged: { object: MUG_ID, to: { position: 'windowsill' } },
    });
    assert.equal(merge.status, 'pending', 'merge proposal waits for review');
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'HOME unchanged by the proposal alone');
    assert.equal(world.listMergeProposals().length, 1, 'one reviewable proposal on record');
    const decision = world.decideMerge(merge.merge_proposal_id, { decision: 'approved', decidedBy: 'Noah.Physical', note: 'Approved for review only; application is future work.' });
    assert.equal(decision.appliedToHome, false, 'deciding a proposal does not silently apply it');
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'HOME still unchanged after approval record');
  } finally {
    world.close();
  }
});

test('AI cannot mutate state: a raw AI sentence is rejected and changes nothing', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    enterNoah(world);
    const before = world.getObjectState(MUG_ID, 'HOME').position;
    const result = world.applyAiSentence('Move the mug to the windowsill.');
    assert.equal(result.ok, false, 'raw sentence rejected');
    assert.match(result.error, /cannot mutate world state/);
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, before, 'state unchanged');
    assert.equal(world.countExecutedEvents('HOME'), 1, 'no event written for the sentence');
  } finally {
    world.close();
  }
});

test('AI cannot mutate state: a proposal without validation never executes', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = enterNoah(world);
    // A proposal on its own changes nothing until validated.
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'proposal alone changes nothing');
    // A raw string is not a valid action at all.
    assert.throws(
      () => world.proposeAction({
        proposerType: 'AI',
        proposerId: 'Merlin',
        action: 'Move the mug to the windowsill.',
        targetObjectId: MUG_ID,
        branchId: 'HOME',
      }),
      /structured objects/,
      'string action rejected at proposal time',
    );
    // An AI proposer holds no execution permission.
    const aiProposal = world.proposeAction({
      proposerType: 'AI',
      proposerId: 'Merlin',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    const outcome = world.validateAndExecute(aiProposal.proposalId, { decidedBy: 'test' });
    assert.equal(outcome.ok, false, 'AI-proposed execution rejected');
    assert.match(outcome.reason, /do not hold execution permission/);
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'state unchanged');
    // There is no direct mutation method to call.
    assert.equal(typeof world.directSetState, 'undefined');
    assert.equal(typeof world.executeWithoutValidation, 'undefined');
    assert.equal(typeof world.mutateState, 'undefined');
  } finally {
    world.close();
  }
});

test('AI cannot mutate state: a proposal from an actor with no active session is rejected', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = enterNoah(world);
    world.exitHuman(noah.sessionId);
    assert.equal(world.isSessionActive(noah.sessionId), false);
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    const outcome = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(outcome.ok, false, 'ended session cannot execute');
    assert.match(outcome.reason, /no active session/);
    assert.equal(world.getObjectState(MUG_ID, 'HOME').position, 'desk', 'state unchanged');
    const outcomes = world.db.prepare(
      "SELECT COUNT(*) n FROM action_proposal_outcomes WHERE decision = 'rejected'",
    ).get().n;
    assert.equal(outcomes, 1, 'rejection is on the record');
  } finally {
    world.close();
  }
});

test('append-only enforcement: UPDATE and DELETE on ledger tables are rejected', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = enterNoah(world);
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    const moved = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(moved.ok, true);
    const targets = [
      ['executed_events', `event_id = ${moved.eventId}`, 'summary = summary'],
      ['world_state', `state_id = ${world.getObjectState(MUG_ID, 'HOME').stateId}`, 'state = state'],
      ['action_proposals', `proposal_id = ${proposal.proposalId}`, 'action = action'],
      ['human_sessions', `session_id = '${noah.sessionId}'`, 'avatar = avatar'],
      ['world_objects', `object_id = '${MUG_ID}'`, 'name = name'],
      ['assertions', 'id = 1', 'confidence = confidence'],
      ['claims', "id = 'bk-02'", 'statement = statement'],
      ['character_memories', 'memory_id = 1', 'summary = summary'],
    ];
    for (const [table, where, setClause] of targets) {
      assert.throws(
        () => world.db.exec(`UPDATE ${table} SET ${setClause} WHERE ${where}`),
        /append-only/,
        `UPDATE on ${table} is rejected`,
      );
      assert.throws(
        () => world.db.exec(`DELETE FROM ${table} WHERE ${where}`),
        /append-only/,
        `DELETE on ${table} is rejected`,
      );
    }
  } finally {
    world.close();
  }
});

test('hash-chain integrity: verification passes on a clean ledger', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = enterNoah(world);
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    const moved = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(moved.ok, true);
    const chain = world.verifyHashChain('HOME');
    assert.equal(chain.ok, true);
    assert.ok(chain.checked >= 2, 'at least the session start and the move were checked');
    assert.deepEqual(chain.broken, []);
  } finally {
    world.close();
  }
});

test('hash-chain integrity: tampering with an event breaks verification', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    const noah = enterNoah(world);
    const proposal = world.proposeAction({
      proposerType: 'human',
      proposerId: 'Noah.Physical',
      action: { type: 'move_object', toLocationId: ELLIE_LOCATION_ID, toPosition: 'windowsill' },
      targetObjectId: MUG_ID,
      branchId: 'HOME',
      sessionId: noah.sessionId,
    });
    const moved = world.validateAndExecute(proposal.proposalId, { decidedBy: 'test' });
    assert.equal(moved.ok, true);
    assert.equal(world.verifyHashChain('HOME').ok, true, 'chain verifies before tampering');
    // Tamper: drop the append-only trigger (as a privileged operator
    // could), edit the receipt, then verify. The hash chain must
    // detect the edit.
    world.db.exec('DROP TRIGGER executed_events_no_update');
    world.db.exec(`UPDATE executed_events SET summary = 'Tampered summary.' WHERE event_id = ${moved.eventId}`);
    const chain = world.verifyHashChain('HOME');
    assert.equal(chain.ok, false, 'chain fails after tampering');
    assert.ok(chain.broken.some((b) => b.eventId === moved.eventId), 'tampered event is named');
    assert.ok(chain.broken.some((b) => b.reason.includes('recomputed hash')), 'failure reason names the hash mismatch');
  } finally {
    world.close();
  }
});

test('hash-chain integrity: an event with a wrong prev hash is refused at insert', () => {
  const world = freshWorld();
  try {
    world.instantiateEllie();
    enterNoah(world);
    assert.throws(
      () => world.db.prepare(
        `INSERT INTO executed_events(branch_id, event_type, actor_type, actor_id, witnesses, occurred_at, summary, what_changed, prev_event_hash, event_hash)
         VALUES('HOME','object_moved','human','Noah.Physical','[]','2026-11-06T00:00:00.000Z','Forged event.','{}','not-the-real-prev-hash','forged-hash')`,
      ).run(),
      /hash chain broken/,
      'forged prev hash refused by the trigger',
    );
  } finally {
    world.close();
  }
});
