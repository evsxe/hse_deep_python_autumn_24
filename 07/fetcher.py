import argparse

import asyncio
import logging
import aiohttp


async def fetch_url(session, url):
    try:
        async with session.get(url) as response:
            status = response.status
            content = await response.text()
            return status, content
    except aiohttp.ClientError as e:
        logging.error(f"Error fetching {url}: {e}")  # pylint: disable=all
        return None, None


async def fetch_urls(urls, concurrent_requests):
    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(concurrent_requests)
        tasks = [
            asyncio.ensure_future(fetch_one_url(session, url, semaphore))
            for url in urls
        ]
        results = await asyncio.gather(*tasks)
        return results


async def fetch_one_url(session, url, semaphore):
    async with semaphore:
        url = url.strip()
        if url:
            return await fetch_url(session, url)


def main():
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
    args = parser.parse_args()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    try:
        with open(args.url_file, "r", encoding='utf-8') as f:
            urls = f.readlines()
    except FileNotFoundError:
        logging.error(f"File {args.url_file} not found.")  # pylint: disable=all
        return

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    results = loop.run_until_complete(
        fetch_urls(urls, args.concurrent)
    )
    loop.close()

    for i, (status, _) in enumerate(results):
        if status:
            print(f"URL: {urls[i].strip()}")
            print(f"Status: {status}")
            print("---")


if __name__ == "__main__":
    main()
