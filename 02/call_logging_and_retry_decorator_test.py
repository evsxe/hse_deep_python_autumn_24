import logging
import unittest

from unittest.mock import patch
from call_logging_and_retry_decorator import retry_deco


class TestRetryDeco(unittest.TestCase):

    def test_add_success(self):
        @retry_deco(retries=1)
        def add(a, b):
            return a + b

        result = add(4, 2)
        self.assertEqual(result, 6)

    def test_add_success_with_kwargs(self):
        @retry_deco(retries=1)
        def add(a, b):
            return a + b

        result = add(4, b=2)
        self.assertEqual(result, 6)

    def test_check_str_success(self):
        @retry_deco(retries=1)
        def check_str(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, str)

        result = check_str(value="123")
        self.assertTrue(result)

    def test_check_str_failure(self):
        @retry_deco(retries=1)
        def check_str(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, str)

        result = check_str(value=1)
        self.assertFalse(result)

    def test_check_str_retry(self):
        @retry_deco(retries=3)
        def check_str(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, str)

        result = check_str(value=None)
        self.assertIsNone(result)

    def test_check_int_success(self):
        @retry_deco(retries=1)
        def check_int(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, int)

        result = check_int(value=1)
        self.assertTrue(result)

    def test_check_int_failure_with_expected_exception(self):
        @retry_deco(retries=2, exceptions=[ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, int)

        result = check_int(value=None)
        self.assertIsNone(result)

    def test_check_int_failure_with_unexpected_exception(self):
        @retry_deco(retries=2, exceptions=[TypeError])
        def check_int(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, int)

        with patch.object(logging, 'info') as mock_log:
            check_int(value=None)
            mock_log.assert_any_call(
                "Reached maximum retries (2) for check_int."
            )


if __name__ == '__main__':
    unittest.main()
