import unittest,tempfile,os,sqlite3
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
from authority_checkpoint05 import *
class Tests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=os.path.join(self.tmp.name,'db');self.c=connect(self.path)
  self.key=Ed25519PrivateKey.generate();enroll_synthetic_fixture(self.c,'fixture',self.key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw))
  self.p={'purpose':'candidate_attestation','event_id':'e1','key_id':'fixture','nonce':'fixture-nonce-0001'}
 def tearDown(self):self.c.close();self.tmp.cleanup()
 def sign(self,p=None):return self.key.sign(canonical(p or self.p))
 def test_valid(self):self.assertFalse(verify_candidate(self.c,'e1','fixture',self.p,self.sign())['canon_promoted'])
 def test_replay(self):
  verify_candidate(self.c,'e1','fixture',self.p,self.sign())
  with self.assertRaises(sqlite3.IntegrityError):verify_candidate(self.c,'e1','fixture',self.p,self.sign())
 def test_restart(self):
  verify_candidate(self.c,'e1','fixture',self.p,self.sign());self.c.close();self.c=connect(self.path)
  with self.assertRaises(sqlite3.IntegrityError):verify_candidate(self.c,'e1','fixture',self.p,self.sign())
 def test_tamper(self):
  p=dict(self.p,nonce='fixture-nonce-0002')
  with self.assertRaises(PermissionError):verify_candidate(self.c,'e1','fixture',p,self.sign())
 def test_wrong_signer(self):
  sig=Ed25519PrivateKey.generate().sign(canonical(self.p))
  with self.assertRaises(PermissionError):verify_candidate(self.c,'e1','fixture',self.p,sig)
 def test_canon(self):
  p=dict(self.p,purpose='canon_promotion')
  with self.assertRaises(PermissionError):verify_candidate(self.c,'e1','fixture',p,self.sign(p))
 def test_unknown_key(self):
  p=dict(self.p,key_id='unknown')
  with self.assertRaises(PermissionError):verify_candidate(self.c,'e1','unknown',p,self.sign(p))
 def test_binding(self):
  with self.assertRaises(ValueError):verify_candidate(self.c,'e2','fixture',self.p,self.sign())
 def test_short_nonce(self):
  p=dict(self.p,nonce='short')
  with self.assertRaises(ValueError):verify_candidate(self.c,'e1','fixture',p,self.sign(p))
 def test_new_event(self):
  verify_candidate(self.c,'e1','fixture',self.p,self.sign())
  p=dict(self.p,event_id='e2',nonce='fixture-nonce-0002')
  self.assertFalse(verify_candidate(self.c,'e2','fixture',p,self.sign(p))['canon_promoted'])
if __name__=='__main__':unittest.main(verbosity=2)
