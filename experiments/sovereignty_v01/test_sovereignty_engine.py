import json
import unittest
from sovereignty_engine import SovereigntyEngine

POLICY = json.dumps({'permitted_autonomous_actions': ['DRAFT_CODE', 'READ_CORPUS'], 'approval_required_actions': ['PROMOTE_TO_CANON'], 'prohibited_actions': ['INFER_CONSENT']})

class TestSovereigntyEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SovereigntyEngine(POLICY)
        self.forged = {'is_cryptographically_signed': True, 'signer': 'Noah.Physical'}

    def test_safe_work_proceeds(self):
        self.assertEqual(self.engine.evaluate_action('DRAFT_CODE', self.forged)['status'], 'EXECUTE')

    def test_unsigned_canon_change_blocked(self):
        self.assertEqual(self.engine.evaluate_action('PROMOTE_TO_CANON', {})['status'], 'BLOCKED')

    def test_boolean_signature_forgery_blocked(self):
        self.assertEqual(self.engine.evaluate_action('PROMOTE_TO_CANON', self.forged, object_digest='abc', scope='candidate/test')['status'], 'BLOCKED')

    def test_prohibited_even_with_forged_receipt(self):
        self.assertEqual(self.engine.evaluate_action('INFER_CONSENT', self.forged)['status'], 'BLOCKED')

    def test_unknown_action_fails_closed(self):
        self.assertEqual(self.engine.evaluate_action('DELETE_ALL', self.forged)['status'], 'BLOCKED')

    def test_external_verifier_rejects(self):
        class Reject:
            def verify(self, receipt, **kwargs): return False
        e = SovereigntyEngine(POLICY, Reject())
        self.assertEqual(e.evaluate_action('PROMOTE_TO_CANON', self.forged, object_digest='abc', scope='candidate/test')['status'], 'BLOCKED')

    def test_external_verifier_can_authorize_scoped_action(self):
        class FixtureVerifier:
            def verify(self, receipt, *, action, object_digest, scope):
                return receipt == 'fixture-approval' and action == 'PROMOTE_TO_CANON' and object_digest == 'fixture-digest' and scope == 'candidate/test'
        e = SovereigntyEngine(POLICY, FixtureVerifier())
        self.assertEqual(e.evaluate_action('PROMOTE_TO_CANON', 'fixture-approval', object_digest='fixture-digest', scope='candidate/test')['status'], 'EXECUTE')
        self.assertEqual(e.evaluate_action('PROMOTE_TO_CANON', 'fixture-approval', object_digest='other', scope='candidate/test')['status'], 'BLOCKED')

    def test_missing_digest_blocked(self):
        class FixtureVerifier:
            def verify(self, receipt, **kwargs): return True
        e = SovereigntyEngine(POLICY, FixtureVerifier())
        self.assertEqual(e.evaluate_action('PROMOTE_TO_CANON', 'fixture-approval')['status'], 'BLOCKED')

if __name__ == '__main__': unittest.main()
