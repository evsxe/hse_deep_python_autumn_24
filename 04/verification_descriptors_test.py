import unittest

from verification_descriptors import (
    FloatDescriptor,
    NonEmptyStringDescriptor,
    RangeDescriptor,
    Product
)


class TestDescriptors(unittest.TestCase):

    def test_float_descriptor(self):
        class TestClass:
            value = FloatDescriptor()

        test_instance = TestClass()
        test_instance.value = 3.14
        self.assertEqual(test_instance.value, 3.14)

        with self.assertRaises(ValueError):
            test_instance.value = "hello"

    def test_non_empty_string_descriptor(self):
        class TestClass:
            name = NonEmptyStringDescriptor()

        test_instance = TestClass()
        test_instance.name = "John Doe"
        self.assertEqual(test_instance.name, "John Doe")

        with self.assertRaises(ValueError):
            test_instance.name = ""

        with self.assertRaises(ValueError):
            test_instance.name = 123

    def test_range_descriptor(self):
        class TestClass:
            quantity = RangeDescriptor(0, 10)

        test_instance = TestClass()
        test_instance.quantity = 5

        self.assertEqual(test_instance.quantity, 5)

        with self.assertRaises(ValueError):
            test_instance.quantity = -1

        with self.assertRaises(ValueError):
            test_instance.quantity = 11

        with self.assertRaises(ValueError):
            test_instance.quantity = "ten"

    def test_product(self):
        product = Product(10.99, "Laptop", 5)
        self.assertEqual(product.price, 10.99)
        self.assertEqual(product.name, "Laptop")
        self.assertEqual(product.quantity, 5)

        with self.assertRaises(ValueError):
            _ = Product(
                "invalid",  # pylint: disable=all
                "Laptop",
                5
            )

        with self.assertRaises(ValueError):
            _ = Product(10.99, "", 5)

        with self.assertRaises(ValueError):
            _ = Product(10.99, "Laptop", -2)
            _ = Product(10.99, "Laptop", 105)


if __name__ == '__main__':
    unittest.main()
