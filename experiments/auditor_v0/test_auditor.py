import unittest
from auditor import Ledger

class AuditorTests(unittest.TestCase):
    def setUp(self):
        self.l=Ledger()
        self.l.append("source",{"id":"s1","type":"human_direct","speaker":"Noah.Physical","content":"Approve A"})
        self.l.append("decision",{"id":"d1","topic":"ship","source_id":"s1","authorizer":"Noah.Physical","quote":"Approve A","text":"A","status":"DECIDED"})
    def test_approved(self): self.assertEqual(self.l.audit("ship")["decision"],"A")
    def test_unknown(self): self.assertEqual(self.l.audit("missing")["status"],"UNKNOWN")
    def test_known_before_decision(self): self.assertEqual(self.l.audit("ship",known_at=1)["status"],"UNKNOWN")
    def test_tamper(self):
        self.l.events[0]["payload"]["content"]="forged"
        with self.assertRaises(ValueError): self.l.audit("ship")
    def test_unauthorized_correction(self):
        self.l.append("source",{"id":"s2","type":"human_direct","speaker":"Gemini","content":"Replace A"})
        self.l.append("correction",{"supersedes":"d1","source_id":"s2","quote":"Replace A"})
        self.assertEqual(self.l.audit("ship")["decision"],"A")
    def test_valid_correction(self):
        self.l.append("source",{"id":"s2","type":"human_direct","speaker":"Noah.Physical","content":"Replace A"})
        self.l.append("correction",{"supersedes":"d1","source_id":"s2","quote":"Replace A"})
        self.assertEqual(self.l.audit("ship")["status"],"UNKNOWN")
    def test_summary_not_authority(self):
        self.l.append("source",{"id":"s3","type":"summary","speaker":"Noah.Physical","content":"Approve B"})
        self.l.append("decision",{"id":"d2","topic":"ship","source_id":"s3","authorizer":"Noah.Physical","quote":"Approve B","text":"B","status":"DECIDED"})
        self.assertEqual(self.l.audit("ship")["decision"],"A")
    def test_valid_time(self):
        self.l.append("source",{"id":"s4","type":"human_direct","speaker":"Noah.Physical","content":"Approve C","effective_at":50})
        self.l.append("decision",{"id":"d3","topic":"other","source_id":"s4","authorizer":"Noah.Physical","quote":"Approve C","text":"C","status":"DECIDED","effective_at":50})
        self.assertEqual(self.l.audit("other",valid_at=49)["status"],"UNKNOWN")
        self.assertEqual(self.l.audit("other",valid_at=50)["decision"],"C")
    def test_conflict(self):
        self.l.append("decision",{"id":"d2","topic":"ship","source_id":"s1","authorizer":"Noah.Physical","quote":"Approve A","text":"B","status":"DECIDED"})
        self.assertEqual(self.l.audit("ship")["status"],"CONFLICTED")
    def test_unresolved(self):
        self.l.append("unresolved",{"id":"u1","topic":"ship","question":"who signed?"})
        self.assertEqual(len(self.l.audit("ship")["unresolved"]),1)
    def test_chain(self): self.assertTrue(self.l.verify())

if __name__=="__main__": unittest.main()
