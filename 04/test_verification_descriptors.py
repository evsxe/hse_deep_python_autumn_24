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
        with self.assertRaises(ValueError) as context:
            data_instance.num = "not an integer"
        self.assertEqual(
            str(context.exception),
            "Invalid value for num: not an integer"
        )

    def test_invalid_num_type_during_init(self):
        with self.assertRaises(ValueError) as context:
            Data("not an integer", "Sample Item", 20)
        self.assertEqual(
            str(context.exception),
            "Invalid value for num: not an integer"
        )

    def test_empty_name(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError) as context:
            data_instance.name = ""
        self.assertEqual(str(context.exception),
                         "Invalid value for name: ")

    def test_empty_name_during_init(self):
        with self.assertRaises(ValueError) as context:
            Data(1, "", 20)
        self.assertEqual(str(context.exception),
                         "Invalid value for name: ")

    def test_negative_price(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError) as context:
            data_instance.price = -5
        self.assertEqual(str(context.exception),
                         "Invalid value for price: -5")

    def test_zero_price(self):
        data_instance = Data(1, "Sample Item", 20)
        with self.assertRaises(ValueError) as context:
            data_instance.price = 0
        self.assertEqual(str(context.exception),
                         "Invalid value for price: 0")

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

    def test_large_integer(self):
        data_instance = Data(1, "Sample Item", 20)
        data_instance.num = 2 ** 63 - 1
        self.assertEqual(data_instance.num, 2 ** 63 - 1)

    def test_max_int_price(self):
        data_instance = Data(1, "Sample Item", 20)
        data_instance.price = 2 ** 31 - 1
        self.assertEqual(data_instance.price, 2 ** 31 - 1)

    def test_repr(self):
        data_instance = Data(1, "Sample Item", 20)
        self.assertEqual(repr(data_instance),
                         "Data(num=1, name='Sample Item', price=20)")

    def test_display_info(self):
        data_instance = Data(1, "Sample Item", 20)
        self.assertEqual(data_instance.display_info(),
                         "Data Info - Num: 1, Name: Sample Item, Price: 20")

    def test_update_price(self):
        data_instance = Data(1, "Sample Item", 20)
        data_instance.update_price(30)
        self.assertEqual(data_instance.price, 30)

    def test_independent_instances(self):
        data1 = Data(1, "Item A", 10)
        data2 = Data(2, "Item B", 20)

        data1.num = 100
        self.assertEqual(data1.num, 100)
        self.assertEqual(data2.num,
                         2)

        with self.assertRaises(ValueError):
            data1.name = ""
        self.assertEqual(data1.name, "Item A")
        self.assertEqual(data2.name, "Item B")

    def test_failed_validation_does_not_change_value(self):
        data = Data(1, "Item A", 10)
        original_num = data.num
        original_name = data.name
        original_price = data.price

        try:
            data.num = "invalid"
        except ValueError:
            pass
        self.assertEqual(data.num, original_num)

        try:
            data.name = ""
        except ValueError:
            pass
        self.assertEqual(data.name, original_name)

        try:
            data.price = -5
        except ValueError:
            pass
        self.assertEqual(data.price, original_price)


if __name__ == '__main__':
    unittest.main()
