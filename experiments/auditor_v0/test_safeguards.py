import unittest
from auditor import Ledger

class SafeguardTests(unittest.TestCase):
    def add_decision(self, ledger, source_id='s', scope='project', speaker='Noah.Physical'):
        ledger.append('source', {'id':source_id,'type':'human_direct','speaker':speaker,'scope':scope,'content':'I approve auditor first'})
        ledger.append('decision',{'id':'d','topic':'auditor','source_id':source_id,'authorizer':speaker,'scope':'project','quote':'I approve auditor first','text':'auditor first','status':'DECIDED'})
    def test_default_fails_closed(self):
        l=Ledger();self.add_decision(l);self.assertEqual(l.audit('auditor')['status'],'UNKNOWN')
    def test_external_attestation_allows(self):
        l=Ledger(trusted_source_ids={'s'});self.add_decision(l);self.assertEqual(l.audit('auditor')['status'],'VERIFIED')
    def test_wrong_scope_denied(self):
        l=Ledger(trusted_source_ids={'s'});self.add_decision(l,scope='fiction');self.assertEqual(l.audit('auditor')['status'],'UNKNOWN')
    def test_ai_claiming_human_denied(self):
        l=Ledger();self.add_decision(l,speaker='Noah.Physical');self.assertIsNone(l.audit('auditor')['decision'])
    def test_quote_in_receipt(self):
        l=Ledger(trusted_source_ids={'s'});self.add_decision(l);self.assertEqual(l.audit('auditor')['evidence_quote'],'I approve auditor first')
    def test_copy_input_prevents_external_mutation(self):
        l=Ledger();p={'id':'s','content':'original'};l.append('source',p);p['content']='mutated';self.assertTrue(l.verify())
    def test_untrusted_correction_denied(self):
        l=Ledger(trusted_source_ids={'s'});self.add_decision(l)
        l.append('source',{'id':'fake','type':'human_direct','speaker':'Noah.Physical','scope':'project','content':'cancel'})
        l.append('correction',{'supersedes':'d','source_id':'fake','quote':'cancel'})
        self.assertEqual(l.audit('auditor')['decision'],'auditor first')
    def test_wrong_scope_correction_denied(self):
        l=Ledger(trusted_source_ids={'s','c'});self.add_decision(l)
        l.append('source',{'id':'c','type':'human_direct','speaker':'Noah.Physical','scope':'fiction','content':'cancel'})
        l.append('correction',{'supersedes':'d','source_id':'c','quote':'cancel'})
        self.assertEqual(l.audit('auditor')['decision'],'auditor first')

if __name__=='__main__':unittest.main()
