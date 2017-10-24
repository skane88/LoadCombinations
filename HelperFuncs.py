# coding=utf-8

"""
This file contains a number of helper functions that don't really fit under
the Load or LoadGroup headers.
"""

import math
from collections import namedtuple
from typing import List, Tuple, Union

# define a named tuple for interpolation results
InterpResults = namedtuple('InterpResults', ['left', 'right'])


def linear_interp(range: float, x: float):
    """
    Linearly interpolates within a range. Used for the interpolation functions
    within the LoadGroup functions, and returns a "left" and "right" factor that
    can be used to factor 2x loads to generate a resultant load that is in
    between them.

    :param range: The range to interpolate between.
    :param x: An interim value within the range.
    :return: Returns an InterpResults NamedTuple with a factor for the LHS & RHS
        loads.
    """

    if x < 0 or x > range:
        raise ValueError("Expected x to be within the range.")

    a = (range - x) / range
    b = 1 - a
    return InterpResults(left = a, right = b)


def sine_interp_90(range: float, x: float):
    """
    Interpolates within a range. Used for the interpolation functions
    within the LoadGroup functions, and returns a "left" and "right" factor that
    can be used to factor 2x loads to generate a resultant load that is in
    between them.

    This function interpolates using a sine curve.

    This function throws an error if the range is != 90 degrees. Technically the
    range should not be specified (it is always 90) but for compatibility with
    other interpolation functions (where the range could be specified) it is
    left in as an argument so that the RotationalGroup and WindGroup
    generate_cases functions do not have to be customised.

    :param range: The range to interpolate between.
    :param x: An interim value within the range.
    :return: Returns an InterpResults NamedTuple with a factor for the LHS & RHS
        loads.
    """

    if range != 90:
        raise ValueError('Gap expected to be 90 degrees.')

    if x < 0 or x > 90:
        raise ValueError('x expected to be within the 90 degree range.')

    x = math.radians(x)

    return InterpResults(left = math.cos(x), right = math.sin(x))


def sine_interp(range: float, x: float):
    """
    Interpolates within a range. Used for the interpolation functions
    within the LoadGroup functions, and returns a "left" and "right" factor that
    can be used to factor 2x loads to generate a resultant load that is in
    between them.

    This function interpolates using a sine curve.

    To achieve this it scales both the range and the interpolation value by the
    parameter 90 / range.

    :param range: The range to interpolate between.
    :param x: An interim value within the range.
    :return: Returns an InterpResults NamedTuple with a factor for the LHS & RHS
        loads.
    """

    if x < 0 or x > range:
        raise ValueError(f'x expected to be within the range 0 to {range}.'
                         + f' x given was {x}')

    return sine_interp_90(range * 90.0 / range, x * 90.0 / range)


def wind_interp_85(range: float, x: float):
    """
    Interpolates within a range. Used for the interpolation functions
    within the LoadGroup functions, and returns a "left" and "right" factor that
    can be used to factor 2x loads to generate a resultant load that is in
    between them.

    This function interpolates using a sine curve. This is then modified with
    the factor 1.20208-0.20208 * abs(cos(2 * x)) to produce a value that at the
    45 degree angle results in an increase in load of about 20%. This is
    consistent with the method given in AS4324 for non-orthogonal wind loads.

    This function throws an error if the range is != 90 degrees. Technically the
    range should not be specified (it is always 90) but for compatibility with
    other interpolation functions (where the range could be specified) it is
    left in as an argument so that the RotationalGroup and WindGroup
    generate_cases functions do not have to be customised.

    :param range: The range to interpolate between.
    :param x: An interim value within the range.
    :return: Returns an InterpResults NamedTuple with a factor for the LHS & RHS
        loads.
    """

    if x < 0 or x > range:
        raise ValueError(f'x expected to be within the range of {range}. '
                         + f'x given was {x}')

    α = 1.20208 - 0.20208 * abs(math.cos(2 * math.radians(x)))
    results = sine_interp_90(range, x)
    results = InterpResults(results.left * α, results.right * α)

    return results


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


def req_angles_chooser(
        angles: Union[Union[List[float], Tuple[float, ...]], int]):

    if isinstance(angles, int):
        return req_angles_int(angles)
    else:
        return req_angles_list(angles)
