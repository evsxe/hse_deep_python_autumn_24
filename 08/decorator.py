import pstats
import cProfile
from functools import wraps


def profile_deco(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        wrapper.profile_data.append(pr)
        return result

    wrapper.profile_data = []

    def print_stat():
        if not wrapper.profile_data:
            print("Function has not been called yet.")
            return
        p = pstats.Stats(wrapper.profile_data[0])
        for profiler in wrapper.profile_data[1:]:
            p.add(profiler)
        p.strip_dirs().sort_stats('cumulative').print_stats()

    wrapper.print_stat = print_stat
    return wrapper
