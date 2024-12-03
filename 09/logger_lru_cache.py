import logging
import argparse
import sys


class Node:  # pylint: disable=all
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    def __init__(self, limit=42):
        self.limit = limit
        self.cache = {}
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def _remove(node):
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node):
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def get(self, key):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            self.logger.debug(f"Get existing key: {key}, value: {node.value}")
            return node.value
        self.logger.debug(f"Get non-existing key: {key}")
        return None

    def set(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            self._remove(node)
            node.value = value
            self._add_to_head(node)
            self.logger.debug(f"Set existing key: {key}, new value: {value}")
        else:
            if len(self.cache) >= self.limit:
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]
                self.logger.debug(
                    f"Cache full, evicting LRU key: {lru_node.key}")
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)
            self.logger.debug(f"Set new key: {key}, value: {value}")


def custom_filter(record):
    message = record.getMessage()
    words = message.split()
    return len(words) % 2 != 0


def main():
    parser = argparse.ArgumentParser(
        description='LRU Cache with logging'
    )

    parser.add_argument(
        '-s',
        '--stdout',
        action='store_true',
        help='Log to stdout'
    )

    parser.add_argument(
        '-f',
        '--filter',
        action='store_true',
        help='Apply custom filter'
    )

    args = parser.parse_args()

    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(
        filename='cache.log',
        level=logging.DEBUG,
        format=log_format
    )

    if args.filter:
        logging.getLogger().addFilter(logging.Filter())
        logging.getLogger().addFilter(logging.Filter())
        logging.getLogger().addFilter(lambda record: custom_filter(record))

    if args.stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(logging.Formatter('%(message)s'))
        logging.getLogger().addHandler(stdout_handler)

    cache = LRUCache(limit=2)

    cache.set('a', 1)
    cache.set('b', 2)
    print(cache.get('a'))  # 1
    cache.set('c', 3)
    print(cache.get('b'))  # None
    cache.set('a', 4)
    print(cache.get('a'))  # 4
    print(cache.get('d'))  # None


if __name__ == "__main__":
    main()
