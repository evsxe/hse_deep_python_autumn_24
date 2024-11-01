import unittest
from unittest.mock import patch, MagicMock
from requests import RequestException
from client import RequestThread
from server import Worker, Master


class ClientServerTest(unittest.TestCase):
    def test_worker_process_url_request_error(self):
        url = 'https://www.example.com'
        with patch('requests.get', side_effect=RequestException):
            worker = Worker(None, None)
            top_words = worker.process_url(url)
            self.assertEqual(top_words, {})

    def test_master_init_workers(self):
        master = Master(8080, 3, 2)
        self.assertEqual(len(master.workers), 3)


if __name__ == '__main__':
    unittest.main()
