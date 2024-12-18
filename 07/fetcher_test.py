import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp

from fetcher import URLFetcher, main


class TestURLFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = URLFetcher(concurrency=5, timeout=2)

    @patch('aiohttp.ClientSession')
    async def test_fetch_success(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Hello, World!')

        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch(mock_session, mock_url)

        mock_print.assert_called_with(
            f"Fetched {mock_url} with status 200 and length 13")

    @patch('aiohttp.ClientSession')
    async def test_fetch_connection_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_session.return_value.__aenter__.side_effect = \
            aiohttp.ClientConnectionError

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch(mock_session, mock_url)

        mock_print.assert_called_with(f"Connection error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_timeout_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(side_effect=asyncio.TimeoutError)

        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch(mock_session, mock_url)

        mock_print.assert_called_with(f"Timeout error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_success(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(status=200, text=AsyncMock(return_value='Response 2'))
        ]

        mock_session.return_value.__aenter__.side_effect = mock_responses

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url_1, mock_url_2])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10")
        mock_print.assert_any_call(
            f"Fetched {mock_url_2} with status 200 and length 10")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_partial_failure(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'

        mock_response_1 = AsyncMock(
            status=200, text=AsyncMock(
                return_value='Response 1'))
        mock_response_2 = AsyncMock(side_effect=aiohttp.ClientConnectionError)

        mock_session.return_value.__aenter__.side_effect = [
            mock_response_1, mock_response_2]

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url_1, mock_url_2])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10")

        mock_print.assert_any_call(f"Connection error for {mock_url_2}")

    @patch('builtins.open',
           new_callable=unittest.mock.mock_open,
           read_data='https://example.com\nhttps://google.com')
    @patch('asyncio.run')
    def test_main(self, mock_run, mock_open):
        URLFetcher.fetch_all = AsyncMock()

        main(concurrency=2, timeout=5, file_name='test_urls.txt')
        mock_run.assert_called_once()
        mock_open.assert_called_once_with('test_urls.txt', 'r',
                                          encoding='utf-8')
        self.assertEqual(len(mock_open().readlines()),
                         2)  # Check that file was read

    @patch('builtins.open',
           new_callable=unittest.mock.mock_open,
           read_data='')
    @patch('asyncio.run')
    def test_main_empty_file(self, mock_run, mock_open):
        URLFetcher.fetch_all = AsyncMock()

        main(concurrency=2, timeout=5, file_name='empty.txt')
        mock_run.assert_called_once()
        mock_open.assert_called_once()


if __name__ == '__main__':
    unittest.main()
