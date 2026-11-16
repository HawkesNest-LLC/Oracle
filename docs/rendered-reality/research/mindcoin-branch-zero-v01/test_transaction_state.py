import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from transaction_state import Journal

class JournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name) / 'journal.db'
        self.j = Journal(self.path)

    def test_create_and_idempotent_request(self):
        self.assertEqual(self.j.request('a','d'), 'REQUESTED')
        self.assertEqual(self.j.request('a','d'), 'REQUESTED')
        self.assertEqual(len(self.j.history('a')), 1)

    def test_conflicting_digest(self):
        self.j.request('a','d')
        with self.assertRaisesRegex(ValueError,'ACTION_ID_DIGEST_CONFLICT'):
            self.j.request('a','other')

    def test_success_path(self):
        self.j.request('a','d')
        for state in ('VERIFIED','RESERVED','EXECUTED'):
            self.j.transition('a',state,'synthetic observation')
        self.assertEqual(self.j.state('a'),'EXECUTED')
        self.assertEqual(len(self.j.history('a')),4)

    def test_failed_path(self):
        self.j.request('a','d')
        self.j.transition('a','FAILED','synthetic rejection')
        self.assertEqual(self.j.state('a'),'FAILED')

    def test_illegal_transition(self):
        self.j.request('a','d')
        with self.assertRaisesRegex(ValueError,'ILLEGAL_TRANSITION'):
            self.j.transition('a','EXECUTED','cannot skip')

    def test_recover_reserved(self):
        self.j.request('a','d')
        self.j.transition('a','VERIFIED','verified')
        self.j.transition('a','RESERVED','reserved')
        self.assertEqual(Journal(self.path).recover(),['a'])
        self.assertEqual(Journal(self.path).state('a'),'UNKNOWN_OUTCOME')
        self.assertEqual(Journal(self.path).recover(),[])

    def test_unknown_not_auto_success(self):
        self.j.request('a','d')
        self.j.transition('a','VERIFIED','verified')
        self.j.transition('a','RESERVED','reserved')
        self.j.recover()
        self.assertEqual(self.j.state('a'),'UNKNOWN_OUTCOME')
        with self.assertRaises(ValueError):
            self.j.transition('a','RESERVED','no automatic retry')

    def test_manual_resolution_requires_note(self):
        self.j.request('a','d')
        self.j.transition('a','VERIFIED','verified')
        self.j.transition('a','RESERVED','reserved')
        self.j.recover()
        with self.assertRaises(ValueError):
            self.j.transition('a','FAILED','')
        self.j.transition('a','FAILED','synthetic reconciliation evidence')
        self.assertEqual(self.j.state('a'),'FAILED')

    def test_no_action(self):
        with self.assertRaises(KeyError):
            self.j.transition('missing','VERIFIED','note')

    def test_concurrent_same_id(self):
        def submit(_):
            return Journal(self.path).request('a','d')
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            states=list(pool.map(submit,range(20)))
        self.assertEqual(states,['REQUESTED']*20)
        self.assertEqual(len(self.j.history('a')),1)

    def test_restart_persists_terminal(self):
        self.j.request('a','d')
        self.j.transition('a','FAILED','synthetic fail')
        self.assertEqual(Journal(self.path).state('a'),'FAILED')

    def test_recovery_only_reserved(self):
        self.j.request('a','d')
        self.j.request('b','d2')
        self.j.transition('b','VERIFIED','verified')
        self.assertEqual(self.j.recover(),[])
        self.assertEqual(self.j.state('b'),'VERIFIED')

if __name__ == '__main__':
    unittest.main()
