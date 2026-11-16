import concurrent.futures, multiprocessing, tempfile, unittest
from pathlib import Path
from receipt_journal_v07 import ReceiptJournal, digest

def worker(path):
    return ReceiptJournal(path).request('shared','d')

class ReceiptJournalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'journal.db'
        self.j=ReceiptJournal(self.path)
        self.j.request('a','d')
    def reserve(self):
        self.j.advance('a','VERIFIED','synthetic review')
        self.j.advance('a','RESERVED','synthetic reservation')
    def receipt(self,outcome='EXECUTED',**kw):
        return {'action_id':'a','action_digest':'d','outcome':outcome,'evidence_ref':'synthetic:test:001',**kw}
    def test_receipt_required_for_execution(self):
        self.reserve()
        with self.assertRaisesRegex(ValueError,'RECEIPT_REQUIRED'): self.j.advance('a','EXECUTED','unsubstantiated')
        self.assertEqual(self.j.state('a'),'RESERVED')
    def test_matching_receipt_allows_execution(self):
        self.reserve()
        self.assertEqual(self.j.advance('a','EXECUTED','fixture observed',self.receipt()),'EXECUTED')
        self.assertEqual(self.j.history('a')[-1][2],digest(self.receipt()))
    def test_wrong_action_receipt_rejected(self):
        self.reserve()
        with self.assertRaises(ValueError): self.j.advance('a','EXECUTED','wrong',self.receipt(action_id='other'))
    def test_wrong_digest_rejected(self):
        self.reserve()
        with self.assertRaises(ValueError): self.j.advance('a','EXECUTED','wrong',self.receipt(action_digest='wrong'))
    def test_wrong_outcome_rejected(self):
        self.reserve()
        with self.assertRaises(ValueError): self.j.advance('a','EXECUTED','wrong',self.receipt('FAILED'))
    def test_recover_preserves_unknown(self):
        self.reserve()
        self.assertEqual(ReceiptJournal(self.path).recover(),['a'])
        self.assertEqual(ReceiptJournal(self.path).state('a'),'UNKNOWN_OUTCOME')
        self.assertEqual(self.j.recover(),[])
    def test_unknown_cannot_be_retried(self):
        self.reserve();self.j.recover()
        with self.assertRaises(ValueError): self.j.advance('a','RESERVED','unsafe retry')
    def test_unknown_can_resolve_with_receipt(self):
        self.reserve();self.j.recover()
        self.j.advance('a','FAILED','fixture evidence',self.receipt('FAILED'))
        self.assertEqual(self.j.state('a'),'FAILED')
    def test_missing_evidence_ref(self):
        self.reserve()
        with self.assertRaises(ValueError): self.j.advance('a','EXECUTED','no evidence',self.receipt(evidence_ref=''))
    def test_restart_terminal_persists(self):
        self.reserve();self.j.advance('a','EXECUTED','fixture',self.receipt())
        self.assertEqual(ReceiptJournal(self.path).state('a'),'EXECUTED')
    def test_idempotent_request(self):
        self.assertEqual(self.j.request('a','d'),'REQUESTED')
        self.assertEqual(len(self.j.history('a')),1)
    def test_conflicting_request(self):
        with self.assertRaises(ValueError): self.j.request('a','different')
    def test_multiprocess_same_request(self):
        with concurrent.futures.ProcessPoolExecutor(max_workers=4,mp_context=multiprocessing.get_context('spawn')) as pool:
            results=list(pool.map(worker,[str(self.path)]*12))
        self.assertEqual(results,['REQUESTED']*12)
        self.assertEqual(len(self.j.history('shared')),1)
    def test_crash_boundary_before_reservation(self):
        self.j.advance('a','VERIFIED','verified')
        self.assertEqual(ReceiptJournal(self.path).recover(),[])
        self.assertEqual(self.j.state('a'),'VERIFIED')
    def test_crash_boundary_after_reservation(self):
        self.reserve();ReceiptJournal(self.path).recover()
        self.assertEqual(self.j.state('a'),'UNKNOWN_OUTCOME')
if __name__=='__main__': unittest.main()
