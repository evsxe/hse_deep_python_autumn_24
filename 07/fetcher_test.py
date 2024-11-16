import unittest
from unittest.mock import patch, AsyncMock

from fetcher import fetch_urls, fetch_url


class TestFetcher(unittest.IsolatedAsyncioTestCase):

    @patch('fetcher.aiohttp')
    async def test_fetch_url_client_error(self, mock_aiohttp):
        mock_session = AsyncMock()
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_response.text = AsyncMock(return_value="Error text")
        mock_session.get = AsyncMock(return_value=mock_response)
        mock_aiohttp.ClientSession = AsyncMock(return_value=mock_session)
        mock_aiohttp.ClientError = Exception

        with patch('fetcher.logging.error') as mock_log:
            status, content = await fetch_url(mock_session, "bad_url")
            self.assertIsNone(status)
            self.assertIsNone(content)
            mock_log.assert_called_once()

    @patch('fetcher.fetch_url')
    async def test_fetch_urls_success(self, mock_fetch_url):
        mock_fetch_url.side_effect = [
            (200, "Content 1"), (201, "Content 2"), (404, "Content 3")
        ]
        urls = ["url1", "url2", "url3"]
        results = await fetch_urls(urls, concurrent_requests=2)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], (200, "Content 1"))
        self.assertEqual(results[1], (201, "Content 2"))
        self.assertEqual(results[2], (404, "Content 3"))

    @patch('fetcher.fetch_url')
    async def test_fetch_urls_empty_url(self, mock_fetch_url):
        mock_fetch_url.return_value = (200, "Content")
        urls = ["url1", "", "url3"]
        results = await fetch_urls(urls, concurrent_requests=2)
        self.assertEqual(len(results), 3)
        self.assertIsNone(results[1])

    @patch('fetcher.fetch_url')
    async def test_fetch_urls_all_failures(self, mock_fetch_url):
        mock_fetch_url.return_value = (None, None)
        urls = ["url1", "url2", "url3"]
        results = await fetch_urls(urls, concurrent_requests=2)
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0], (None, None))
        self.assertEqual(results[1], (None, None))
        self.assertEqual(results[2], (None, None))

    @patch('fetcher.aiohttp')
    async def test_fetch_urls_aiohttp_exception(self, mock_aiohttp):
        mock_aiohttp.ClientSession.side_effect = Exception
        urls = ["url1", "url2"]
        with self.assertRaises(Exception):
            await fetch_urls(urls, concurrent_requests=2)


if __name__ == '__main__':
    unittest.main()
