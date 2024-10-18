import unittest
from lru_cache import LRUCache


class TestLRUCache(unittest.TestCase):
    def setUp(self):
        self.cache = LRUCache(2)

    def test_basic_operations(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")

        self.assertIsNone(self.cache.get("k3"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k1"), "val1")

        self.cache.set("k3", "val3")

        self.assertEqual(self.cache.get("k3"), "val3")
        self.assertIsNone(self.cache.get("k2"))
        self.assertEqual(self.cache.get("k1"), "val1")

    def test_eviction_policy(self):
        self.cache.set("k1", "val1")
        self.cache.set("k2", "val2")
        self.cache.set("k3", "val3")

        self.assertIsNone(self.cache.get("k1"))
        self.assertEqual(self.cache.get("k2"), "val2")
        self.assertEqual(self.cache.get("k3"), "val3")

    def test_update_value(self):
        self.cache.set("k1", "val1")
        self.cache.set("k1", "val1_updated")

        self.assertEqual(self.cache.get("k1"), "val1_updated")


if __name__ == '__main__':
    unittest.main()
