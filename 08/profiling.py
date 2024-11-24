import pstats
import cProfile
import tracemalloc

from class_comparison import (RegularClass,
                              SlottedClass,
                              WeakRefClass,
                              MyObject)


def profile_class(cls, num_iterations=10_000):
    my_objects = [MyObject(i + 1) for i in range(5)]
    tracemalloc.start()

    if cls == WeakRefClass:
        def weak_ref_creation():
            for i in range(num_iterations):
                cls(*my_objects)

        cProfile.runctx('weak_ref_creation()', globals(), locals(),
                        f'{cls.__name__}_profile')
    else:
        def regular_creation():
            for i in range(num_iterations):
                cls(1, 2, 3, 4, 5)

        cProfile.runctx('regular_creation()', globals(), locals(),
                        f'{cls.__name__}_profile')

    snapshot = tracemalloc.take_snapshot()
    tracemalloc.stop()
    top_stats = snapshot.statistics('lineno')

    print(f"\nMemory usage for {cls.__name__}:")
    for stat in top_stats[:10]:
        print(stat)

    p = pstats.Stats(f'{cls.__name__}_profile')
    p.strip_dirs().sort_stats('cumulative').print_stats(20)


profile_class(RegularClass)
profile_class(SlottedClass)
profile_class(WeakRefClass)
