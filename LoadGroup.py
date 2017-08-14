# coding=utf-8

"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""

from typing import List, Tuple, Union, Callable
from collections import namedtuple
from Load import Load, ScalableLoad, RotatableLoad, WindLoad
from HelperFuncs import sine_interp_90

# define a named tuple for returning results.
LoadFactor = namedtuple('LoadFactor', ['load', 'load_factor', 'add_info'])


class LoadGroup:
    """
    This class stores collections of Load objects in groups and determines the
    appropriate return cases.

    This is the base class, and will be inherited by other sorts of load groups.

    This class simply returns all loads in its self.loads method in a single
    valued iterator.
    """

    def __init__(self, *, group_name: str, loads: List[Load], abbrev: str = ''):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param abbrev: An abbreviation for the load group.
        """
        self.group_name = group_name
        self.loads = loads
        self.abbrev = abbrev

    @property
    def group_name(self) -> str:
        """
        The name of the load group.
        """

        return self._group_name

    @group_name.setter
    def group_name(self, group_name: str):
        """
        The name of the load group.

        :param group_name: the name of the load group.
        """

        self._group_name = group_name

    @property
    def loads(self) -> List[Load]:
        """
        A list of loads to be included in the load group.
        """

        return self._loads

    @loads.setter
    def loads(self, loads: List[Load]):
        """
        A list of loads to be included in the load group.

        :param loads: the list of loads.
        """

        self._loads = loads

    @property
    def abbrev(self) -> str:
        """
        An abbreviation for the LoadGroup.

        :return: Returns the abbreviation.
        """

        return self._abbrev

    @abbrev.setter
    def abbrev(self, abbrev: str):
        """
        An abbreviation for the LoadGroup.

        :param abbrev: An abbreviation for the load group.
        """

        self._abbrev = abbrev

    def generate_cases(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own named tuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        results = []
        for l in self.loads:
            lf = LoadFactor(load = l, load_factor = 1.0, add_info = '')
            results.append(lf)

        results = tuple(results)

        yield results

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}('
                + f'group_name = {repr(self.group_name)}, '
                + f'loads = {repr(self.loads)}, '
                + f'abbrev = {repr(self.abbrev)}'
                + ')')

    def __str__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return f'{type(self).__name__}: {self.group_name}, loads: {self.loads}'


# next define more complex load groups as subclasses.
class FactoredGroup(LoadGroup):
    """
    A subclass of LoadGroup. In a FactoredGroup the loads are treated as a group
    (i.e. all will be returned in the generated result loads, but they can be
    returned with a given list of load factors.
    """

    def __init__(self, *, group_name, loads: List[Load],
                 factors: Tuple[float, ...] = (1.0,), abbrev: str = ''):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param factors: the list of load factors.
        """
        super().__init__(group_name = group_name, loads = loads,
                         abbrev = abbrev)
        self.factors = factors

    @property
    def factors(self) -> Tuple[float, ...]:
        """
        load_factors contains the list of load factors in the group.

        :return: the list of load factors.
        """

        return self._factors

    @factors.setter
    def factors(self, factors: Tuple[float]):
        """
        load_factors contains the list of load factors in the group.

        :param load_factors: the list of load factors.
        """
        self._factors = factors

    def generate_cases(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        for f in self.factors:
            # first iterate through the factors, so that all loads in the group
            # have the same factor

            results = []
            for l in self.loads:
                # then iterate through the load_factors

                lf = LoadFactor(load = l, load_factor = f, add_info = '')
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, factors: {self.factors}')


class ScaledGroup(FactoredGroup):
    def __init__(self, *, group_name, loads: List[ScalableLoad],
                 factors: Tuple[float, ...], scale_to: float, scale: bool,
                 abbrev: str = ''):

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, abbrev = abbrev)

        self.scale_to = scale_to
        self.scale = scale

    @property
    def scale_to(self):
        return self._scale_to

    @scale_to.setter
    def scale_to(self, scale_to):
        self._scale_to = scale_to

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    def generate_cases(self):

        # first iterate through the load factors so that all loads have the same
        # factor
        for f in self.factors:

            results = []

            # then iterate through the loads
            for l in self.loads:
                # call the load's scale_factor method to determine the scale
                # factor to scale the load by.
                scale_factor = l.scale_factor(scale_to = self.scale_to,
                                              scale = self.scale)

                lf = LoadFactor(load = l, load_factor = scale_factor * f,
                                add_info = f'(scaled: {self.scale_to})')
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_to={repr(self.scale_to)}, '
                + f'scale={repr(self.scale)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_to:  {self.scale_to}')


class ExclusiveGroup(ScaledGroup):
    """
    A subclass of ScaledGroup. In an ExclusiveGroup only 1x load case will be
    reported at any time. The only difference from ScaledGroup is the method
    generate_cases returns exclusive results.
    """

    # no need to call __init__ as it shares all the same properties as a scaled
    # group, only calls the generate_cases method differently.

    def generate_cases(self):

        # first iterate through the load factors
        for f in self.factors:

            # then iterate through the loads and get a return.
            for l in self.loads:
                # call the load's scale_factor method to determine the scale
                # factor to scale the load by.
                scale_factor = l.scale_factor(scale_to = self.scale_to,
                                              scale = self.scale)

                lf = LoadFactor(load = l, load_factor = scale_factor * f,
                                add_info = f'(scaled: {self.scale_to})')

                # yield at this level so each load is yielded exclusively.
                yield (lf,)


class RotationalGroup(ScaledGroup):
    """
    A subclass of a ScaledGroup. in a RotationalGroup the loads are scaled by
    load factors corresponding to an interpolation
    """

    def __init__(self, *, group_name, loads: List[RotatableLoad],
                 factors: Tuple[float, ...], scale_to, scale: bool,
                 req_angles: Tuple[float, ...],
                 interp_func: Callable = sine_interp_90,
                 abbrev: str = ''):
        """

        :param group_name:
        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        :param factors:
        :param scale_to:
        :param scale:
        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        :param interp_func:
        :param abbrev:
        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        self.interp_func = interp_func
        self.req_angles = req_angles

    @LoadGroup.loads.setter
    def loads(self, loads):
        """
        Set the loads. This setter overrides the parent class' method to allow
        for the list of loads to be sorted.

        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        """

        # store loads as a sorted list
        loads.sort(key = lambda x: x.angle)
        self._loads = loads

    @property
    def interp_func(self) -> Callable[[float, float], Tuple[float, float]]:
        """
        Getter for the interpolation function.

        :return: Returns the interpolation function used to determine the load
            factors for intermediate angles between the Load angles.
        """
        return self._interp_func

    @interp_func.setter
    def interp_func(self, interp_func: Callable[[float, float],
                                                Tuple[float, float]]):
        """
        Setter for the interpolation function.

        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        """

        self._interp_func = interp_func

    @property
    def req_angles(self) -> Tuple[float, ...]:
        """
        The getter for the req_angles.

        :return: A tuple containing the angles that the RotataionalGroup will
            generate load combinations for.
        """
        return self._req_angles

    @req_angles.setter
    def req_angles(self, req_angles: Tuple[float, ...]):
        """
        The setter for the req_angles list.

        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        """

        req_angles = tuple(i % 360 for i in req_angles) # Convert everything
                                                        # into the 360 deg range
        req_angles = tuple(set(req_angles)) # Remove duplicates

        self._req_angles = tuple(sorted(req_angles)) # Sort and set the
                                                     # attribute

    def set_req_angles_int(self, no_angles: int):
        """
        Sets the no. of req_angles based on a single integer input, rather than
        a list of input angles.
        """

        angle_list = [i * 360.0 / no_angles for i in range(no_angles)]

        self.req_angles = angle_list

    def generate_cases(self):

        # first build a list of loads and rotation factors:
        load_list = self.loads
        rotation_factor = [1.0] * len(load_list)
        angle_mod = [0.0] * len(load_list)

        # If the loads only form half the circle then need to wrap them around:
        if self.half_list:
            load_list = load_list + load_list
            rotation_factor = rotation_factor + [-1] * len(rotation_factor)
            angle_mod = angle_mod + [180.0] * len(angle_mod)

        # append the first load to the end of the list of loads to get a full
        # 360 degree array that wraps around
        load_list = load_list + load_list[:1]
        rotation_factor = rotation_factor + [1]
        angle_mod = angle_mod + [0]

        # zip the load & rotation lists for ease of use later.
        zip_loads = list(zip(load_list, rotation_factor, angle_mod))

        angles_req = self.generate_angle_list()

        # next we need to iterate through the load factors:
        for f in self.load_factors:

            # next iterate through the angles that loads are required from
            for a in angles_req:
                list_min = [t for t in zip_loads if (t[0].angle + t[2]) <= a]
                l_min = list_min[-1][0]
                rf_min = list_min[-1][1]
                list_max = [t for t in zip_loads if (t[0].angle + t[2]) >= a]
                l_max = list_max[0][0]
                rf_max = list_max[0][1]

                gap = l_max.angle - l_min.angle
                x = a - l_min.angle

                factors = self.interp_func(gap, x)

                lf1 = LoadFactor(load = l_min,
                                 load_factor = rf_min * f * factors.left,
                                 add_info = f'(Rotated: {a})')
                lf2 = LoadFactor(load = l_max,
                                 load_factor = rf_max * f * factors.right,
                                 add_info = f'(Rotated: {a})')

                yield (lf1, lf2)

    def __str__(self):

        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_to:  {self.scale_to}'
                + f'angles: {self.req_angles}')

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_to={repr(self.scale_to)}, '
                + f'scale={repr(self.scale)}, '
                + f'req_angles={repr(self.req_angles)}, '
                + f'interp_func={repr(self.interp_func.__name__)}, '
                + f'abbrev={repr(self.abbrev)})')

class WindGroup(FactoredGroup):
    def generate_cases(self):
        raise NotImplementedError()
