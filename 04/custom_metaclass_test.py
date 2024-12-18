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

        CustomClass.custom_x = 50  # type: ignore
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            _ = CustomClass.x

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
        self.assertEqual(
            inst.custom_x,  # pylint: disable=all
            50
        )
        self.assertEqual(
            inst.custom_val,  # pylint: disable=all
            99
        )
        self.assertEqual(
            inst.custom_line(),  # pylint: disable=all
            100
        )
        self.assertEqual(
            str(inst),
            "Custom_by_metaclass"
        )

        with self.assertRaises(AttributeError):
            _ = inst.x
        with self.assertRaises(AttributeError):
            _ = inst.val
        with self.assertRaises(AttributeError):
            _ = inst.line()

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
        inst.dynamic = "added later"  # pylint: disable=all
        self.assertEqual(
            inst.custom_dynamic,  # pylint: disable=all
            "added later"
        )
        with self.assertRaises(AttributeError):
            _ = inst.dynamic

    def test_inheritance(self):
        class BaseClass(metaclass=CustomMeta):
            base_attr = 10

        class DerivedClass(BaseClass):
            derived_attr = 20

        self.assertEqual(
            DerivedClass.custom_base_attr,  # pylint: disable=all
            10
        )
        self.assertEqual(
            DerivedClass.custom_derived_attr,  # pylint: disable=all
            20
        )
        with self.assertRaises(AttributeError):
            _ = DerivedClass.base_attr
        with self.assertRaises(AttributeError):
            _ = DerivedClass.derived_attr

        inst = DerivedClass()
        self.assertEqual(
            inst.custom_base_attr,  # pylint: disable=all
            10)

        self.assertEqual(
            inst.custom_derived_attr,  # pylint: disable=all
            20
        )
        with self.assertRaises(AttributeError):
            _ = inst.base_attr
        with self.assertRaises(AttributeError):
            _ = inst.derived_attr

    def test_special_methods(self):
        class CustomClass(metaclass=CustomMeta):
            def __len__(self):
                return 5

            def __getitem__(self, item):
                return item * 2

        inst = CustomClass()
        self.assertEqual(len(inst), 5)
        self.assertEqual(inst.__getitem__(3), 6)
        with self.assertRaises(AttributeError):
            _ = inst.custom___len__  # pylint: disable=all
        with self.assertRaises(AttributeError):
            _ = inst.custom___getitem__  # pylint: disable=all

    def test_attribute_override(self):
        class CustomClass(metaclass=CustomMeta):
            x = 10

        inst = CustomClass()
        inst.x = 20  # this will set custom_x
        self.assertEqual(
            inst.custom_x,  # pylint: disable=all
            20
        )
        self.assertEqual(
            CustomClass.custom_x,  # pylint: disable=all
            10
        )

        with self.assertRaises(AttributeError):
            _ = inst.x


if __name__ == '__main__':
    unittest.main()
