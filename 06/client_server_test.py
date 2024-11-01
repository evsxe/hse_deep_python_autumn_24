import unittest

from unittest.mock import patch, MagicMock
from requests import RequestException
from client import RequestThread
from server import Worker, Master


class ClientServerTest(unittest.TestCase):

    def test_request_thread_success(self):
        url = 'https://www.example.com'
        result = {}
        thread = RequestThread(url, result)
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.return_value = None
            mock_socket.return_value.sendall.return_value = None
            mock_socket.return_value.recv.return_value = (b'{"word1": 1,'
                                                          b' "word2": 2}')
            thread.run()
            self.assertEqual(result[url], '{"word1": 1, "word2": 2}')

    def test_request_thread_connection_error(self):
        url = 'https://www.example.com'
        result = {}
        thread = RequestThread(url, result)
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.connect.side_effect = (
                ConnectionRefusedError
            )
            thread.run()
            self.assertNotIn(url, result)

    def test_worker_process_url_success(self):
        url = 'https://www.example.com'
        with patch('requests.get') as mock_get:
            mock_get.return_value.text = 'This is a test. Test words.'
            worker = Worker(None, None)
            top_words = worker.process_url(url)
            self.assertEqual(top_words,
                             {'test': 2,
                              'is': 1,
                              'a': 1,
                              'This': 1,
                              'words': 1})

    def test_worker_process_url_request_error(self):
        url = 'https://www.example.com'
        with patch('requests.get') as mock_get:
            mock_get.side_effect = RequestException
            worker = Worker(None, None)
            top_words = worker.process_url(url)
            self.assertEqual(top_words, {})

    def test_master_handle_client_success(self):
        url = 'https://www.example.com'
        with patch('socket.socket') as mock_socket, \
                patch('queue.Queue') as mock_queue:
            mock_socket.return_value.accept.return_value = (
                MagicMock(), ('127.0.0.1', 12345))
            mock_socket.return_value.recv.return_value = url.encode()
            mock_queue.return_value.put.return_value = None
            mock_queue.return_value.get.return_value = (
                url, {'word1': 1, 'word2': 2})
            master = Master(8080, 1, 2)
            master.handle_client(MagicMock())
            self.assertEqual(master.active_requests, 1)

    def test_master_handle_client_incorrect_url(self):
        url = 'file://example.com'
        with patch('socket.socket') as mock_socket:
            mock_socket.return_value.accept.return_value = (
                MagicMock(), ('127.0.0.1', 12345))
            mock_socket.return_value.recv.return_value = url.encode()
            master = Master(8080, 1, 2)
            master.handle_client(MagicMock())
            self.assertEqual(master.active_requests, 0)

    def test_master_start_thread_success(self):
        with patch('socket.socket') as mock_socket, \
                patch('queue.Queue') as mock_queue, \
                patch('threading.Thread') as mock_thread:
            mock_socket.return_value.accept.return_value = (
                MagicMock(),
                ('127.0.0.1', 12345)
            )
            mock_socket.return_value.recv.return_value = (
                'https://www.example.com'.encode()
            )
            mock_queue.return_value.put.return_value = None
            mock_queue.return_value.get.return_value = (
                'https://www.example.com', {'word1': 1, 'word2': 2})
            mock_thread.return_value.start.return_value = None
            master = Master(8080, 1, 2)
            master.start()
            self.assertEqual(master.active_requests, 1)

    @patch('server.Worker')
    def test_master_init_workers(self, mock_worker):
        master = Master(8080, 3, 2)
        mock_worker.assert_called_with(master.task_queue, master.result_queue)
        self.assertEqual(len(master.workers), 3)


if __name__ == '__main__':
    unittest.main()
