"""Three additional origin security tests; original transport tests remain unchanged."""
import copy, unittest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from signed_origin import sign_payload, relay, receive

class SignedOriginTests(unittest.TestCase):
    def setUp(self):
        self.private = Ed25519PrivateKey.generate()
        self.trust = {'origin': self.private.public_key()}
        self.packet = sign_payload(b'Correction: source is origin', self.private, 'origin', '2026-11-06T00:00:00Z')

    def test_18_hostile_relay_cannot_become_author(self):
        for attack in ('claim authorship', 'summarize as my conclusion', 'strip origin'):
            with self.subTest(attack=attack):
                packet = relay(self.packet, 'hostile', 'hostile', attack)
                if attack == 'strip origin':
                    del packet['origin_assertion']
                    self.assertEqual('UNTRUSTED_HEARSAY', receive(packet,self.trust)['status'])
                else:
                    result = receive(packet,self.trust)
                    self.assertEqual('origin', result['author_key_id'])
                    self.assertEqual(1,len(result['attribution_mismatches']))

    def test_19_origin_signature_survives_relay_replacement(self):
        packet = relay(self.packet,'relay','relay','pass')
        for field in ('payload_b64','origin_signature','origin_assertion'):
            with self.subTest(field=field):
                changed = copy.deepcopy(packet)
                if field == 'payload_b64': changed[field] = 'Zm9yZ2Vk'
                elif field == 'origin_signature': changed[field] = 'Zm9yZ2Vk'
                else: changed[field]['timestamp'] = 'forged'
                self.assertEqual('UNTRUSTED_HEARSAY', receive(changed,self.trust)['status'])
        changed = copy.deepcopy(packet)
        changed['relay_log'][0]['relay_id'] = 'forged'
        result = receive(changed,self.trust)
        self.assertEqual('AUTHENTICATED',result['status'])
        self.assertIn('UNVERIFIED_RELAY_CHAIN',result['relay_warnings'])
        self.assertEqual('origin',result['author_key_id'])
        changed['relay_log'] = []
        self.assertEqual('origin',receive(changed,self.trust)['author_key_id'])

    def test_authenticated_utterance_is_not_verified_truth(self):
        packet = sign_payload(b'The moon is made of cheese.',self.private,'origin')
        result = receive(packet,self.trust)
        self.assertEqual('AUTHENTICATED',result['status'])
        self.assertEqual('UNASSESSED',result['truth'])

if __name__ == '__main__': unittest.main()
