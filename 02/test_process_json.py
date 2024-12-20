import json
import unittest
from unittest.mock import patch, call

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

    @patch('process_json.print')
    def test_tokens_not_present(self, mock_print):
        json_str = '{"name": "John Doe", "age": 30}'
        tokens = ["Jane", "Smith"]
        process_json(json_str=json_str, tokens=tokens)
        mock_print.assert_not_called()

    @patch('process_json.print')
    def test_callback_function(self, mock_print):
        json_str = '{"name": "John Doe", "age": 30}'
        required_keys = ["name"]
        tokens = ["John"]

        def callback(key, token):
            return f"{key}: {token}"

        process_json(json_str=json_str, required_keys=required_keys,
                     tokens=tokens, callback=callback)
        mock_print.assert_called_once_with("name: John")

    @patch('process_json.print')
    def test_multiple_required_keys_and_tokens(self, mock_print):
        json_str = '{"name": "John Doe", "city": "New York", "age": 30}'
        required_keys = ["name", "city"]
        tokens = ["John", "York"]
        process_json(json_str=json_str, required_keys=required_keys,
                     tokens=tokens)
        mock_print.assert_has_calls([call("name: John"), call("city: York")])

    @patch('process_json.print')
    def test_multiple_tokens_per_key(self, mock_print):
        json_str = '{"name": "John Doe, Jane Doe"}'
        required_keys = ["name"]
        tokens = ["John", "Jane"]
        process_json(json_str=json_str, required_keys=required_keys,
                     tokens=tokens)
        mock_print.assert_has_calls([call("name: John"), call("name: Jane")])

    @patch('process_json.print')
    def test_case_insensitive_token_search(self, mock_print):
        json_str = '{"name": "john doe"}'
        required_keys = ["name"]
        tokens = ["JOHN"]
        process_json(json_str=json_str, required_keys=required_keys,
                     tokens=tokens)
        mock_print.assert_called_once_with("name: JOHN")

    def test_none_arguments(self):
        json_str = '{"name": "John Doe", "age": 30}'
        process_json(json_str=json_str, required_keys=None, tokens=None,
                     callback=None)


if __name__ == '__main__':
    unittest.main()
