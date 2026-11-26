"""Finite scoped checks for RR-CCS-003 v0.2, not a cryptographic proof."""
import itertools
import hashlib
import unittest


def bits_required(n):
    assert n > 0
    return (n - 1).bit_length()


def has_coloring(edges, n, k):
    for colors in itertools.product(range(k), repeat=n):
        if all(colors[i] != colors[j] for i, j in edges):
            return True
    return False


class CorrectedClaims(unittest.TestCase):
    def test_same_view_binary_correctness(self):
        for out in ('YES', 'NO', 'ABSTAIN'):
            self.assertLessEqual(sum(out == q for q in ('YES', 'NO')), 1)

    def test_randomness_does_not_identify_missing_message(self):
        # World-independent output distribution on identical views.
        outputs = {'REFUSE': .25, 'DELAY': .25, 'PARTITION': .25, 'UNKNOWN': .25}
        p_right = sum(outputs[w] / 3 for w in ('REFUSE', 'DELAY', 'PARTITION'))
        self.assertAlmostEqual(p_right, .25)
        self.assertLessEqual(p_right, 1 / 3)

    def test_two_world_correct_definitive_verdict(self):
        correct = {'LIVE': 'GRANT', 'REVOKED': 'DENY'}
        for verdict in ('GRANT', 'DENY', 'ABSTAIN'):
            self.assertLessEqual(sum(verdict == x for x in correct.values()), 1)
        self.assertNotEqual('DENY', correct['LIVE'])

    def test_tagged_one_way_output_exposes_predicate(self):
        # A digest may reveal a predicate, independently of inversion difficulty.
        def output(payload):
            return bytes([payload[0] & 1]) + hashlib.sha256(payload).digest()
        for first in (0, 1):
            self.assertEqual(output(bytes([first]) + b'prefix')[0], first)

    def test_count_distinct_answer_vectors(self):
        independent = set(itertools.product((0, 1), repeat=6))
        correlated = {(a, b, c, a, b, c)
                      for a, b, c in itertools.product((0, 1), repeat=3)}
        self.assertEqual(bits_required(len(independent)), 6)
        self.assertEqual(bits_required(len(correlated)), 3)
        self.assertEqual(bits_required(2), 1)

    def test_decoder_side_information_five_cycle(self):
        edges = [(i, (i + 1) % 5) for i in range(5)]
        self.assertFalse(has_coloring(edges, 5, 2))
        self.assertTrue(has_coloring(edges, 5, 3))
        self.assertEqual(bits_required(3), 2)

    def test_allowed_output_sets_need_joint_consistency(self):
        outputs = ({'a', 'b'}, {'b', 'c'}, {'a', 'c'})
        self.assertTrue(all(a & b for a, b in itertools.combinations(outputs, 2)))
        self.assertFalse(set.intersection(*outputs))

    def test_conditional_policy_baseline(self):
        # Reported original counts, not a trial-level replay.
        n, safe_executes, execute_cost, abstain_cost = 600, 100, 2, 5
        mean = (safe_executes * execute_cost +
                (n - safe_executes) * abstain_cost) / n
        self.assertEqual(mean, 4.5)
        self.assertLess(mean, abstain_cost)

    def test_old_certificate_does_not_prove_future_state(self):
        cert = ('HISTORICAL', 'GRANT', 3)
        worlds = [('LIVE', cert), ('REVOKED', cert)]
        self.assertEqual(worlds[0][1], worlds[1][1])
        self.assertNotEqual(worlds[0][0], worlds[1][0])

    def test_registration_order_not_production_order(self):
        registered = (('REVOKE', 10), ('SIGNATURE', 11))
        histories = [('SIGN', 'REVOKE'), ('REVOKE', 'SIGN')]
        self.assertEqual(registered, registered)
        self.assertNotEqual(histories[0], histories[1])


if __name__ == '__main__':
    unittest.main()
