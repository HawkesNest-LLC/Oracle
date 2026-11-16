import base64, os, tempfile, unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from phase4_governance import GovernanceStore, canonical, digest
NOW=1800000000
def raw(k):return k.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
def sig(k,domain,p):return base64.b64encode(k.sign(domain+canonical(p))).decode()
class TestGovernance(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.path=os.path.join(self.tmp.name,'db.sqlite')
  self.root=Ed25519PrivateKey.generate();self.user=Ed25519PrivateKey.generate()
  self.store=GovernanceStore(self.path,raw(self.root),clock=lambda:NOW)
  self.assertTrue(self.manage('ENROLL','a',base64.b64encode(raw(self.user)).decode()))
 def tearDown(self):self.store.close();self.tmp.cleanup()
 def manage(self,op,key,pub=None,signer=None,event=None):
  p={'event_id':event or op+key,'operation':op,'key_id':key,'public_key':pub,'issued_at':NOW}
  return self.store.manage_key(p,sig(signer or self.root,b'EXOCORTEX-KEY-MGMT-V1\0',p))
 def receipt(self,**kwargs):
  p={'version':1,'key_id':'a','actor':'Noah.Physical','action':'PROMOTE_TO_CANON','scope':'candidate/test','object_sha256':digest(b'candidate'),'issued_at':NOW-1,'expires_at':NOW+60,'nonce':'fixture-nonce-00000001'}
  p.update(kwargs);return {'payload':p,'signature':sig(self.user,b'EXOCORTEX-APPROVAL-V1\0',p)}
 def approve(self,r=None,scope='candidate/test'):
  return self.store.approve(r or self.receipt(),'PROMOTE_TO_CANON',scope,digest(b'candidate'))
 def test_signed_approval(self):self.assertIsNotNone(self.approve())
 def test_replay(self):
  r=self.receipt();self.assertIsNotNone(self.approve(r));self.assertIsNone(self.approve(r))
 def test_restart_replay(self):
  r=self.receipt();self.assertIsNotNone(self.approve(r));self.store.close()
  self.store=GovernanceStore(self.path,raw(self.root),clock=lambda:NOW);self.assertIsNone(self.approve(r))
 def test_forged_enrollment(self):
  fake=Ed25519PrivateKey.generate()
  self.assertFalse(self.manage('ENROLL','b',base64.b64encode(raw(fake)).decode(),signer=fake))
 def test_revocation(self):
  self.assertTrue(self.manage('REVOKE','a'));self.assertIsNone(self.approve())
 def test_revocation_restart(self):
  self.assertTrue(self.manage('REVOKE','a'));self.store.close()
  self.store=GovernanceStore(self.path,raw(self.root),clock=lambda:NOW);self.assertIsNone(self.approve())
 def test_rotation(self):
  self.assertTrue(self.manage('REVOKE','a'))
  new=Ed25519PrivateKey.generate()
  self.assertTrue(self.manage('ENROLL','b',base64.b64encode(raw(new)).decode()))
  p=self.receipt(key_id='b',nonce='fixture-nonce-00000002')['payload']
  r={'payload':p,'signature':sig(new,b'EXOCORTEX-APPROVAL-V1\0',p)}
  self.assertIsNotNone(self.approve(r))
 def test_wrong_scope(self):self.assertIsNone(self.approve(scope='wrong'))
 def test_modified_receipt(self):
  r=self.receipt();r['payload']['scope']='wrong';self.assertIsNone(self.approve(r))
 def test_execution_record_once(self):
  aid=self.approve();self.assertTrue(self.store.record_execution(aid,digest(b'output'),'SUCCEEDED'))
  self.assertFalse(self.store.record_execution(aid,digest(b'output'),'SUCCEEDED'))
 def test_execution_after_revocation(self):
  aid=self.approve();self.assertTrue(self.manage('REVOKE','a'))
  self.assertFalse(self.store.record_execution(aid,digest(b'output'),'SUCCEEDED'))
 def test_durable_chain(self):
  self.approve();self.store.close();self.store=GovernanceStore(self.path,raw(self.root),clock=lambda:NOW)
  self.assertTrue(self.store.verify_chain())
 def test_tampered_chain(self):
  self.approve();self.store.db.execute("UPDATE events SET payload='{}' WHERE seq=1")
  self.assertFalse(self.store.verify_chain())
 def test_nonce_reuse_new_signature(self):
  self.assertIsNotNone(self.approve());self.assertIsNone(self.approve(self.receipt(issued_at=NOW-2)))
if __name__=='__main__':unittest.main()
