"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""

from typing import List
from collections import namedtuple
from Load import Load, ScalableLoad

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

        for f in self.load_factors:
            # first iterate through the load_factors

            results = []
            for l in self.loads:
                # then iterate through the loads

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
                 scale_to):
        super().__init__(group_name = group_name, loads = loads,
                         load_factors = load_factors)

        self.scale_to = scale_to

    @property
    def scale_to(self):
        return self._scale_to

    @scale_to.setter
    def scale_to(self, scale_to):
        self._scale_to = scale_to

    def generate_cases(self):

        # first iterate through the load factors
        for f in self.load_factors:

            results = []

            for l in self.loads:
                # then iterate through the loads

                scale_factor = self.scale_to / l.load_value
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
    A subclass of LoadGroup. In an ExclusiveGroup only 1x load case will be
    reported at any time.
    """

    pass


class RotationalGroup(ScaledGroup):
    pass


class WindGroup(ScaledGroup):
    pass


def reversed_group():
    pass


def wind_group_3():
    pass
