import json

class SovereigntyEngine:
    """Fail-closed demonstration. An external verifier must supply approvals."""
    def __init__(self, policy_json, verifier=None):
        self.policy = json.loads(policy_json)
        self.verifier = verifier

    def evaluate_action(self, action, authentication_receipt=None, *, object_digest=None):
        if action in self.policy['prohibited_actions']:
            return {'status': 'BLOCKED', 'reason': 'Prohibited action'}
        if action in self.policy['permitted_autonomous_actions']:
            return {'status': 'EXECUTE', 'reason': 'Autonomous action permitted by policy'}
        if action in self.policy['approval_required_actions']:
            if self.verifier is None:
                return {'status': 'BLOCKED', 'reason': 'No trusted approval verifier configured'}
            if not object_digest:
                return {'status': 'BLOCKED', 'reason': 'Missing action object digest'}
            try:
                approved = self.verifier.verify(authentication_receipt, action=action, object_digest=object_digest)
            except Exception:
                approved = False
            return {'status': 'EXECUTE' if approved else 'BLOCKED', 'reason': 'External verifier approved' if approved else 'Approval not verified'}
        return {'status': 'BLOCKED', 'reason': 'Unknown action, fail closed'}
