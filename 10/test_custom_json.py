import json
import unittest
import custom_json


class TestCustomJson(unittest.TestCase):

    def test_loads_valid(self):
        valid_cases = [
            '{"a": 1, "b": "hello"}',
            '{"a": 100, "b": "world"}',
        ]

        for case in valid_cases:
            expected = json.loads(case)
            actual = custom_json.loads(case)
            self.assertEqual(expected,
                             actual,
                             f"Failed for input: {case}")

    def test_loads_dumps_roundtrip(self):
        data = {"a": 1, "b": "hello", "c": 1234567890}
        reloaded_data = custom_json.loads(custom_json.dumps(data))
        self.assertEqual(data, reloaded_data)

    def test_empty_dict(self):
        self.assertEqual(custom_json.loads("{}"), {})
        self.assertEqual(custom_json.dumps({}), "{}")


if __name__ == '__main__':
    unittest.main()
