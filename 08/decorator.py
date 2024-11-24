import cProfile
import pstats

from collections import defaultdict

profile_data = defaultdict(list)


def profile_deco(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        profile_data[func].append(pr)
        return result

    return wrapper


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)

for func, profilers in profile_data.items():
    p = pstats.Stats(profilers[0])
    for profiler in profilers[1:]:
        p.add(profiler)
    p.strip_dirs().sort_stats('cumulative').print_stats()
    print("-" * 20)
