# coding=utf-8

"""
This module contains a helper class that associates a ``LoadGroup`` with
combination factors.
"""

from LoadGroup import LoadGroup

class GroupFactor:
    """
    This class is a helper class that combines a ``LoadGroup`` with a factor to
    multiply the resulting combinations with.
    """
    pass

    def __init__(self, *, load_group: LoadGroup, group_factor: float = 1.0):
        """
        Constructor for the ``GroupFactor`` object.

        :param load_group: The ``LoadGroup`` object.
        :param group_factor: The factor to multiply the LoadGroup by.
        """

        self.load_group = load_group
        self.group_factor = group_factor

    @property
    def load_group(self) -> LoadGroup:
        """
        Getter for the ``load_group`` property
        """
        return self._load_group

    @load_group.setter
    def load_group(self, load_group: LoadGroup):
        """
        Setter for the ``load_group`` property.

        :param load_group: A ``LoadGroup`` object.
        """

        self._load_group = load_group

    @property
    def group_factor(self) -> float:
        """
        Getter for the ``group_factor`` property.
        :return: The group_factor.
        """

        return self._group_factor

    @group_factor.setter
    def group_factor(self, group_factor: float = 1.0):
        """
        Setter for the ``group_factor`` property.
        :param group_factor: The group_factor.
        """

        self._group_factor = group_factor

    def __str__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.

        return (f'{type(self).__name__}: '
                + f'load_group: {self.load_group}, '
                + f'factor: {self.group_factor}'
                )

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadCase without change.

        return (f'{type(self).__name__}('
                + f'load_group = {repr(self.load_group)}, '
                + f'group_factor = {repr(self.group_factor)}'
                + ')')

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
