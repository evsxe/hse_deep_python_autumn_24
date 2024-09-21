import json
import unittest

from process_json import process_json


class TestProcessJson(unittest.TestCase):

    def test_empty_json(self):
        json_str = '{}'
        process_json(
            json_str=json_str
        )

    def test_json_str_not_str(self):
        json_str = 123
        with self.assertRaises(TypeError):
            process_json(
                json_str=json_str
            )

    def test_invalid_json_str(self):
        json_str = '{"name": "John Doe", "age": 30]'
        with self.assertRaises(json.decoder.JSONDecodeError):
            process_json(
                json_str=json_str
            )

    def test_no_required_keys(self):
        json_str = '{"name": "John Doe", "age": 30}'
        process_json(
            json_str=json_str
        )

    def test_required_keys_present(self):
        json_str = '{"name": "John Doe", "age": 30}'
        required_keys = ["name", "age"]
        process_json(
            json_str=json_str,
            required_keys=required_keys
        )

    def test_tokens_present(self):
        json_str = '{"name": "John Doe", "age": 30}'
        tokens = ["John", "Doe"]

        def callback(key, token):
            return f"{key}: {token}"

        process_json(
            json_str=json_str,
            tokens=tokens,
            callback=callback
        )

    def test_tokens_not_present(self):
        json_str = '{"name": "John Doe", "age": 30}'
        tokens = ["Jane", "Smith"]

        def callback(key, token):
            return f"{key}: {token}"

        process_json(
            json_str=json_str,
            tokens=tokens,
            callback=callback
        )

    def test_callback_function(self):
        json_str = '{"name": "John Doe", "age": 30}'
        required_keys = ["name"]
        tokens = ["John"]

        def callback(key, token):
            return f"{key}: {token}"

        process_json(
            json_str=json_str,
            required_keys=required_keys,
            tokens=tokens,
            callback=callback
        )


if __name__ == '__main__':
    unittest.main()
