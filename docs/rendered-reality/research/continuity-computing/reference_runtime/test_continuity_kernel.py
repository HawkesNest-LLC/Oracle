import sqlite3
import tempfile
import unittest
from pathlib import Path
from continuity_kernel import ContinuityKernel


class ContinuityKernelTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.kernel = ContinuityKernel(Path(self.tmp.name) / 'continuity.sqlite')
        self.kernel.add_source('src1', 'creator-note', 'Noah commands Avalon', access='public', authorship='Noah.Physical')
        self.kernel.add_fact('fact1', 'Noah commands Avalon', 'src1', year=2397)

    def tearDown(self):
        self.kernel.close()
        self.tmp.cleanup()

    def approve(self):
        self.kernel.rule('ruling1', 'fact1', 'approve', 'src1', actor_claim='Noah.Physical', reason='creator adoption')

    def test_candidate_not_canon_until_approved(self):
        self.kernel.create_world('replay', 'home-2397', 2397, mode='canon_replay')
        self.assertEqual(self.kernel.scene_facts('replay'), [])
        self.approve()
        self.assertEqual(len(self.kernel.scene_facts('replay')), 1)
        with self.assertRaises(PermissionError):
            self.kernel.append_event('e1', 'replay', 'Reg', 'change_history', {})

    def test_character_cannot_know_without_acquisition(self):
        self.approve()
        self.kernel.create_world('world', 'home-2397', 2397)
        self.assertEqual(self.kernel.character_knowledge('world', 'Ellie'), [])
        self.kernel.append_event('e1', 'world', 'Ellie', 'read_source', {'source_id': 'src1'}, witness='observed')
        self.kernel.teach('world', 'Ellie', 'fact1', 'e1')
        self.assertEqual(len(self.kernel.character_knowledge('world', 'Ellie')), 1)

    def test_no_knowledge_teleportation_through_unrelated_event(self):
        self.approve()
        self.kernel.create_world('w2', 'home-2397', 2397)
        self.kernel.append_event('unrelated', 'w2', 'Reg', 'inspect_console', {})
        with self.assertRaises(ValueError):
            self.kernel.teach('w2', 'Ellie', 'fact1', 'unrelated')
        self.kernel.append_event('wrong_source', 'w2', 'Ellie', 'read_source', {'source_id': 'different'})
        with self.assertRaises(ValueError):
            self.kernel.teach('w2', 'Ellie', 'fact1', 'wrong_source')

    def test_branch_and_era_isolation(self):
        self.approve()
        self.kernel.create_world('past', 'home-2397', 2371)
        self.kernel.create_world('other', 'alternate-branch', 2397)
        self.assertEqual(self.kernel.scene_facts('past'), [])
        self.assertEqual(self.kernel.scene_facts('other'), [])
        self.kernel.append_event('e1', 'past', 'Reg', 'observe', {}, witness='reported')
        with self.assertRaises(ValueError):
            self.kernel.teach('other', 'Reg', 'fact1', 'e1')

    def test_event_receipts_detect_mutation(self):
        self.kernel.create_world('w', 'home-2397', 2397)
        self.kernel.append_event('e1', 'w', 'Reg', 'observe', {'clock': 1})
        self.kernel.append_event('e2', 'w', 'Ellie', 'inspect', {'clock': 2})
        self.assertTrue(self.kernel.verify_events('w'))
        with self.assertRaises(sqlite3.DatabaseError):
            self.kernel.db.execute("UPDATE events SET action='forged' WHERE event_id='e1'")
        # A privileged attacker can remove local triggers, so the receipt hash is checked as well.
        self.kernel.db.execute('DROP TRIGGER no_event_update')
        self.kernel.db.execute("UPDATE events SET action='forged' WHERE event_id='e1'")
        self.assertFalse(self.kernel.verify_events('w'))

    def test_persistence_across_restart(self):
        self.approve()
        self.kernel.create_world('persist', 'home-2397', 2397)
        self.kernel.append_event('e1', 'persist', 'Reg', 'observe', {'value': 42})
        path = self.kernel.path
        self.kernel.close()
        self.kernel = ContinuityKernel(path)
        self.assertEqual(self.kernel.fact_status('fact1'), 'canon')
        self.assertTrue(self.kernel.verify_events('persist'))
        self.assertEqual(self.kernel.world_info('persist')['story_year'], 2397)

    def test_private_source_not_in_public_render(self):
        self.kernel.add_source('private1', 'protected-manuscript', 'Private source detail', access='private')
        self.kernel.add_fact('secret', 'Private source detail', 'private1', year=2397)
        self.kernel.rule('rsecret', 'secret', 'approve', 'private1', actor_claim='Noah.Physical', reason='private source adoption demo')
        self.kernel.create_world('wprivate', 'home-2397', 2397)
        self.assertNotIn('secret', [x['fact_id'] for x in self.kernel.render_packet('wprivate')['canon_facts']])
        self.assertIn('secret', [x['fact_id'] for x in self.kernel.scene_facts('wprivate', include_private=True)])

    def test_rulings_are_append_only_and_role_claim_is_not_identity(self):
        with self.assertRaises(PermissionError):
            self.kernel.rule('bad', 'fact1', 'approve', 'src1', actor_claim='Reg', reason='model output')
        self.approve()
        with self.assertRaises(sqlite3.DatabaseError):
            self.kernel.db.execute("UPDATE rulings SET decision='retract'")


if __name__ == '__main__':
    unittest.main()