import gc
import time

from decorator import profile_deco


class MyObject:
    def __init__(self, value):
        self.value = value


class RegularClass:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class SlottedClass:
    __slots__ = ['a', 'b', 'c', 'd', 'e']

    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


class WeakRefClass:
    def __init__(self, a, b, c, d, e):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e


num_instances = 100_000

my_objects = [MyObject(i + 1) for i in range(5)]


def timeit(func, *args):
    start = time.perf_counter()
    func(*args)
    end = time.perf_counter()
    return end - start


regular_creation_time = timeit(
    lambda: [RegularClass(*my_objects) for _ in range(num_instances)]
)

slotted_creation_time = timeit(
    lambda: [SlottedClass(*my_objects) for _ in range(num_instances)]
)

weak_ref_creation_time = timeit(
    lambda: [WeakRefClass(*my_objects) for _ in range(num_instances)]
)


@profile_deco
def get_regular_instances():
    return [RegularClass(*my_objects) for _ in range(num_instances)]


@profile_deco
def get_slotted_instances():
    return [SlottedClass(*my_objects) for _ in range(num_instances)]


@profile_deco
def get_weak_ref_instances():
    return [WeakRefClass(*my_objects) for _ in range(num_instances)]


regular_instances = get_regular_instances()
slotted_instances = get_slotted_instances()
weak_ref_instances = get_weak_ref_instances()

regular_access_time = timeit(
    lambda: [instance.a.value + 1 for instance in regular_instances]
)

slotted_access_time = timeit(
    lambda: [instance.a.value + 1 for instance in slotted_instances]
)

weak_ref_access_time = timeit(
    lambda: [instance.a.value + 1 for instance in weak_ref_instances]
)

print(f'Number of instances: {num_instances}')
print(f"RegularClass creation time: {regular_creation_time:.4f} sec")
print(f"SlottedClass creation time: {slotted_creation_time:.4f} sec")
print(f"WeakRefClass creation time: {weak_ref_creation_time:.4f} sec")
print(f"RegularClass attribute access time: {regular_access_time:.4f} sec")
print(f"SlottedClass attribute access time: {slotted_access_time:.4f} sec")
print(f"WeakRefClass attribute access time: {weak_ref_access_time:.4f} sec")

get_regular_instances.print_stat()
get_slotted_instances.print_stat()
get_weak_ref_instances.print_stat()

del regular_instances, slotted_instances, weak_ref_instances, my_objects
gc.collect()
