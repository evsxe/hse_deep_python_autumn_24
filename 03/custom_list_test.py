import unittest

from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_init(self):
        custom_list = CustomList([1, 2, 3])
        self.assertEqual(custom_list, [1, 2, 3])

    def test_add_customlist(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        result = custom_list1 + custom_list2
        self.assertEqual(result, CustomList([5, 7, 9]))
        self.assertEqual(custom_list1, [1, 2, 3])
        self.assertEqual(custom_list2, [4, 5, 6])

    def test_add_list(self):
        custom_list = CustomList([1, 2, 3])
        list1 = [4, 5, 6]
        result = custom_list + list1
        self.assertEqual(result, CustomList([5, 7, 9]))
        self.assertEqual(custom_list, [1, 2, 3])
        self.assertEqual(list1, [4, 5, 6])

    def test_add_int(self):
        custom_list = CustomList([1, 2, 3])
        result = custom_list + 5
        self.assertEqual(result, CustomList([6, 7, 8]))
        self.assertEqual(custom_list, [1, 2, 3])

    def test_radd_customlist(self):
        custom_list = CustomList([1, 2, 3])
        list1 = [4, 5, 6]
        result = list1 + custom_list
        self.assertEqual(result, CustomList([5, 7, 9]))
        self.assertEqual(custom_list, [1, 2, 3])
        self.assertEqual(list1, [4, 5, 6])

    def test_radd_int(self):
        custom_list = CustomList([1, 2, 3])
        result = 5 + custom_list
        self.assertEqual(result, CustomList([6, 7, 8]))
        self.assertEqual(custom_list, [1, 2, 3])

    def test_sub_customlist(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        result = custom_list1 - custom_list2
        self.assertEqual(result, CustomList([-3, -3, -3]))
        self.assertEqual(custom_list1, [1, 2, 3])
        self.assertEqual(custom_list2, [4, 5, 6])

    def test_sub_list(self):
        custom_list = CustomList([1, 2, 3])
        list1 = [4, 5, 6]
        result = custom_list - list1
        self.assertEqual(result, CustomList([-3, -3, -3]))
        self.assertEqual(custom_list, [1, 2, 3])
        self.assertEqual(list1, [4, 5, 6])

    def test_sub_int(self):
        custom_list = CustomList([1, 2, 3])
        result = custom_list - 5
        self.assertEqual(result, CustomList([-4, -3, -2]))
        self.assertEqual(custom_list, [1, 2, 3])

    def test_rsub_customlist(self):
        custom_list = CustomList([1, 2, 3])
        list1 = [4, 5, 6]
        result = list1 - custom_list
        self.assertEqual(result, CustomList([3, 3, 3]))
        self.assertEqual(custom_list, [1, 2, 3])
        self.assertEqual(list1, [4, 5, 6])

    def test_rsub_int(self):
        custom_list = CustomList([1, 2, 3])
        result = 5 - custom_list
        self.assertEqual(result, CustomList([4, 3, 2]))
        self.assertEqual(custom_list, [1, 2, 3])

    def test_eq(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([1, 2, 3])
        self.assertTrue(custom_list1 == custom_list2)
        custom_list3 = CustomList([5, 1, 3, 7])
        custom_list4 = CustomList([1, 2, 7, 6])
        self.assertFalse(custom_list3 == custom_list4)

    def test_ne(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        self.assertTrue(custom_list1 != custom_list2)

    def test_lt(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        self.assertTrue(custom_list1 < custom_list2)

    def test_le(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        self.assertTrue(custom_list1 <= custom_list2)

    def test_gt(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        self.assertFalse(custom_list1 > custom_list2)

    def test_ge(self):
        custom_list1 = CustomList([1, 2, 3])
        custom_list2 = CustomList([4, 5, 6])
        self.assertFalse(custom_list1 >= custom_list2)

    def test_str(self):
        custom_list = CustomList([1, 2, 3])
        self.assertEqual(str(custom_list),
                         "CustomList([1, 2, 3]), сумма элементов: 6")

    def test_comparison_different_types(self):
        custom_list = CustomList([1, 2, 3])
        for other in ["test", (1, 2, 3), {1, 2, 3}, 5.0]:
            self.assertFalse(custom_list == other)
            self.assertTrue(custom_list != other)
            self.assertFalse(custom_list < other)
            self.assertFalse(custom_list <= other)
            self.assertFalse(custom_list > other)
            self.assertFalse(custom_list >= other)

    def test_add_different_lengths(self):
        custom_list1 = CustomList([1, 2])
        custom_list2 = CustomList([3, 4, 5])
        result = custom_list1 + custom_list2
        self.assertEqual(result, CustomList([4, 6, 5]))

        custom_list3 = CustomList([1, 2, 3])
        custom_list4 = CustomList([4])
        result = custom_list3 + custom_list4
        self.assertEqual(result, CustomList([5, 2, 3]))

    def test_sub_different_lengths(self):
        custom_list1 = CustomList([1, 2])
        custom_list2 = CustomList([3, 4, 5])
        result = custom_list1 - custom_list2
        self.assertEqual(result, CustomList([-2, -2, -5]))

        custom_list3 = CustomList([1, 2, 3])
        custom_list4 = CustomList([4])
        result = custom_list3 - custom_list4
        self.assertEqual(result, CustomList([-3, 2, 3]))


if __name__ == '__main__':
    unittest.main()
