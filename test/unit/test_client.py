import unittest

from pdp import PolicyDecisionPointClient


class TestPolicyDecisionPointClient(unittest.TestCase):
    def test_get_endpoint(self):
        test_cases = [
            (
                PolicyDecisionPointClient(),
                'http://localhost:8181/v1/data/authz'
            ),
            (
                PolicyDecisionPointClient(hostname='localhost'),
                'http://localhost:8181/v1/data/authz'
            ),
            (
                PolicyDecisionPointClient(hostname='xyz.com'),
                'http://xyz.com:8181/v1/data/authz'
            ),
            (
                PolicyDecisionPointClient(hostname='http://xyz.com'),
                'http://xyz.com:8181/v1/data/authz'
            ),
            (
                PolicyDecisionPointClient(port=8182),
                'http://localhost:8182/v1/data/authz'
            ),
            (
                PolicyDecisionPointClient(policy_path='/policy/path'),
                'http://localhost:8181/v1/data/policy/path'
            ),
            (
                PolicyDecisionPointClient(policy_path='policy/path'),
                'http://localhost:8181/v1/data/policy/path'
            ),
            (
                PolicyDecisionPointClient(policy_path='/v1/data/policy/path'),
                'http://localhost:8181/v1/data/policy/path'
            ),
            (
                PolicyDecisionPointClient(hostname='xyz.com', port=8182, policy_path='policy/path'),
                'http://xyz.com:8182/v1/data/policy/path'
            ),
        ]

        for i, case in enumerate(test_cases):
            client, expected_endpoint = case
            self.assertEqual(client.endpoint, expected_endpoint, msg='Running subtest {}'.format(i))


if __name__ == '__main__':
    unittest.main()
