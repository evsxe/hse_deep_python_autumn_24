import asyncio
import argparse
import aiohttp

TIMEOUT = 5


class URLFetcher:
    def __init__(self, concurrency: int, timeout: int):
        self.concurrency = concurrency
        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout = timeout

    async def fetch(self, session: aiohttp.ClientSession, url: str) -> None:
        async with self.semaphore:
            try:
                async with session.get(url) as response:
                    content = await response.text()
                    print(
                        f"Fetched {url} with status \
                        {response.status} and length \
                          {len(content)}"
                    )
            except aiohttp.ClientConnectionError:
                print(f"Connection error for {url}")
            except asyncio.TimeoutError:
                print(f"Timeout error for {url}")

    async def fetch_all(self, urls: list):
        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            tasks = [self.fetch(session, url) for url in urls]
            await asyncio.gather(*tasks)


def main(concurrency: int, timeout: int, file_name: str):
    with open(file_name, 'r', encoding='utf-8') as f:
        urls = [line.strip() for line in f if line.strip()]

    fetcher = URLFetcher(concurrency, timeout)
    asyncio.run(fetcher.fetch_all(urls))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'concurrency',
        type=int
    )
    parser.add_argument('file', type=str)

    args = parser.parse_args()
    main(args.concurrency, TIMEOUT, args.file)
