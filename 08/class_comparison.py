import gc
import time
import weakref
import tracemalloc

from decorator import profile_deco


class MyObject:  # pylint: disable=all
    def __init__(self, value):
        self.value = value


class RegularClass:  # pylint: disable=all
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class SlottedClass:  # pylint: disable=all
    __slots__ = ['a', 'b', 'c', 'd', 'e']

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class WeakRefClass:  # pylint: disable=all
    def __init__(self, a, b, c, d, e):
        self.a = weakref.ref(a)
        self.b = weakref.ref(b)
        self.c = weakref.ref(c)
        self.d = weakref.ref(d)
        self.e = weakref.ref(e)


NUM_INSTANCES = 10_000
my_objects = [MyObject(i + 1) for i in range(5)]


def timeit(func, *args, memory_profile=False):
    start = time.perf_counter()
    tracemalloc.start()
    _ = func(*args)
    end = time.perf_counter()
    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    if memory_profile:
        top_stats = snapshot.statistics('lineno')
        print("Memory usage:")
        for stat in top_stats[:10]:
            print(stat)
    return end - start


regular_creation_time = timeit(
    lambda: [RegularClass(
        *[MyObject(i + 1) for i in range(5)]) for _ in range(NUM_INSTANCES)]
)

slotted_creation_time = timeit(
    lambda: [SlottedClass(
        *[MyObject(i + 1) for i in range(5)]) for _ in range(NUM_INSTANCES)]
)

weak_ref_creation_time = timeit(
    lambda: [WeakRefClass(
        *[MyObject(i + 1) for i in range(5)]) for _ in range(NUM_INSTANCES)]
)

regular_access_time = timeit(
    lambda: [
        instance.a.value + 1 for instance in [
            RegularClass(
                *[MyObject(i + 1) for i in range(5)]
            ) for _ in range(NUM_INSTANCES)
        ]
    ]
)

slotted_access_time = timeit(
    lambda: [
        instance.a.value + 1 for instance in [
            SlottedClass(
                *[MyObject(i + 1) for i in range(5)]
            ) for _ in range(NUM_INSTANCES)
        ]
    ]
)

weak_ref_access_time = timeit(
    lambda: [
        instance.a().value + 1 if instance.a() else 0 for instance in [
            WeakRefClass(
                *[MyObject(i + 1) for i in range(5)]
            ) for _ in range(NUM_INSTANCES)
        ]
    ]
)

print(f'Number of instances: {NUM_INSTANCES}')
print(f"RegularClass creation time: {regular_creation_time:.4f} sec")
print(f"SlottedClass creation time: {slotted_creation_time:.4f} sec")
print(f"WeakRefClass creation time: {weak_ref_creation_time:.4f} sec")
print(f"RegularClass attribute access time: {regular_access_time:.4f} sec")
print(f"SlottedClass attribute access time: {slotted_access_time:.4f} sec")
print(f"WeakRefClass attribute access time: {weak_ref_access_time:.4f} sec")

get_regular_instances = profile_deco(
    lambda: [RegularClass(*my_objects) for _ in range(NUM_INSTANCES)]
)

get_slotted_instances = profile_deco(
    lambda: [SlottedClass(*my_objects) for _ in range(NUM_INSTANCES)]
)

get_weak_ref_instances = profile_deco(
    lambda: [WeakRefClass(*my_objects) for _ in range(NUM_INSTANCES)]
)

get_regular_instances()
get_slotted_instances()
get_weak_ref_instances()

get_regular_instances.print_stat()
get_slotted_instances.print_stat()
get_weak_ref_instances.print_stat()

# del regular_instances, slotted_instances, weak_ref_instances, my_objects
gc.collect()
