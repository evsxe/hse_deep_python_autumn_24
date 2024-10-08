import unittest

from custom_metaclass import CustomMeta


class TestCustomMeta(unittest.TestCase):
    def test_class_attribute_prefix(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            CustomClass.x

    def test_instance_attribute_prefix(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        inst = CustomClass()
        self.assertEqual(inst.custom_x, 50)
        self.assertEqual(inst.custom_val, 99)
        self.assertEqual(inst.custom_line(), 100)
        self.assertEqual(str(inst), "Custom_by_metaclass")

        with self.assertRaises(AttributeError):
            _ = inst.x
        with self.assertRaises(AttributeError):
            _ = inst.val
        with self.assertRaises(AttributeError):
            _ = inst.line()
        with self.assertRaises(AttributeError):
            _ = inst.yyy

    def test_dynamic_attribute_prefix(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        inst = CustomClass()
        inst.dynamic = "added later"
        self.assertEqual(inst.custom_dynamic, "added later")
        with self.assertRaises(AttributeError):
            _ = inst.dynamic


if __name__ == '__main__':
    unittest.main()
