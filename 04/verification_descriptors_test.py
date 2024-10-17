import unittest
from verification_descriptors import Data


class TestData(unittest.TestCase):

    def test_valid_data_initialization(self):
        data_instance = Data(1, "Sample Item", 20)
        self.assertEqual(data_instance.num, 1)
        self.assertEqual(data_instance.name, "Sample Item")
        self.assertEqual(data_instance.price, 20)

    def test_invalid_num_type(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError):
            data_instance.num = "not an integer"

    def test_empty_name(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError):
            data_instance.name = ""

    def test_negative_price(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError):
            data_instance.price = -5

    def test_valid_updates(self):
        data_instance = Data(1, "Sample Item", 20)
        data_instance.num = 2
        data_instance.name = "Updated Item"
        data_instance.price = 30

        self.assertEqual(data_instance.num, 2)
        self.assertEqual(data_instance.name, "Updated Item")
        self.assertEqual(data_instance.price, 30)

    def test_invalid_updates(self):
        data_instance = Data(1, "Sample Item", 20)

        with self.assertRaises(ValueError):
            data_instance.num = 1.5

        with self.assertRaises(ValueError):
            data_instance.name = None

        with self.assertRaises(ValueError):
            data_instance.price = 0


if __name__ == '__main__':
    unittest.main()
