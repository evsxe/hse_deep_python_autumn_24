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

    def test_check_int_success(self):
        @retry_deco(retries=1)
        def check_int(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, int)

        result = check_int(value=1)
        self.assertTrue(result)

    def test_check_int_type_error(self):
        @retry_deco(retries=1, exceptions=[TypeError])
        def check_int(value=None):
            if value is None:
                raise TypeError()

            return isinstance(value, int)

        result = check_int(value="123")
        self.assertFalse(result)

    def test_retry_with_exceptions(self):
        @retry_deco(retries=2, exceptions=[ValueError])
        def check_str(value=None):
            if value is None:
                raise ValueError()

            return isinstance(value, str)

        result = check_str(value=1)
        self.assertFalse(result)


    def test_max_retries(self):
        @retry_deco(retries=2)
        def raise_error():
            raise ValueError()

        result = raise_error()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
