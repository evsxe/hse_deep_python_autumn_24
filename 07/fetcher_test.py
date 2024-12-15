import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp
from fetcher import URLFetcher


class TestURLFetcher(unittest.TestCase):

    def setUp(self):
        self.fetcher = URLFetcher(max_concurrent_requests=5, timeout=2)

    @patch('aiohttp.ClientSession')
    async def test_fetch_success(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Hello, World!')
        mock_response.__aexit__.return_value = None
        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(
            f"Fetched {mock_url} with status 200 and length 13")

    @patch('aiohttp.ClientSession')
    async def test_fetch_connection_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_session.return_value.__aenter__.side_effect = \
            aiohttp.ClientConnectionError

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(f"Connection error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_timeout_error(self, mock_session):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.text = AsyncMock(side_effect=asyncio.TimeoutError)
        mock_response.__aexit__.return_value = None
        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_url(mock_session, mock_url)

        mock_print.assert_called_once_with(f"Timeout error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_success(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_responses = [
            AsyncMock(status=200,
                      text=AsyncMock(return_value='Response 1'),
                      __aexit__=AsyncMock(return_value=None)),

            AsyncMock(status=200,
                      text=AsyncMock(return_value='Response 2'),
                      __aexit__=AsyncMock(return_value=None))
        ]

        mock_session.return_value.__aenter__.side_effect = mock_responses
        mock_session.return_value.__aexit__.return_value = None

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls([mock_url_1, mock_url_2])

        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10")
        mock_print.assert_any_call(
            f"Fetched {mock_url_2} with status 200 and length 10")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_partial_failure(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'

        mock_response_1 = AsyncMock(
            status=200,
            text=AsyncMock(return_value='Response 1'),
            __aexit__=AsyncMock(return_value=None)
        )
        mock_response_2 = AsyncMock(
            side_effect=aiohttp.ClientConnectionError,
            __aexit__=AsyncMock(return_value=None)
        )

        mock_session.return_value.__aenter__.side_effect = [
            mock_response_1, mock_response_2]
        mock_session.return_value.__aexit__.return_value = None

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all_urls([mock_url_1, mock_url_2])

        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10")
        mock_print.assert_any_call(f"Connection error for {mock_url_2}")


if __name__ == '__main__':
    unittest.main()
