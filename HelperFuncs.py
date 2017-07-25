"""
This file contains a number of helper functions that don't really fit under
the Load or LoadGroup headers.
"""

import math
from collections import namedtuple

# define a named tuple for interpolation results
InterpResults = namedtuple('InterpResults', ['left', 'right'])

def linear_interp(gap, x):
    a = (gap - x) / gap
    b = 1 - a
    return InterpResults(left = a, right = b)


def sine_interp_90(gap, x):
    if gap != 90:
        raise ValueError('Gap expected to be 90 degrees.')

    gap = math.radians(gap)
    x = math.radians(x)

    return InterpResults(left = math.cos(x), right = math.sin(x))


def sine_interp(gap, x):
    return sine_interp_90(gap * 90.0 / gap, x * 90.0 / gap)


def wind_interp_85(gap, x):

    α = 1.2 - 0.2 * abs(math.cos(2 * math.radians(x)))
    results = sine_interp_90(gap, x)
    results = InterpResults(results.left * α, results.right * α)

    return results


def reversed_group():
    pass


def wind_group_3():
    pass