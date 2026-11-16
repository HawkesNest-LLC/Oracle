import unittest
from engine import Ledger, Record, load

SRC = 'sha256:' + 'a'*64

def rec(id, value, event='2395-01-01T00:00:00Z', known='2397-01-01T00:00:00Z', branch='alpha', supersedes='', status='OBSERVED'):
    return Record(id, 'reg', 'chair_outcome', value, event, known, 'fictional-test-source:'+id, SRC, 'synthetic-test-author', branch, status, supersedes)

class WitnessTests(unittest.TestCase):
    def test_unknown(self):
        self.assertEqual(Ledger().query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['status'],'UNKNOWN')
    def test_original(self):
        l=Ledger();l.append(rec('a','survived'));self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['value'],'survived')
    def test_correction(self):
        l=Ledger();l.append(rec('a','survived'));l.append(rec('b','biological_death',known='2397-02-01T00:00:00Z',supersedes='a'))
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2397-01-15T00:00:00Z')['value'],'survived')
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2397-03-01T00:00:00Z')['value'],'biological_death')
    def test_conflict(self):
        l=Ledger();l.append(rec('a','survived'));l.append(rec('b','biological_death'))
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['status'],'CONFLICT')
    def test_branch_isolation(self):
        l=Ledger();l.append(rec('a','survived'));l.append(rec('b','biological_death',branch='beta'))
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['value'],'survived')
    def test_no_overwrite(self):
        l=Ledger();l.append(rec('a','survived'))
        with self.assertRaises(ValueError):l.append(rec('a','biological_death'))
    def test_no_cross_branch_supersession(self):
        l=Ledger();l.append(rec('a','survived'))
        with self.assertRaises(ValueError):l.append(rec('b','other',branch='beta',supersedes='a'))
    def test_proposed_not_fact(self):
        l=Ledger();l.append(rec('a','survived',status='PROPOSED'))
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['status'],'PROPOSED')
    def test_missing_provenance(self):
        with self.assertRaises(ValueError):Record('a','x','y','z','2395-01-01T00:00:00Z','2397-01-01T00:00:00Z','','','authority','alpha')
    def test_deterministic_digest(self):
        l=Ledger();l.append(rec('a','survived'));self.assertEqual(l.digest(),load(l.export()).digest())
    def test_event_time_gate(self):
        l=Ledger();l.append(rec('a','survived',event='2397-01-01T00:00:00Z'))
        self.assertEqual(l.query('reg','chair_outcome','alpha','2396-01-01T00:00:00Z','2398-01-01T00:00:00Z')['status'],'UNKNOWN')

if __name__ == '__main__': unittest.main(verbosity=2)
