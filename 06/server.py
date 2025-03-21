import json
import queue
import socket
import threading
from collections import Counter
from urllib.parse import urlparse
import requests


# Start: python server.py -w 10 -k 7

class Worker(threading.Thread):
    def __init__(self, task_queue, result_queue, top_k):
        super().__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.top_k = top_k
        self.processed_urls = 0

    def run(self):
        while True:
            url = self.task_queue.get()
            if url is None:
                break
            print(f"Worker {self.name} Handling URL: {url}")
            top_words = self.process_url(url)
            self.result_queue.put((url, top_words))
            self.task_queue.task_done()
            self.processed_urls += 1
            print(f"Worker {self.name} processed {self.processed_urls} URLs.")

    @staticmethod
    def process_url(url):
        try:
            response = requests.get(url, timeout=5)
            text = response.text
            words = Counter(text.split())
            return dict(words.most_common(7))
        except requests.exceptions.RequestException as e:
            print(f"Processing error {url}: {e}")
            return {}


class Master:
    def __init__(self, port, num_workers, k):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        self.task_queue = queue.Queue()
        self.result_queue = queue.Queue()
        self.active_requests = 0
        self.k = k

        self.workers = [Worker(self.task_queue, self.result_queue, self.k)
                        for _ in range(num_workers)]
        for worker in self.workers:
            worker.start()

    def start(self):
        print("Server is running...")
        while True:
            conn, addr = self.server_socket.accept()
            print(f"Connected {addr}")
            self.handle_client(conn)

    def handle_client(self, conn):
        try:
            url = conn.recv(1024).decode()
            if url:
                if urlparse(url).scheme in ['http', 'https']:
                    self.active_requests += 1
                    self.task_queue.put(url)
                    url, top_words = self.result_queue.get()
                    response = json.dumps(top_words)
                    conn.sendall(response.encode())
                    print(f"URL processed: {self.active_requests}")
                else:
                    conn.sendall("Incorrect URL".encode('utf-8'))
                    print(f"Incorrect URL: {url}")
        except ConnectionResetError as e:
            print(f"Connection reset by client: {e}")
        except TimeoutError as e:
            print(f"Timeout error: {e}")
        except socket.error as e:
            print(f"Socket error: {e}")
        except queue.Empty as e:
            print(f"Result queue is empty: {e}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        finally:
            conn.close()

    def shutdown(self):
        print('Shutting down server...')

        for _ in range(len(self.workers)):
            self.task_queue.put(None)

        for worker in self.workers:
            worker.join()

        self.server_socket.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('-w',
                        type=int,
                        help="Number of Workers",
                        required=True)

    parser.add_argument('-k',
                        type=int,
                        help="Top K Frequent Words",
                        required=True)

    args = parser.parse_args()

    server = Master(8080, args.w, args.k)
    server.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        server.shutdown()
