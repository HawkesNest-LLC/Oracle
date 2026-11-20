import unittest,tempfile,os,json,subprocess,sys
from engine import *
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=os.path.join(self.tmp.name,'ledger.db');self.c=connect(self.path)
 def tearDown(self):self.c.close();self.tmp.cleanup()
 def source(self):append(self.c,'SOURCE','S1',{'locator':'synthetic://fixture'})
 def claim(self):self.source();append(self.c,'CLAIM','C1',{'text':'synthetic','source_id':'S1'})
 def test_empty(self):self.assertEqual(recover(self.c)['events'],[])
 def test_source(self):self.source();self.assertTrue(verify(self.c))
 def test_claim(self):self.claim();self.assertEqual(len(recover(self.c)['events']),2)
 def test_missing_source(self):
  with self.assertRaises(ValueError):append(self.c,'CLAIM','C1',{'text':'x','source_id':'NONE'})
 def test_duplicate_source(self):
  self.source()
  with self.assertRaises(ValueError):self.source()
 def test_duplicate_claim(self):
  self.claim()
  with self.assertRaises(ValueError):append(self.c,'CLAIM','C1',{'text':'x','source_id':'S1'})
 def test_correction(self):
  self.claim();append(self.c,'CORRECTION','C2',{'supersedes':'C1','reason':'new source'});self.assertEqual(len(recover(self.c)['events']),3)
 def test_correction_missing_target(self):
  with self.assertRaises(ValueError):append(self.c,'CORRECTION','C2',{'supersedes':'C1','reason':'x'})
 def test_canon(self):
  with self.assertRaises(ValueError):append(self.c,'CANON_PROMOTION','x',{})
 def test_approval(self):
  with self.assertRaises(ValueError):append(self.c,'APPROVAL','x',{})
 def test_actor(self):
  with self.assertRaises(PermissionError):append(self.c,'DECISION','D1',{'status':'APPROVED','actor':'Noah.Physical'})
 def test_proposal(self):append(self.c,'DECISION','D1',{'status':'PROPOSED'});self.assertTrue(verify(self.c))
 def test_identity_invalid(self):
  with self.assertRaises(ValueError):append(self.c,'IDENTITY','I1',{'scope':'unknown'})
 def test_identity_separation(self):
  append(self.c,'IDENTITY','I1',{'scope':'real'});append(self.c,'IDENTITY','I2',{'scope':'fiction'});self.assertNotEqual(recover(self.c)['events'][0]['payload']['scope'],recover(self.c)['events'][1]['payload']['scope'])
 def test_tamper(self):
  self.source();self.c.execute("UPDATE events SET payload='{}' WHERE seq=1");self.c.commit();self.assertFalse(verify(self.c))
 def test_tamper_blocks_append(self):
  self.source();self.c.execute("UPDATE events SET payload='{}' WHERE seq=1");self.c.commit()
  with self.assertRaises(ValueError):append(self.c,'SOURCE','S2',{'locator':'x'})
 def test_invalid_source(self):
  with self.assertRaises(ValueError):append(self.c,'SOURCE','S1',{})
 def test_restart(self):
  self.claim();self.c.close();self.c=connect(self.path);self.assertEqual(len(recover(self.c)['events']),2)
 def test_fresh_process(self):
  self.claim();self.c.close()
  p=subprocess.run([sys.executable,'-c',"import json,sys;from engine import connect,recover;print(json.dumps(recover(connect(sys.argv[1]))))",self.path],capture_output=True,text=True,cwd=os.path.dirname(__file__),check=True)
  self.assertEqual(len(json.loads(p.stdout)['events']),2);self.c=connect(self.path)
 def test_timestamp_order(self):
  append(self.c,'RECEIPT','R1',{'timestamp':'2026-11-14T10:00:00Z'})
  with self.assertRaises(ValueError):append(self.c,'RECEIPT','R2',{'timestamp':'2026-11-13T10:00:00Z'})
 def test_timestamp_newer(self):
  append(self.c,'RECEIPT','R1',{'timestamp':'2026-11-13T10:00:00Z'});append(self.c,'RECEIPT','R2',{'timestamp':'2026-11-14T10:00:00Z'});self.assertTrue(verify(self.c))
 def test_signature(self):
  key=b'synthetic-only';p={'id':'D1','nonce':'1'};sig=sign_fixture(key,p);self.assertTrue(verify_fixture(key,p,sig));self.assertFalse(verify_fixture(key,{'id':'D1','nonce':'2'},sig))
 def test_wrong_key(self):
  p={'id':'D1'};sig=sign_fixture(b'key-a',p);self.assertFalse(verify_fixture(b'key-b',p,sig))
if __name__=='__main__':unittest.main(verbosity=2)
