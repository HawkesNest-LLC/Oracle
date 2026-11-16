import unittest
from esp_contract import validate, missing_claim, EnvelopeError, STATUSES, AUTHORITIES

class ContractTests(unittest.TestCase):
    def good(self):
        return {'claimId':'c-1','status':'PROPOSED','authority':'AI','confidence':0.4,'sources':['github:example']}
    def test_every_status(self):
        for s in STATUSES:
            x=self.good();x['status']=s;self.assertEqual(validate(x)['status'],s)
    def test_every_authority(self):
        for a in AUTHORITIES:
            x=self.good();x['authority']=a;self.assertEqual(validate(x)['authority'],a)
    def test_unknown_without_sources(self):self.assertEqual(missing_claim('missing')['status'],'UNKNOWN')
    def test_no_established_without_source(self):
        x=self.good();x['status']='ESTABLISHED';x['sources']=[]
        with self.assertRaises(EnvelopeError):validate(x)
    def test_invalid_status(self):
        x=self.good();x['status']='CANONICAL'
        with self.assertRaises(EnvelopeError):validate(x)
    def test_invalid_authority(self):
        x=self.good();x['authority']='SOVEREIGN_AI'
        with self.assertRaises(EnvelopeError):validate(x)
    def test_boolean_confidence(self):
        x=self.good();x['confidence']=True
        with self.assertRaises(EnvelopeError):validate(x)
    def test_out_of_range_confidence(self):
        x=self.good();x['confidence']=2
        with self.assertRaises(EnvelopeError):validate(x)
    def test_extra_field(self):
        x=self.good();x['approved']=True
        with self.assertRaises(EnvelopeError):validate(x)
    def test_missing_field(self):
        x=self.good();del x['sources']
        with self.assertRaises(EnvelopeError):validate(x)
    def test_bad_source(self):
        x=self.good();x['sources']=['']
        with self.assertRaises(EnvelopeError):validate(x)
    def test_empty_id(self):
        x=self.good();x['claimId']=''
        with self.assertRaises(EnvelopeError):validate(x)
if __name__=='__main__':unittest.main()
