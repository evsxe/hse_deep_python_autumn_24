import asyncio
import unittest
from unittest.mock import patch, AsyncMock
import aiohttp
import sys

from fetcher import URLFetcher, main


class TestURLFetcher(unittest.TestCase):
    def setUp(self):
        self.fetcher = URLFetcher(max_concurrent_requests=5, timeout=2)

    async def test_fetch_url_success(self):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Hello, World!')

        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                await self.fetcher.fetch_url(session, mock_url)

            mock_print.assert_called_once_with(
                f"Fetched {mock_url} with status 200 and length 13"
            )

    async def test_fetch_url_connection_error(self):
        mock_url = 'https://example.com'
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                with patch.object(session, 'get',
                                  side_effect=aiohttp.ClientConnectionError):
                    await self.fetcher.fetch_url(session, mock_url)

            mock_print.assert_called_once_with(
                f"Connection error for {mock_url}: ClientConnectionError()"
            )

    async def test_fetch_url_timeout_error(self):
        mock_url = 'https://example.com'
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                with patch.object(session, 'get',
                                  side_effect=asyncio.TimeoutError):
                    await self.fetcher.fetch_url(session, mock_url)
            mock_print.assert_called_once_with(f"Timeout error for {mock_url}")

    async def test_fetch_url_http_error(self):
        mock_url = 'https://example.com'
        mock_response = AsyncMock()
        mock_response.status = 404
        mock_response.text.return_value = asyncio.Future()
        mock_response.text.return_value.set_result('Not Found')

        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                with patch.object(session,
                                  'get',
                                  return_value=mock_response):
                    await self.fetcher.fetch_url(session, mock_url)

        mock_print.assert_called_once_with(
            f"HTTP error for {mock_url}: 404 ClientResponseError: 404 Not Found"
        )

    async def test_fetch_url_empty_url(self):
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                await self.fetcher.fetch_url(session, "")
            mock_print.assert_called_once()
            self.assertTrue(
                "Connection error for :" in mock_print.call_args.args[0]
            )

    async def test_fetch_url_invalid_url(self):
        mock_url = "invalid-url"  # Not a valid URL
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                await self.fetcher.fetch_url(session, mock_url)
            self.assertTrue(
                "Connection error for " in mock_print.call_args[0][0])

    async def test_fetch_all_urls_success(self):
        urls = ['https://example.com/1', 'https://example.com/2']
        mock_responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(status=200, text=AsyncMock(return_value='Response 2'))
        ]

        async with aiohttp.ClientSession() as session:
            with patch.object(session,
                              'get',
                              side_effect=mock_responses):

                with patch('builtins.print') as mock_print:
                    await self.fetcher.fetch_all_urls(urls)

                self.assertEqual(mock_print.call_count,
                                 2)  # Check for both calls
                mock_print.assert_any_call(
                    f"Fetched {urls[0]} with status 200 and length 10"
                )
                mock_print.assert_any_call(
                    f"Fetched {urls[1]} with status 200 and length 10"
                )

    async def test_fetch_all_urls_multiple_failures(self):
        urls = ['https://example.com/1',
                'https://example.com/2',
                'https://example.com/3']

        responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(side_effect=aiohttp.ClientConnectionError),
            AsyncMock(side_effect=asyncio.TimeoutError),
        ]

        async with aiohttp.ClientSession() as session:
            with patch.object(session, 'get', side_effect=responses):
                with patch('builtins.print') as mock_print:
                    await self.fetcher.fetch_all_urls(urls)

                mock_print.assert_any_call(
                    f"Fetched {urls[0]} with status 200 and length 10"
                )

                mock_print.assert_any_call(
                    f"Connection error for {urls[1]}: ClientConnectionError()"
                )

                mock_print.assert_any_call(
                    f"Timeout error for {urls[2]}")

    async def test_fetch_all_urls_empty_list(self):
        async with aiohttp.ClientSession():
            with patch('builtins.print') as mock_print:
                await self.fetcher.fetch_all_urls([])
            mock_print.assert_not_called()

    async def test_semaphore_limit(self):
        async with aiohttp.ClientSession() as session:
            mock_url = 'https://example.com'
            mock_response = AsyncMock(status=200,
                                      text=AsyncMock(return_value=''))

            with patch.object(session,
                              'get',
                              return_value=mock_response):

                self.assertEqual(self.fetcher.semaphore._value, 5)
                await asyncio.gather(
                    *[self.fetcher.fetch_url(session, mock_url) for _ in
                      range(6)]
                )
                self.assertEqual(self.fetcher.semaphore._value, 5)

    def test_main_invalid_args(self):
        with patch('sys.argv', ['fetcher.py', '-c', 'abc']):
            with self.assertRaises(SystemExit):
                main()

        with patch('sys.argv', ['fetcher.py']):
            with self.assertRaises(SystemExit):
                main()

    async def test_fetch_all_urls_mixed_results(self):
        urls = ['https://example.com/1',
                'https://example.com/2',
                'https://example.com/3']

        responses = [
            AsyncMock(status=200, text=AsyncMock(return_value='Response 1')),
            AsyncMock(side_effect=aiohttp.ClientConnectionError),
            AsyncMock(status=404, text=AsyncMock(return_value='Not Found'))
        ]

        async with aiohttp.ClientSession() as session:
            with patch.object(session, 'get', side_effect=responses):
                with patch('builtins.print') as mock_print:
                    await self.fetcher.fetch_all_urls(urls)

                mock_print.assert_any_call(
                    f"Fetched {urls[0]} with status 200 and length 10"
                )
                mock_print.assert_any_call(
                    f"Connection error for {urls[1]}: ClientConnectionError()"
                )
                mock_print.assert_any_call(
                    f"HTTP error for {urls[3]}:"
                    f" 404 ClientResponseError: 404 Not Found"
                )

    async def test_fetch_all_urls_large_number_of_urls(self):
        urls = ['https://example.com/' + str(i) for i in range(100)]
        async with aiohttp.ClientSession() as session:
            with patch.object(
                    session,
                    'get',
                    return_value=AsyncMock(status=200,
                                           text=AsyncMock(return_value=''))):

                with patch('builtins.print') as mock_print:
                    await self.fetcher.fetch_all_urls(urls)
                self.assertEqual(mock_print.call_count, 100)


if __name__ == '__main__':
    unittest.main()
