import unittest,tempfile,os,sqlite3
from engine import *
class EngineTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.path=os.path.join(self.t.name,'events.db');self.c=connect(self.path)
 def tearDown(self):self.c.close();self.t.cleanup()
 def source(self):append(self.c,'SOURCE','S1',{'locator':'https://example.invalid/source','hash':'fixture'})
 def claim(self):self.source();append(self.c,'CLAIM','C1',{'text':'synthetic fact','source_id':'S1'})
 def test_restart(self):
  self.claim();self.c.close();self.c=connect(self.path);self.assertTrue(verify(self.c));self.assertEqual(len(recover(self.c)['events']),2)
 def test_correction_history(self):
  self.claim();append(self.c,'CORRECTION','C2',{'supersedes':'C1','reason':'synthetic correction'});self.assertEqual(len(recover(self.c)['events']),3)
 def test_missing_source(self):
  with self.assertRaises(ValueError):append(self.c,'CLAIM','C1',{'text':'x','source_id':'MISSING'})
 def test_forged_approval(self):
  with self.assertRaises(ValueError):append(self.c,'APPROVAL','X',{'actor':'Noah.Physical'})
 def test_canon_mutation(self):
  with self.assertRaises(ValueError):append(self.c,'CANON_PROMOTION','X',{})
 def test_actor_string(self):
  with self.assertRaises(PermissionError):append(self.c,'DECISION','D',{'status':'APPROVED','actor':'Noah.Physical'})
 def test_tamper(self):
  self.claim();self.c.execute("UPDATE events SET payload='{}' WHERE seq=1");self.c.commit();self.assertFalse(verify(self.c))
 def test_replay_not_deduped(self):
  self.source();append(self.c,'SOURCE','S1',{'locator':'https://example.invalid/source','hash':'fixture'});self.assertEqual(len(recover(self.c)['events']),2)
 def test_out_of_order_not_rejected(self):
  self.source();append(self.c,'RECEIPT','R1',{'timestamp':'1990-01-01'});self.assertTrue(verify(self.c))
 def test_unknown(self):self.assertEqual(recover(self.c)['events'],[])
 def test_integrity_after_invalid(self):
  with self.assertRaises(ValueError):append(self.c,'SOURCE','S1',{});self.assertTrue(verify(self.c))
 def test_identity(self):append(self.c,'IDENTITY','I1',{'scope':'fiction'});self.assertEqual(recover(self.c)['events'][0]['kind'],'IDENTITY')
if __name__=='__main__':unittest.main(verbosity=2)
