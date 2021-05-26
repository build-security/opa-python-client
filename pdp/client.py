from urllib3.util.retry import Retry

from requests.adapters import HTTPAdapter
from requests.exceptions import RequestException
import requests

from .input import PolicyDecisionPointInput


class PolicyDecisionPointClient:
    """Client to ask the Policy Decision Point (PDP) for authz decisions"""

    def __init__(
            self,
            hostname: str = "http://localhost",
            port: int = 8181,
            policy_path: str = "/authz",
            read_timeout_milliseconds: int = 5000,
            connection_timeout_milliseconds: int = 5000,
            retry_max_attempts: int = 2,
            retry_backoff_milliseconds: int = 250,
    ):
        self.hostname = hostname
        self.port = port
        self.policy_path = policy_path
        self.read_timeout_milliseconds = read_timeout_milliseconds
        self.connection_timeout_milliseconds = connection_timeout_milliseconds
        self.retry_max_attempts = retry_max_attempts
        self.retry_backoff_milliseconds = retry_backoff_milliseconds

        self.endpoint = self._get_endpoint()

        self.session = requests.Session()

        retries = Retry(
            total=self.retry_max_attempts,
            backoff_factor=self.retry_backoff_milliseconds/1000,
        )

        self.session.mount(self.endpoint, HTTPAdapter(max_retries=retries))

    def _get_endpoint(self):
        if not ('://' in self.hostname):
            self.hostname = 'http://' + self.hostname

        if self.hostname[-1] == '/':
            self.hostname = self.hostname[:-1]

        if self.policy_path[0] != '/':
            self.policy_path = '/' + self.policy_path

        if not self.policy_path.startswith('/v1/data'):
            self.policy_path = '/v1/data' + self.policy_path

        return self.hostname + ':' + str(self.port) + self.policy_path

    def authorize(self, pdp_input: PolicyDecisionPointInput) -> bool:
        try:
            res = self.session.post(
                self.endpoint,
                timeout=(self.connection_timeout_milliseconds/1000, self.read_timeout_milliseconds/1000),
                json=pdp_input,
            )
        except RequestException as e:
            raise AuthzException from e

        if not res.ok:
            raise AuthzException('Policy Decision Point at endpoint {} returned with status code {}'.format(
                self.endpoint, res.status_code))

        try:
            if res.json()['result'] is True:
                return True
            else:
                return False
        except (ValueError, KeyError) as e:
            raise AuthzException from e


class AuthzException(Exception):
    pass
