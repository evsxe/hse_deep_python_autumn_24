import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp
from fetcher import URLFetcher


class TestURLFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = URLFetcher(
            max_concurrent_requests=5,
            timeout=2
        )

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

        mock_response_1 = AsyncMock(
            status=200,
            text=AsyncMock(return_value='Response 1')
        )

        mock_response_2 = AsyncMock(
            side_effect=aiohttp.ClientConnectionError
        )

        mock_response_3 = AsyncMock(
            side_effect=asyncio.TimeoutError
        )

        mock_session.return_value.__aenter__.side_effect = [
            mock_response_1, mock_response_2, mock_response_3
        ]

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls(
                [mock_url_1, mock_url_2, mock_url_3]
            )

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10"
        )

        mock_print.assert_any_call(
            f"Connection error for {mock_url_2}"
        )

        mock_print.assert_any_call(
            f"Timeout error for {mock_url_3}"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_urls_empty_list(self):
        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls([])
        mock_print.assert_not_called()


if __name__ == '__main__':
    unittest.main()
