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

        :param group_name: the name of the load group.
        :param loads: the list of loads.
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

        For each case a tuple is returned of the format:
            ((load factor, load case), (load factor, load case), ...)
        """

        # need to check on what sort of group this is.
        results = []
        for l in self.loads:
            results.append((1, l))

        results = tuple(results)

        yield (results,)

    def __repr__(self):
        return f"LoadGroup('{self.group_name}', {repr(self.loads)})"

    def __str__(self):
        return f'LoadGroup: {self.group_name}, loads: {self.loads}'
