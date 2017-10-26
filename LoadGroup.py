# coding=utf-8

"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""

from typing import List, Tuple, Union, Callable
from collections import namedtuple
from Load import Load, ScalableLoad, RotatableLoad, WindLoad
from HelperFuncs import sine_interp_90, wind_interp_85, req_angles_list
from copy import deepcopy

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

    def add_load(self, load: Load):
        """
        A method to add a single load into the loads that make up the group.

        This is a place-holder method currently. Eventually it is planned to
        use this method to provide logic when adding the loads in
        through the "loads" property, to allow for checking that loads don't
        already exist etc. and to allow migration of the internal storage
        from a list to a dictionary.

        :param load: The load to add.
        """

        raise NotImplementedError

    def del_load(self, load_no: int = None, load_name: str = None,
                 abbrev: str = None):
        """
        A method to delete a single load from the loads list.

        This is a place-holder method currently. Eventually it is planned to
        use this method to allow deletion of a single load at a time from the
        group.

        Loads should be able to be deleted optionally via their no., name or
        abbrev.

        :param load_no: The load_no of the load to delete.
        :param load_name: The load_name of the load to delete.
        :param abbrev:  The abbrev of the load to delete.
        """
        raise NotImplementedError

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
        Creates a LoadGroup object.

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param factors: the list of load factors.
        :param abbrev: An abbreviation for the load group.
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

        :param factors: the list of load factors.
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
    """
    A ScaledGroup is a subclass of factored groups and has the following
    properties:

    * A single factor can be applied to all loads.
    * A scaling factor can be applied to scale loads that may be based on
        different real life values (i.e. different floor loads) to a common
        value - for example, scaling all floor loads to 2.5kPa.
    """

    def __init__(self, *, group_name, loads: List[ScalableLoad],
                 factors: Tuple[float, ...], scale_to: float,
                 scale: bool = True,
                 abbrev: str = ''):
        """
        A constructor for a ScaledGroup object.

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param factors: the list of load factors.
        :param scale_to: The load the group should be scaled to.
        :param scale: Should the group scale. by default this is True.
        :param abbrev: An abbreviation for the load group.
        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, abbrev = abbrev)

        self.scale_to = scale_to
        self.scale = scale

    @property
    def scale_to(self) -> float:
        """
        The value to scale all the loads to.

        :return: The value to which all loads will be scaled to.
        """
        return self._scale_to

    @scale_to.setter
    def scale_to(self, scale_to: float):
        """
        The value to scale all the loads to.

        :param scale_to: The value to which all loads will be scaled to.
        """
        self._scale_to = scale_to

    @property
    def scale(self) -> bool:
        """
        Should the scale factor be used. If False, this is effectively the same
        as the factored load group.

        :return: Is the group scaled?
        """
        return self._scale

    @scale.setter
    def scale(self, scale: bool):
        """
        Should the scale factor be used. If False, this is effectively the same
        as the factored load group.

        :param scale: Should the scale factor be used. If False, this is
            effectively the same as the factored load group.
        """
        self._scale = scale

    def generate_cases(self,
                       scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # first iterate through the load factors so that all loads have the same
        # factor
        for f in self.factors:

            results = []

            # then iterate through the loads
            for l in self.loads:
                # call the load's scale_factor method to determine the scale
                # factor to scale the load by.
                scale_factor = l.scale_factor(scale_to = self.scale_to,
                                              scale_func = scale_func,
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

    def generate_cases(self,
                       scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # first iterate through the load factors
        for f in self.factors:

            # then iterate through the loads and get a return.
            for l in self.loads:
                # call the load's scale_factor method to determine the scale
                # factor to scale the load by.
                scale_factor = l.scale_factor(scale_to = self.scale_to,
                                              scale_func = scale_func,
                                              scale = self.scale)

                lf = LoadFactor(load = l, load_factor = scale_factor * f,
                                add_info = f'(scaled: {self.scale_to})')

                # yield at this level so each load is yielded exclusively.
                yield (lf,)


class RotationalGroup(ScaledGroup):
    """
    A subclass of a ScaledGroup. in a RotationalGroup the loads are scaled by
    load factors but also between each other depending on a specified angle
    at which the interpolation is carried out.
    """

    def __init__(self, *, group_name, loads: List[RotatableLoad],
                 factors: Tuple[float, ...], scale_to: float, scale: bool,
                 req_angles: Tuple[float, ...],
                 interp_func: Callable = sine_interp_90,
                 abbrev: str = ''):
        """
        Constructor for a RotationalGroup object.

        :param group_name: The name of the load group.
        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        :param factors: the list of load factors.
        :param scale_to: The load the group should be scaled to.
        :param scale: Should the group scale. by default this is True.
        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        :param abbrev: An abbreviation for the load group.
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

    def add_load(self, load: Load):
        """
        A method to add a single load into the loads that make up the group.

        This is a place-holder method currently. Eventually it is planned to
        use this method to provide logic when adding the loads in
        through the "loads" property, to allow for checking that loads don't
        already exist etc. and to allow migration of the internal storage
        from a list to a dictionary.

        :param load: The load to add.
        """

        raise NotImplementedError

    def del_load(self, load_no: int = None, load_name: str = None,
                 abbrev: str = None):
        """
        A method to delete a single load from the loads list.

        This is a place-holder method currently. Eventually it is planned to
        use this method to allow deletion of a single load at a time from the
        group.

        Loads should be able to be deleted optionally via their no., name or
        abbrev.

        :param load_no: The load_no of the load to delete.
        :param load_name: The load_name of the load to delete.
        :param abbrev:  The abbrev of the load to delete.
        """
        raise NotImplementedError

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

        :return: A tuple containing the angles that the RotationalGroup will
            generate load combinations for.
        """
        return self._req_angles

    @req_angles.setter
    def req_angles(self, req_angles: Union[List[float], Tuple[float, ...]]):
        """
        The setter for the req_angles list.

        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        """

        self._req_angles = req_angles_list(req_angles)

    def generate_cases(self, scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        The load factor will interpolate between loads based on the given
        list of required return angles.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # first build a dictionary of loads mapped to their angles:
        load_dict = {l.angle: l for l in self.loads}
        sym_dict = {l.angle: 1.0 for l in self.loads}

        # next go through each load and check if it can be reversed.
        for l in self.loads:

            if l.symmetrical:
                # if l is symmetrical then need to check if the angle already
                # exists in the dictionary

                angle = (l.angle + 180.0) % 360

                if angle not in load_dict:
                    # only add to the load dict if there isn't already an angle

                    l_new = deepcopy(l)
                    # note: don't change the angle for the copied load, as this
                    # would change the load itself

                    load_dict[angle] = l_new
                    sym_dict[angle] = -1.0

        # next check if 0 or 360 exist in the load dictionary, and wrap them
        # around if necessary

        if 0.0 in load_dict and 360.0 not in load_dict:
            # need to wrap 0.0 to 360.0

            l_new = deepcopy(load_dict[0.0])

            # note don't change the angle for the copied load as this would
            # change the load

            load_dict[360.0] = l_new
            sym_dict[360.0] = 1.0

        if 360.0 in load_dict and 0.0 not in load_dict:
            # need to wrap 360.0 to 0.0

            l_new = deepcopy(load_dict[360.0])

            # note don't change the angle for the copied load as this would
            # change the load

            load_dict[0.0] = l_new
            sym_dict[0.0] = 1.0

        # next need to get a list of angles rather than a dictionary so we can
        # easily slice
        list_angles = sorted(load_dict.keys())

        # next we need to iterate through the load factors:
        for f in self.factors:

            # next iterate through the angles that loads are required from
            for a in self.req_angles:

                # first check if a is already in the list of angles
                if a in list_angles:
                    # if so, we can simply return load_a
                    load_a = load_dict[a]
                    sym_a = sym_dict[a]

                    scale_a = load_a.scale_factor(scale_to = self.scale_to,
                                                  scale_func = scale_func,
                                                  scale = self.scale)

                    lf1 = LoadFactor(load = load_a,
                                     load_factor = scale_a * sym_a * f,
                                     add_info = f'(Rotated: {a})')
                    ret_val = (lf1,)

                else:
                    # if not, we need to interpolate between angles.
                    list_min = [x for x in list_angles if x <= a]

                    if len(list_min) == 0:
                        # if there are no elements less than or == a, then we
                        # need to get the last element and wrap it round
                        l_min = list_angles[-1]
                        load_min = load_dict[l_min]
                        sym_min = sym_dict[l_min]
                        l_min = l_min.angle - 360.0
                    else:
                        # else, the next smallest angle will do.
                        l_min = list_min[-1]
                        load_min = load_dict[l_min]
                        sym_min = sym_dict[l_min]

                    scale_min = load_min.scale_factor(scale_to = self.scale_to,
                                                      scale_func = scale_func,
                                                      scale = self.scale)

                    list_max = [x for x in list_angles if x >= a]

                    if len(list_max) == 0:
                        # if there are no angles in the list larger than a
                        # we need to take the smallest and wrap it around
                        l_max = list_angles[0]
                        load_max = load_dict[l_max]
                        sym_max = sym_dict[l_max]
                        l_max = l_max + 360.0
                    else:
                        # else the next largest angle will do
                        l_max = list_max[0]
                        load_max = load_dict[l_max]
                        sym_max = sym_dict[l_max]

                    scale_max = load_max.scale_factor(scale_to = self.scale_to,
                                                      scale_func = scale_func,
                                                      scale = self.scale)

                    gap = l_max - l_min
                    x = a - l_min

                    factors = self.interp_func(gap, x)

                    lf1 = LoadFactor(load = load_min,
                                     load_factor = scale_min * sym_min * f * factors.left,
                                     add_info = f'(Rotated: {a})')
                    lf2 = LoadFactor(load = load_max,
                                     load_factor = scale_max * sym_max * f * factors.right,
                                     add_info = f'(Rotated: {a})')

                    ret_val = (lf1, lf2)

                yield ret_val

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


class WindGroup(RotationalGroup):
    """
    A subclass of a RotatableGroup. The only differences are that:

    property scale_speed is provided as an alias to scale_to
    The generate_cases function overrides the parent case to provide a
        scale_func that scales the loads based on the wind speed. Wind load
        scales on the square of wind speed and therefore if a load is input
        at 10m/s and is scaled to 20m/s the scale factor returned is
        4.0, whereas a RotationalGroup object will return 2.
    """

    def __init__(self, *, group_name, loads: List[RotatableLoad],
                 factors: Tuple[float, ...], scale_speed: float, scale: bool,
                 req_angles: Tuple[float, ...],
                 interp_func: Callable = wind_interp_85,
                 abbrev: str = ''):
        """
        The constructor for a WindGroup object.

        :param group_name: The name of the load group.
        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        :param factors: the list of load factors.
        :param scale_speed: The wind_speed the load group is scaled to. This is
            simply an alias for the scale_to property of the parent class
            RotatationalGroup.
        :param scale: Should the group scale. by default this is True.
        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        :param abbrev: An abbreviation for the load group.


        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, scale_to = scale_speed,
                         scale = scale, req_angles = req_angles,
                         interp_func = interp_func,
                         abbrev = abbrev)


    @property
    def scale_speed(self) -> float:
        """
        The wind_speed that the load group is scaled to. This is simply an alias
        for the scale_to property of the parent class RotatationalGroup.

        :return: Returns the wind_speed that the load group is scaled to.
        """

        return self._scale_to

    @scale_speed.setter
    def scale_speed(self, scale_speed: float):
        """
        The wind_speed that the load group is scaled to. This is simply an alias
        for the scale_to property of the parent class RotatationalGroup.

        :param scale_speed: The wind_speed the load group is scaled to. This is
            simply an alias for the scale_to property of the parent class
            RotatationalGroup.
        """

        self._scale_to = scale_speed

    def generate_cases(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        The load factor will interpolate between loads based on the given
        list of required return angles.

        Note that this overrides the parent function from RotationalGroup to
        provide a scale_func that scales the loads based on the wind speed.
        Wind load scales on the square of wind speed and therefore if a load
        is input at 10m/s and is scaled to 20m/s the scale factor returned is
        4.0, whereas a RotationalGroup object will return 2.0.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        def scale_func(scale_to, scale_from):
            return (scale_to ** 2) / (scale_from ** 2)

        return super(WindGroup, self).generate_cases(scale_func)

    def __str__(self):

        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_speed:  {self.scale_speed}'
                + f'angles: {self.req_angles}')

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_speed={repr(self.scale_speed)}, '
                + f'scale={repr(self.scale)}, '
                + f'req_angles={repr(self.req_angles)}, '
                + f'interp_func={repr(self.interp_func.__name__)}, '
                + f'abbrev={repr(self.abbrev)})')
