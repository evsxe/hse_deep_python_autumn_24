import gc
import time


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

regular_instances = [RegularClass(*my_objects) for _ in range(num_instances)]
slotted_instances = [SlottedClass(*my_objects) for _ in range(num_instances)]
weak_ref_instances = [WeakRefClass(*my_objects) for _ in range(num_instances)]

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

del regular_instances, slotted_instances, weak_ref_instances, my_objects
gc.collect()
