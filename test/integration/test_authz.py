import unittest
from unittest.mock import Mock, MagicMock, patch

from requests import Response

from pdp import PolicyDecisionPointClient, PolicyDecisionPointInput, AuthzException


class TestPolicyDecisionPointClient(unittest.TestCase):

    mock_response = Mock(spec=Response)

    def test_authorize_true(self):
        client = PolicyDecisionPointClient()

        self.mock_response.ok = True
        self.mock_response.json = MagicMock(return_value={'result': True})

        client.session.post = MagicMock(return_value=self.mock_response)

        authz = client.authorize(PolicyDecisionPointInput(method='GET'))

        self.assertTrue(authz)

    def test_authorize_false(self):
        client = PolicyDecisionPointClient()

        self.mock_response.ok = True
        self.mock_response.json = MagicMock(return_value={'result': False})

        client.session.post = MagicMock(return_value=self.mock_response)

        authz = client.authorize(PolicyDecisionPointInput(method='GET'))

        self.assertFalse(authz)

    def test_authorize_exception(self):
        client = PolicyDecisionPointClient()

        self.mock_response.ok = False
        self.mock_response.status_code = 500

        client.session.post = MagicMock(return_value=self.mock_response)

        with self.assertRaises(AuthzException):
            client.authorize(PolicyDecisionPointInput(method='GET'))


if __name__ == '__main__':
    unittest.main()
