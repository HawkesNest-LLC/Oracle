import unittest,tempfile,os
from candidate_ledger import connect,append,verify,lookup
class Tests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.p=os.path.join(self.t.name,'db');self.c=connect(self.p)
 def tearDown(self):self.c.close();self.t.cleanup()
 def source(self):append(self.c,'SOURCE','x',{'locator':'local:x'})
 def claim(self):append(self.c,'CLAIM','x',{'text':'candidate'})
 def test_unknown(self):self.assertEqual(lookup(self.c,'x')['status'],'UNKNOWN')
 def test_source_only_unknown(self):self.source();self.assertEqual(lookup(self.c,'x')['status'],'UNKNOWN')
 def test_candidate(self):self.source();self.claim();self.assertFalse(lookup(self.c,'x')['loadable'])
 def test_no_approval(self):
  with self.assertRaises(ValueError):append(self.c,'APPROVAL','x',{'actor':'Noah.Physical'})
 def test_no_promotion(self):
  with self.assertRaises(ValueError):append(self.c,'CANON_PROMOTION','x',{})
 def test_retraction(self):self.source();self.claim();append(self.c,'RETRACTION','x',{});self.assertEqual(lookup(self.c,'x')['status'],'RETRACTED_CANDIDATE')
 def test_restart(self):self.source();self.claim();self.c.close();self.c=connect(self.p);self.assertTrue(verify(self.c));self.assertEqual(lookup(self.c,'x')['status'],'CANDIDATE')
 def test_tamper(self):
  self.source();self.c.execute("UPDATE events SET payload='{}' WHERE id=1");self.c.commit();self.assertFalse(verify(self.c))
  with self.assertRaises(ValueError):self.claim()
 def test_invalid_source(self):
  with self.assertRaises(ValueError):append(self.c,'SOURCE','x',{})
 def test_correction(self):self.source();self.claim();append(self.c,'CORRECTION','x',{});self.assertTrue(lookup(self.c,'x')['has_correction'])
 def test_chain(self):
  for i in range(10):append(self.c,'SOURCE',str(i),{'locator':'local:'+str(i)})
  self.assertTrue(verify(self.c))
 def test_invalid_claim(self):
  with self.assertRaises(ValueError):append(self.c,'CLAIM','x',{})
if __name__=='__main__':unittest.main()
