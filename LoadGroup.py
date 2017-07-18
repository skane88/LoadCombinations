"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""


class LoadGroup:
    """
    This class stores collections of Load objects in groups and determines the
    appropriate return cases.

    This is the base class, and will be inherited by other sorts of load groups.

    This class simply returns all loads in its self.loads method in a single
    valued iterator.
    """

    def __init__(self, *, group_name, loads):
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

        :return: returns a generator which will create a tuple of load cases:
            ((load case, load factor), (load case, load factor), ...)
        """

        # need to check on what sort of group this is.
        results = []
        for l in self.loads:
            results.append((l, 1.0))

        results = tuple(results)

        yield (results,)

    def __repr__(self):

        #use the {type(self).__name__} call to get the exact class name. This
        #should allow the __repr__ method to be accepted for subclasses of
        #LoadGroup without change.
        return f"{type(self).__name__}('{self.group_name}', {repr(self.loads)})"

    def __str__(self):

        #use the {type(self).__name__} call to get the exact class name. This
        #should allow the __str__ method to be accepted for subclasses of
        #LoadGroup without change.
        return f'{type(self).__name__}: {self.group_name}, loads: {self.loads}'

#next define more complex load groups as subclasses.
class FactoredGroup(LoadGroup):
    """
    A subclass of LoadGroup. In a FactoredGroup the loads are treated as a group
    (i.e. all will be returned in the generated result loads, but they can be
    returned with a given list of load factors.
    """

    def __init__(self, *, group_name, loads, load_factors):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param load_factors: the list of load factors.
        """
        self.group_name = group_name
        self.loads = loads
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

        :return: returns a generator which will create a tuple of load cases:
            ((load case, load factor), (load case, load factor), ...)
        """

        for f in self.load_factors:
            #first iterate through the load_factors

            results = []
            for l in self.loads:
                results.append((l, f))

            results = tuple(results)

            yield results

    def __repr__(self):

        #use the {type(self).__name__} call to get the exact class name. This
        #should allow the __repr__ method to be accepted for subclasses of
        #LoadGroup without change.
        return (f"{type(self).__name__}(group_name='{self.group_name}', "
                + f"loads={repr(self.loads)}, "
                + f"load_factors={repr(self.load_factors)})")

    def __str__(self):

        #use the {type(self).__name__} call to get the exact class name. This
        #should allow the __str__ method to be accepted for subclasses of
        #LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, load_factors: {self.load_factors}')

class ExclusiveGroup(LoadGroup):
    """
    A subclass of LoadGroup. In an ExclusiveGroup only 1x load case will be
    reported at any time.
    """

    pass

class RotationalGroup(LoadGroup):
    pass

class WindGroup(LoadGroup):
    pass

class WindGroup3(WindGroup):
    pass

