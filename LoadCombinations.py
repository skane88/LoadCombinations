# coding=utf-8

"""
This contains a class describing a ``LoadCombinations`` object. This will be
used to combine Loads, LoadGroups and LoadCases together into a single simple
object for use by the end user.
"""

class LoadCombinations():
    """
    Defines a class that combines ``Load``, ``LoadGroup`` and ``LoadCase``
    objects in a single object to simplify the user interface.
    """

    def __init__(self, loads, load_groups, load_cases):
        """

        :param loads:
        :param load_groups:
        :param load_cases:
        """

        raise NotImplementedError

    @property
    def loads(self):
        """

        :return:
        """

        return self._loads

    @loads.setter
    def loads(self, loads):
        """

        :param loads:
        :return:
        """

        self._loads = {}

        self.add_load(loads)

    def add_load(self, load):
        """

        :param load:
        :return:
        """

        raise NotImplementedError

    def del_load(self, load_no = None, load = None):
        """

        :param load_no:
        :param load:
        :return:
        """

        raise NotImplementedError

    @property
    def load_groups(self):
        """

        :return:
        """

        return self._load_groups

    @load_groups.setter
    def load_groups(self, load_groups):
        """

        :param load_groups:
        :return:
        """

        self._load_groups = {}

        self.add_load_groups(load_groups)

    def add_load_groups(self, load_groups):
        """

        :param load_groups:
        :return:
        """

        raise NotImplementedError

    def del_load_groups(self, load_group_no = None, load_group = None):
        """

        :param load_group_no:
        :param load_group:
        :return:
        """

        raise NotImplementedError

    @property
    def load_cases(self):
        """

        :return:
        """

        return self._load_cases

    @load_cases.setter
    def load_cases(self, load_cases):
        """

        :param load_cases:
        :return:
        """

        self._load_cases = {}

        self.add_load_cases(load_cases)

    def add_load_cases(self, load_cases):
        """

        :param load_cases:
        :return:
        """

        raise NotImplementedError

    def del_load_cases(self, load_case_no = None, load_case = None):
        """

        :param load_case_no:
        :param load_case:
        :return:
        """

        raise NotImplementedError

    def __eq__(self, other):
        """
        Override the equality test.
        """

        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __ne__(self, other):
        """
        Override the non-equality test.
        """

        if isinstance(other, self.__class__):
            return not self.__eq__(other)

        return NotImplemented