import json
import unittest
import custom_json


class TestCustomJson(unittest.TestCase):

    def test_loads_valid(self):
        valid_cases = [
            '{"a": 1, "b": "hello"}',
            '{"a": 100, "b": "world"}',
            '{"a": -123, "b": "negative"}',  # Negative number
            '{"a": 0, "b": ""}',  # Zero and empty string
            '{"a": 1, "b": "hello", "c": 3}',  # Multiple Key Value pairs
        ]

        for case in valid_cases:
            expected = json.loads(case)
            actual = custom_json.loads(case)
            self.assertEqual(expected, actual, f"Failed for input: {case}")

    def test_loads_dumps_roundtrip(self):
        data_cases = [
            {"a": 1, "b": "hello", "c": 1234567890},
            {"a": -5, "b": "test", "c": 0},
            {"empty": ""}
        ]
        for data in data_cases:
            reloaded_data = custom_json.loads(custom_json.dumps(data))
            self.assertEqual(data, reloaded_data,
                             f"Roundtrip failed for data: {data}")

    def test_empty_dict(self):
        self.assertEqual(custom_json.loads("{}"), {})
        self.assertEqual(custom_json.dumps({}), "{}")

    def test_dumps_various_types(self):
        self.assertEqual(custom_json.dumps({"a": 1}), '{"a":1}')
        self.assertEqual(custom_json.dumps({"a": "hello"}), '{"a":"hello"}')
        self.assertEqual(custom_json.dumps({"a": -123}), '{"a":-123}')
        self.assertEqual(custom_json.dumps({"a": 0}), '{"a":0}')

    def test_dumps_errors(self):
        with self.assertRaises(TypeError):
            custom_json.dumps(123)
        with self.assertRaises(TypeError):
            custom_json.dumps({"a": 1, "b": [1, 2, 3]})


if __name__ == '__main__':
    unittest.main()
