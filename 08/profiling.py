import pstats
import cProfile

from class_comparison import (RegularClass,
                              SlottedClass,
                              WeakRefClass)  # pylint: disable=all

cProfile.run(
    'for i in range(10000): RegularClass(1,2,3,4,5)',
    'regular_profile'
)

cProfile.run(
    'for i in range(10000): SlottedClass(1,2,3,4,5)',
    'slotted_profile'
)

cProfile.run(
    'for i in range(10000): WeakRefClass(1,2,3,4,5)',
    'weak_ref_profile'
)

p = pstats.Stats('regular_profile')
p.strip_dirs().sort_stats('cumulative').print_stats(20)

p = pstats.Stats('slotted_profile')
p.strip_dirs().sort_stats('cumulative').print_stats(20)

p = pstats.Stats('weak_ref_profile')
p.strip_dirs().sort_stats('cumulative').print_stats(20)
