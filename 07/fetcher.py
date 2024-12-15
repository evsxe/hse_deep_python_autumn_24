import asyncio
import argparse
import aiohttp


class URLFetcher:
    def __init__(self, max_concurrent_requests: int, timeout: int):
        """Initializes the URLFetcher with concurrency limits and timeout."""
        self.max_concurrent_requests = max_concurrent_requests
        self.semaphore = asyncio.Semaphore(max_concurrent_requests)
        self.timeout = timeout

    async def fetch_url(self, session: aiohttp.ClientSession, url: str) -> None:
        """Fetches a single URL using the provided session."""
        async with self.semaphore:
            try:
                async with session.get(url, timeout=self.timeout) as response:
                    content_length = len(await response.text())
                    print(f"Fetched {url} with status"
                          f" {response.status} and length {content_length}")

            except aiohttp.ClientConnectionError as e:
                print(f"Connection error for {url}: {e}")

            except asyncio.TimeoutError:
                print(f"Timeout error for {url}")

            # Handle other HTTP errors
            except aiohttp.ClientResponseError as e:
                print(f"HTTP error for {url}: {e}")

    async def fetch_all_urls(self, urls: list) -> None:
        """Fetches all URLs concurrently."""
        # Timeout is handled per request now.
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch_url(session, url) for url in urls]
            await asyncio.gather(*tasks)


def main():
    """Parses command-line arguments and runs the URL fetcher."""
    parser = argparse.ArgumentParser(
        description="Asynchronous URL fetching."
    )

    parser.add_argument(
        "-c",
        "--concurrent",
        type=int,
        default=10,
        help="Number of concurrent requests (default: 10)."
    )

    parser.add_argument(
        "url_file",
        type=str,
        help="Path to the file containing URLs."
    )

    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=5,
        help="Timeout for each request in seconds (default: 5)"
    )

    args = parser.parse_args()

    try:
        with open(args.url_file, "r", encoding='utf-8') as f:
            urls = f.readlines()
    except FileNotFoundError:
        print(f"Error: File '{args.url_file}' not found.")
        return

    fetcher = URLFetcher(args.max_concurrent_requests, args.timeout)
    asyncio.run(fetcher.fetch_all_urls(urls))


if __name__ == "__main__":
    main()
