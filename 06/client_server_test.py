import json
import queue
import unittest
from unittest.mock import MagicMock, patch

import requests
from server import Worker, Master
from client import RequestThread


class TestWorker(unittest.TestCase):

    def test_process_url_error(self):
        worker = Worker(None, None, 7)
        url = "https://www.invalid-url.com"
        with patch('requests.get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException(
                "Connection error")
            top_words = worker.process_url(url)
            self.assertEqual(top_words, {})


class TestMaster(unittest.TestCase):

    def test_handle_client_valid_url(self):
        master = Master(8080, 2, 7)
        conn = MagicMock()
        url = "https://www.example.com"
        conn.recv.return_value = url.encode()
        master.task_queue = queue.Queue()
        master.result_queue = queue.Queue()
        master.result_queue.put((url, {'word1': 10, 'word2': 5}))
        master.handle_client(conn)
        conn.sendall.assert_called_once_with(
            json.dumps({'word1': 10, 'word2': 5}).encode())

    def test_handle_client_invalid_url(self):
        master = Master(8080, 2, 7)
        conn = MagicMock()
        url = "invalid_url"
        conn.recv.return_value = url.encode()
        master.handle_client(conn)
        conn.sendall.assert_called_once_with("Incorrect URL".encode('utf-8'))


if __name__ == "__main__":
    unittest.main()
