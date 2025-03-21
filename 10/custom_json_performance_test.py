import time
import json
import statistics
import ujson
import custom_json


def benchmark(func, *args):
    times = []
    for _ in range(10):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append(end - start)
    return times


json_files = [f'./10/test_jsons/test_json_{idx}.json' for idx in range(1, 4)]

results = {
    'loads': {
        'custom_json': [],
        'ujson': [],
        'json': []
    },
    'dumps': {
        'custom_json': [],
        'ujson': [],
        'json': []
    }
}

for json_file in json_files:
    try:
        with open(json_file, 'r', encoding='UTF-8') as f:
            big_json_data = json.load(f)
            big_json_str = json.dumps(big_json_data)

            results['loads']['custom_json'].extend(
                benchmark(
                    custom_json.loads,
                    big_json_str
                )
            )

            results['loads']['ujson'].extend(
                benchmark(
                    ujson.loads,
                    big_json_str
                )
            )

            results['loads']['json'].extend(
                benchmark(
                    json.loads,
                    big_json_str
                )
            )

            results['dumps']['custom_json'].extend(
                benchmark(
                    custom_json.dumps,
                    big_json_data
                )
            )

            results['dumps']['ujson'].extend(
                benchmark(
                    ujson.dumps,
                    big_json_data
                )
            )

            results['dumps']['json'].extend(
                benchmark(
                    json.dumps,
                    big_json_data
                )
            )

        print(f"Finished benchmarking file: {json_file}")
    except FileNotFoundError:
        print(f"Error: File not found - {json_file}")


def print_results(res):
    for operation, libs in res.items():
        print(
            f"====================={operation.upper()}=====================")
        for lib, times in libs.items():
            avg = statistics.mean(times)
            stdev = statistics.stdev(times) if len(times) > 1 else 0
            print(
                f"{lib.upper():12}: "
                f"Average = {avg:.6f} seconds, "
                f"Std Dev = {stdev:.6f}"
            )


print_results(results)
