"""
This file contains a number of helper functions that don't really fit under
the Load or LoadGroup headers.
"""

import math
from collections import namedtuple
from typing import List, Tuple, Union

# define a named tuple for interpolation results
InterpResults = namedtuple('InterpResults', ['left', 'right'])


def linear_interp(gap, x):
    a = (gap - x) / gap
    b = 1 - a
    return InterpResults(left = a, right = b)


def sine_interp_90(gap: float, x: float):
    if gap != 90:
        raise ValueError('Gap expected to be 90 degrees.')

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


def req_angles_int(no_angles: int):
    """
    Sets the no. of req_angles based on a single integer input, rather than
    a list of input angles.
    """

    angle_list = [i * 360.0 / no_angles for i in range(no_angles)]

    return angle_list

def req_angles_list(req_angles: Union[List[float], Tuple[float, ...]]):

    req_angles = tuple(i % 360 for i in req_angles)  # Convert everything
                                                     # into the 360 deg range
    req_angles = tuple(set(req_angles))  # Remove duplicates

    return tuple(sorted(req_angles))  # Sort and return the list

def req_angles_chooser(angles: Union[Union[List[float], Tuple[float,...]], int]):

    if isinstance(angles, int):
        return req_angles_int(angles)
    else:
        return req_angles_list(angles)