import json
import unittest

from pdp import PolicyDecisionPointInput


class TestPolicyDecisionPointInput(unittest.TestCase):
    def test__init__(self):
        test_cases = [
            (
                PolicyDecisionPointInput(schema='some_schema'),
                ['request', 'schema'],
                'some_schema'
                
            ),
            (
                PolicyDecisionPointInput(method='some_method'),
                ['request', 'method'],
                'some_method'
            ),
            (
                PolicyDecisionPointInput(path='some_path'),
                ['request', 'path'],
                'some_path'
            ),
            (
                PolicyDecisionPointInput(query={
                    'k1': 'v1',
                    'k2': 'v2',
                }),
                ['request', 'query'],
                {
                    'k1': 'v1',
                    'k2': 'v2',
                }
            ),
            (
                PolicyDecisionPointInput(query={
                    'k1': 'v1',
                    'k2': ['v2', 'v3'],
                }),
                ['request', 'query'],
                {
                    'k1': 'v1',
                    'k2': 'v2,v3',
                }
            ),
            (
                PolicyDecisionPointInput(headers={
                    'k1': 'v1',
                    'k2': 'v2',
                }),
                ['request', 'headers'],
                {
                    'k1': 'v1',
                    'k2': 'v2',
                }
            ),
            (
                PolicyDecisionPointInput(headers={
                    'k1': 'v1',
                    'k2': ['v2', 'v3'],
                }),
                ['request', 'headers'],
                {
                    'k1': 'v1',
                    'k2': 'v2,v3',
                }
            ),
            (
                PolicyDecisionPointInput(source_ip='some_ip'),
                ['source', 'ipAddress'],
                'some_ip'
            ),
            (
                PolicyDecisionPointInput(source_port=1234),
                ['source', 'port'],
                1234
            ),
            (
                PolicyDecisionPointInput(destination_ip='some_ip'),
                ['destination', 'ipAddress'],
                'some_ip'
            ),
            (
                PolicyDecisionPointInput(destination_port=1234),
                ['destination', 'port'],
                1234
            ),
            (
                PolicyDecisionPointInput(some_enrich_key='some_enrich_value'),
                ['some_enrich_key'],
                'some_enrich_value'
            ),
            (
                PolicyDecisionPointInput(some_other_enrich_key={
                    'enrich_k1': 'v1',
                    'enrich_k2': 'v2',
                }),
                ['some_other_enrich_key'],
                {
                    'enrich_k1': 'v1',
                    'enrich_k2': 'v2',
                }
            ),
        ]

        for i, case in enumerate(test_cases):
            input_obj, input_path, expected_value = case

            o = input_obj
            for path_step in input_path:
                o = o.get(path_step, None)

                self.assertIsNotNone(o, msg='running test {}: expected value {} at path {} in object {}'.format(
                                                        i, expected_value, input_path, input_obj))

            self.assertEqual(o, expected_value, msg='running test {}: inspecting path {} in object {}'.format(
                                                                i, input_path, input_obj))

    @staticmethod
    def json_roundtrip(self, obj: dict) -> dict:
        j = json.dumps(obj)

        obj = json.loads(j)

        return obj


if __name__ == '__main__':
    unittest.main()
