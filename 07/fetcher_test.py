import unittest

from unittest.mock import patch

from fetcher import fetch_urls


class TestFetcher(unittest.IsolatedAsyncioTestCase):

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
        self.assertEqual(results[1], (None, None))


if __name__ == '__main__':
    unittest.main()
