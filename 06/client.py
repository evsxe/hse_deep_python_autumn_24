import sys
import socket
import threading
from urllib.parse import urlparse


# Start: python client.py 10 urls.txt

class RequestThread(threading.Thread):
    def __init__(self, url, result):
        super().__init__()
        self.url = url
        self.result = result

    def run(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(5)
                sock.connect(('127.0.0.1', 8080))
                sock.sendall(self.url.encode())
                data = sock.recv(4096)
                self.result[self.url] = data.decode()
        except (ConnectionRefusedError, TimeoutError, OSError) as e:
            print(f"Error connecting to {self.url}: {e}")
        except Exception as e:
            print(f"Invalid URL: {self.url}: {e}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python client.py select count urls.txt")
        return

    num_threads = int(sys.argv[1])
    url_file = sys.argv[2]

    with open(url_file, encoding='utf-8') as f:
        urls = [line.strip() for line in f.readlines()]

    threads = []
    results = {}

    for url in urls:
        if urlparse(url).scheme in ['http', 'https']:
            if len(threads) >= num_threads:
                for thread in threads:
                    thread.join()
                threads = []

            thread = RequestThread(url, results)
            thread.start()
            threads.append(thread)
        else:
            print(f"Некорректный URL: {url}")

    for thread in threads:
        thread.join()

    for url, response in results.items():
        print(f"{url}: {response}")


if __name__ == '__main__':
    main()
