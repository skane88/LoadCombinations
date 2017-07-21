"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""

import math
from numbers import Number
from typing import List, Union
from collections import namedtuple
from Load import Load, ScalableLoad, RotatableLoad, WindLoad

# define a named tuple for returning results.
LoadFactor = namedtuple('LoadFactor', ['load', 'load_factor', 'add_info'])

#define a named tuple for interpolation results
InterpResults = namedtuple('InterpResults', ['left', 'right'])

class LoadGroup:
    """
    This class stores collections of Load objects in groups and determines the
    appropriate return cases.

    This is the base class, and will be inherited by other sorts of load groups.

    This class simply returns all loads in its self.loads method in a single
    valued iterator.
    """

    def __init__(self, *, group_name, loads: List(Load)):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        """
        self.group_name = group_name
        self.loads = loads

    @property
    def group_name(self):
        """
        The name of the load group.
        """

        return self._group_name

    @group_name.setter
    def group_name(self, group_name):
        """
        The name of the load group.

        :param group_name: the name of the load group.
        """

        self._group_name = group_name

    @property
    def loads(self):
        """
        A list of loads to be included in the load group.
        """

        return self._loads

    @loads.setter
    def loads(self, loads):
        """
        A list of loads to be included in the load group.

        :param loads: the list of loads.
        """

        self._loads = loads

    def generate_cases(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors:
            each of them in their own named tuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # need to check on what sort of group this is.
        results = []
        for l in self.loads:
            lf = LoadFactor(load = l, load_factor = 1.0, add_info = '')
            results.append(lf)

        results = tuple(results)

        yield (results,)

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return f"{type(self).__name__}('{self.group_name}', {repr(self.loads)})"

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

    def __init__(self, *, group_name, loads: List(Load), load_factors = 1.0):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param load_factors: the list of load factors.
        """
        super().__init__(group_name = group_name, loads = loads)
        self.load_factors = load_factors

    @property
    def load_factors(self):
        """
        load_factors contains the list of load factors in the group.

        :return: the list of load factors.
        """
        return self._load_factors

    @load_factors.setter
    def load_factors(self, load_factors):
        """
        load_factors contains the list of load factors in the group.

        :param load_factors: the list of load factors.
        """
        self._load_factors = load_factors

    def generate_cases(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        for l in self.loads:
            # first iterate through the load_s

            results = []
            for f in self.load_factors:
                # then iterate through the load_factors

                lf = LoadFactor(load = l, load_factor = f, add_info = '')
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f"{type(self).__name__}(group_name='{self.group_name}', "
                + f"loads={repr(self.loads)}, "
                + f"load_factors={repr(self.load_factors)})")

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, load_factors: {self.load_factors}')


class ScaledGroup(FactoredGroup):
    def __init__(self, *, group_name, loads: List(ScalableLoad), load_factors,
                 scale_to, scale: bool):
        super().__init__(group_name = group_name, loads = loads,
                         load_factors = load_factors)

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

        # first iterate through the loads
        for l in self.loads:

            results = []

            # call the load's scale_factor method to determine the scale
            # factor to scale the load by.
            scale_factor = l.scale_factor(scale_to = self.scale_to,
                                          scale = self.scale)

            for f in self.load_factors:
                # then iterate through the load_factors

                lf = LoadFactor(load = l, load_factor = scale_factor * f,
                                add_info = f'(scaled: {self.scale_to})')
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f"{type(self).__name__}(group_name='{self.group_name}', "
                + f"loads={repr(self.loads)}, "
                + f"load_factors={repr(self.load_factors)}, scale_to="
                + f"{repr(self.scale_to)})")

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, load_factors: {self.load_factors}, '
                + f'scale_to:  {self.scale_to}')


class ExclusiveGroup(ScaledGroup):
    """
    A subclass of ScaledGroup. In an ExclusiveGroup only 1x load case will be
    reported at any time. The only difference from ScaledGroup is the method
    generate_cases returns exclusive results.
    """

    #no need to call __init__ as it shares all the same properties as a scaled
    #group, only calls the generate_cases method differently.

    def generate_cases(self):

        #first iterate through the loads
        for l in self.loads:

            # call the load's scale_factor method to determine the scale
            # factor to scale the load by.
            scale_factor = l.scale_factor(scale_to = self.scale_to,
                                          scale = self.scale)

            # then iterate through the load_factors and get a return.
            for f in self.load_factors:

                lf = LoadFactor(load = l, load_factor = scale_factor * f,
                                add_info = f'(scaled: {self.scale_to})')

                #yield at this level so each load is yielded exclusively.
                yield (lf,)


class RotationalGroup(ScaledGroup):
    """
    A subclass of a ScaledGroup. in a RotationalGroup the loads are scaled by
    load factors corresponding to an interpolation
    """


    def __init__(self, *, group_name, loads: List(RotatableLoad), load_factors,
                 scale_to, scale: bool, half_list: bool, req_angles,
                 interp_func = sine_interp_90):
        super().__init__(group_name = group_name, loads = loads,
                         load_factors = load_factors, scale_to = scale_to,
                         scale = scale)
        self.half_list = half_list
        self.interp_func = interp_func
        self.req_angles = req_angles

    @LoadGroup.loads.setter
    def loads(self, loads):
        """
        Set the loads. This setter overrides the parent class' method to allow
        for the list of loads to be sorted.

        :param loads: The loads that form part of the group.
        """

        #check angles in each load are less than 180 if half_list:
        if self.half_list:
            for l in loads:
                if l.angle >= 180.0:
                    raise ValueError("With half_list = True, all angles must be"
                                     + ' <180.0 degrees. Load ' + l.abbrev
                                     + ' has an angle of ' + l.angle + '°.')

        self._loads = loads.sort(key = lambda x: x.angle)

    @property
    def half_list(self):
        return self._half_list

    @half_list.setter
    def half_list(self, half_list):
        self._half_list = half_list

    @property
    def interp_func(self):
        return self._interp_func

    @interp_func.setter
    def interp_func(self, interp_func):
        self._interp_func = interp_func

    @property
    def req_angles(self):
        return self._req_angles

    @req_angles.setter
    def req_angles(self, req_angles):

        if isinstance(req_angles, Number):
            if isinstance(req_angles, int):
                self._req_angles = req_angles
            else:
                raise ValueError('Expected req_angles to be an integer or a '
                                 + 'list of integers. Value was: '
                                 + f'{repr(req_angles)}')
        else:
            #assume a list or iterable and sort them.
            self._req_angles = sorted(req_angles)

    def generate_angle_list(self):
        """
        Returns the list of angles that this LoadGroup will return load factors
        for.

        :return: A list of the angles that this LoadGroup will generate load
            factors for.
        """

        angle_list = []

        if isinstance(self.req_angles, int):
            angle_list = [i * 360.0 / self.req_angles
                          for i in range(self.req_angles)]
        else:
            angle_list = self.req_angles

        return angle_list

    def generate_cases(self):

        #first build a list of loads and rotation factors:
        load_list = self.loads
        rotation_factor = [1.0 for l in load_list]
        angle_mod = [0.0 for i in rotation_factor]

        #If the loads only form half the circle then need to wrap them around:
        if self.half_list:
            loads = loads + loads
            rotation_factor = rotation_factor + [-1 for i in rotation_factor]
            angle_mod = angle_mod + [180.0 for i in angle_mod]

        #append the first load to the end of the list of loads to get a full
        #360 degree array that wraps around
        load_list = load_list + load_list[:1]
        rotation_factor = rotation_factor + [1]
        angle_mod = angle_mod + [0]

        #zip the load & rotation lists for ease of use later.
        zip_loads = list(zip(load_list, rotation_factor, angle_mod))

        angles_req = self.generate_angle_list()

        #next we need to iterate through the load factors:
        for f in self.load_factors:

            #next iterate through the angles that loads are required from
            for a in angles_req:

                l_min, rf_min = [t for t in zip_loads if (t[0].angle + t[2]) <= a]
                l_min = l_min[-1]
                rf_min = rf_min[-1]
                l_max, rf_max = [t for t in zip_loads if (t[0].angle + t[2]) >= a]
                l_max = l_max[0]
                rf_max = rf_max[0]

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


class WindGroup(FactoredGroup):

    def generate_cases(self):
        raise NotImplementedError()


def linear_interp(gap, x):

    a = (gap - x) / gap
    b = 1 - a
    return InterpResults(left = a, right = b)


def sine_interp_90(gap, x):

    if gap < 0 or gap > 90:
        raise ValueError('Gap expected to be within 90 degrees.')

    return InterpResults(left = math.cos(x), right = math.sin(x))


def sine_interp(gap, x):

    return sine_interp_90(gap * 90.0 / gap, x * 90.0 / gap)


def reversed_group():
    pass


def wind_group_3():
    pass
