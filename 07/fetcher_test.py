import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp
from fetcher import URLFetcher


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
        mock_response.content_length = 13

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
        mock_session.return_value.__aenter__.side_effect = asyncio.TimeoutError

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch(mock_session, mock_url)

        mock_print.assert_called_once_with(f"Timeout error for {mock_url}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_success(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_responses = [
            AsyncMock(status=200,
                      text=AsyncMock(return_value='Response 1'),
                      content_length=10),
            AsyncMock(status=200,
                      text=AsyncMock(return_value='Response 2'),
                      content_length=10)
        ]

        mock_session.return_value.__aenter__.side_effect = mock_responses

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url_1, mock_url_2])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10"
        )

        mock_print.assert_any_call(
            f"Fetched {mock_url_2} with status 200 and length 10"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_partial_failure(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'

        mock_response_1 = AsyncMock(status=200,
                                    text=AsyncMock(return_value='Response 1'),
                                    content_length=10)

        mock_response_2 = AsyncMock(side_effect=aiohttp.ClientConnectionError)

        mock_session.return_value.__aenter__.side_effect = [mock_response_1,
                                                            mock_response_2]

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url_1, mock_url_2])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10"
        )

        mock_print.assert_any_call(f"Connection error for {mock_url_2}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_empty_urls(self):
        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([])
        mock_print.assert_not_called()

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_mixed_errors(self, mock_session):
        mock_url_1 = 'https://example.com/1'
        mock_url_2 = 'https://example.com/2'
        mock_url_3 = 'https://example.com/3'

        mock_response_1 = AsyncMock(status=200,
                                    text=AsyncMock(return_value='Response 1'),
                                    content_length=10)

        mock_response_2 = AsyncMock(side_effect=aiohttp.ClientConnectionError)
        mock_response_3 = AsyncMock(side_effect=asyncio.TimeoutError)

        mock_session.return_value.__aenter__.side_effect = [mock_response_1,
                                                            mock_response_2,
                                                            mock_response_3]

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url_1, mock_url_2, mock_url_3])

        mock_print.assert_any_call(
            f"Fetched {mock_url_1} with status 200 and length 10"
        )
        mock_print.assert_any_call(f"Connection error for {mock_url_2}")
        mock_print.assert_any_call(f"Timeout error for {mock_url_3}")

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_non_200_status(self, mock_session):
        mock_url = "https://example.com"
        mock_response = AsyncMock(status=404,
                                  text=AsyncMock(return_value="Not Found"),
                                  content_length=10)
        mock_session.return_value.__aenter__.return_value = mock_response

        with patch('builtins.print') as mock_print:
            await self.fetcher.fetch_all([mock_url])

        mock_print.assert_any_call(
            f"Fetched {mock_url} with status 404 and length 10"
        )

    @patch('aiohttp.ClientSession')
    async def test_fetch_all_with_different_timeouts(self, mock_session):
        fetcher1 = URLFetcher(concurrency=5, timeout=1)
        fetcher2 = URLFetcher(concurrency=5, timeout=10)

        mock_response_short = AsyncMock(status=200, text=AsyncMock(
            return_value="Response Short"), content_length=10)
        mock_response_long = AsyncMock(status=200, text=AsyncMock(
            return_value="Response Long"), content_length=10)

        mock_session.return_value.__aenter__.side_effect = [mock_response_short,
                                                            mock_response_long]

        with patch('builtins.print'):
            await fetcher1.fetch_all(
                ["https://example.com/1", "https://example.com/2"])
            await fetcher2.fetch_all(
                ["https://example.com/1", "https://example.com/2"])


if __name__ == '__main__':
    unittest.main()
