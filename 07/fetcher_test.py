import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp

from fetcher import URLFetcher, main


class TestURLFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = URLFetcher(max_concurrent_requests=5, timeout=2)

    @patch('aiohttp.ClientSession')
    async def test_fetch_url_success(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Hello, World!')
        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(
            f"Fetched {mock_url} with status 200 and length 13"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_url_connection_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_session.return_value.__aenter__.side_effect = (
            aiohttp.ClientConnectionError
        )

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(
            f"Connection error for {mock_url}"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_url_timeout_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_session.return_value.__aenter__.side_effect = asyncio.TimeoutError

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(f"Timeout error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_url_http_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Not Found')
        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(
            f"HTTP error for {mock_url}: 404 ClientResponseError: 404 Not Found"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_url_empty_url(self, mock_session):
        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, "")
        mock_print.assert_called_once()
        self.assertTrue(
            "Connection error for :" in mock_print.call_args.args[0]
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_urls_success(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(status=200, text=AsyncMock(return_value='Response 2'))
        ]
        mock_session.return_value.__aenter__.side_effect = mock_responses

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls([mock_url_1, mock_url_2])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10"
        )
        mock_print.assert_any_call(
            f"Fetched {mock_url_2} with status 200 and length 10"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_urls_multiple_failures(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_url_3 = 'https://example.com/3'

        mock_response_1 = AsyncMock(status=200,
                                    text=AsyncMock(return_value='Response 1'))
        mock_response_2 = AsyncMock(side_effect=aiohttp.ClientConnectionError)
        mock_response_3 = AsyncMock(side_effect=asyncio.TimeoutError)

        mock_session.return_value.__aenter__.side_effect = [mock_response_1,
                                                            mock_response_2,
                                                            mock_response_3]

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls(
                [mock_url_1, mock_url_2, mock_url_3])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10")
        mock_print.assert_any_call(
            f"Connection error for {mock_url_2}: ClientConnectionError()")
        mock_print.assert_any_call(f"Timeout error for {mock_url_3}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_urls_empty_list(self):
        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls([])
        mock_print.assert_not_called()

    @patch('aiohttp.ClientSession')
    async def test_semaphore_limit(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock(status=200, text=AsyncMock(return_value=''))
        mock_session.return_value.__aenter__.return_value = mock_response

        self.assertEqual(self.fetcher.semaphore._value,
                         5)  # pylint: disable=all

        await asyncio.gather(
            *[self.fetcher.fetch_url(mock_session, mock_url) for _ in range(6)]
        )

        self.assertEqual(self.fetcher.semaphore._value,
                         5)  # pylint: disable=all

    @patch('builtins.open', side_effect=FileNotFoundError)
    def test_main_file_not_found(self, mock_open):
        with patch('sys.argv', ['fetcher.py', 'nonexistent_file.txt']):
            with patch('builtins.print') as mock_print:
                main()  # pylint: disable=undefined-variable
        mock_open.assert_called_once()
        mock_print.assert_called_once_with(
            "Error: File 'nonexistent_file.txt' not found."
        )

    def test_main_invalid_args(self):
        with patch('sys.argv', ['fetcher.py', '-c', 'abc']):
            with self.assertRaises(SystemExit):
                main()  # pylint: disable=undefined-variable

        with patch('sys.argv', ['fetcher.py']):
            with self.assertRaises(SystemExit):
                main()  # pylint: disable=undefined-variable

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_urls_mixed_results(self, mock_session):
        urls = ['https://example.com/1',
                'https://example.com/2',
                'https://example.com/3']

        responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(side_effect=aiohttp.ClientConnectionError),
            AsyncMock(status=404, text=AsyncMock(return_value='Not Found'))
        ]

        mock_session.return_value.__aenter__.side_effect = responses

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls(urls)

        mock_print.assert_any_call(
            "Fetched https://example.com/1 with status 200 and length 10"
        )
        mock_print.assert_any_call(
            "Connection error for https://example.com/2:"
            " ClientConnectionError()"
        )
        mock_print.assert_any_call(
            "HTTP error for https://example.com/3:"
            " 404 ClientResponseError: 404 Not Found"
        )


if __name__ == '__main__':
    unittest.main()
