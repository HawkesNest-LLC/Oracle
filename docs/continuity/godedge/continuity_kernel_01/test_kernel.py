import unittest
from kernel import connect,append,verify,metrics
class KernelTests(unittest.TestCase):
 def setUp(self):self.c=connect(':memory:')
 def tearDown(self):self.c.close()
 def test_hash_chain(self):
  append(self.c,'CLAIM','x',{'attribution':'Noah.Physical'});self.assertTrue(verify(self.c))
  self.c.execute("UPDATE events SET payload='{}' WHERE id=1");self.assertFalse(verify(self.c))
 def test_human_gate(self):
  with self.assertRaises(PermissionError):append(self.c,'APPROVAL','x',{'actor':'AI'})
 def test_metrics(self):
  append(self.c,'SOURCE','x',{'locator':'local:sample','verified':False})
  append(self.c,'CLAIM','x',{'attribution':'Noah.Physical','status':'CANDIDATE'})
  append(self.c,'CORRECTION','x',{'previous':'a','new':'b'})
  append(self.c,'TEST','x',{'correction_recalled':True})
  m=metrics(self.c,['x']);self.assertEqual((m['RF'],m['CPR'],m['PID']),(1,1,0))
if __name__=='__main__':unittest.main()
