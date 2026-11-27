import unittest
from human_priority_gate import Gate
class Tests(unittest.TestCase):
 def setUp(self):
  self.g=Gate();self.g.source('s1',b'primary statement');self.g.source('s2',b'correction')
 def test_supported(self):
  self.g.record('x','real_world','supported','A','s1');self.assertEqual(self.g.recall('x','real_world')['status'],'SUPPORTED')
 def test_unknown(self):self.assertEqual(self.g.recall('x','real_world')['status'],'UNKNOWN')
 def test_receipt_required(self):
  with self.assertRaises(ValueError):self.g.record('x','real_world','supported','A')
 def test_domain_isolation(self):
  n=self.g.record('x','real_world','supported','A','s1')
  with self.assertRaises(ValueError):self.g.record('x','fictional','supported','B','s2',n)
 def test_correction(self):
  n=self.g.record('x','real_world','supported','A','s1');self.g.record('x','real_world','supported','B','s2',n)
  self.assertEqual(self.g.recall('x','real_world')['content'],'B')
  self.assertEqual(self.g.db.execute('SELECT COUNT(*) FROM events').fetchone()[0],2)
 def test_conflict(self):
  self.g.record('x','real_world','supported','A','s1');self.g.record('x','real_world','supported','B','s2')
  self.assertEqual(self.g.recall('x','real_world')['status'],'CONFLICT_QUARANTINED')
 def test_inference(self):
  self.g.record('x','fictional','inferred','maybe');self.assertEqual(self.g.recall('x','fictional')['status'],'UNKNOWN')
 def test_emergency(self):
  self.g.emergency(True,human_controlled=True);self.assertEqual(self.g.action('background'),'PAUSED');self.assertEqual(self.g.action('safety_critical'),'ALLOWED')
 def test_human_control(self):
  with self.assertRaises(PermissionError):self.g.emergency(True)
 def test_canon(self):
  with self.assertRaises(PermissionError):self.g.action('canon_promotion')
 def test_source_tamper(self):
  self.g.record('x','real_world','supported','A','s1');self.g.db.execute('UPDATE sources SET raw=? WHERE receipt_id=?',(b'tampered','s1'))
  self.assertEqual(self.g.recall('x','real_world')['status'],'UNKNOWN')
 def test_bad_status(self):
  with self.assertRaises(ValueError):self.g.record('x','real_world','verified_by_ai','A')
if __name__=='__main__':unittest.main(verbosity=2)
