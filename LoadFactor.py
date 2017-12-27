# coding=utf-8

"""
This file contains a helper class to associate a ``Load`` with combination
factors.
"""


class LoadFactor:
    """
    This class is a helper class that combines a ``Load`` with factors for the
    final combination.
    """

    @property
    def load(self):
        """
        Getter for the ``load`` property
        :return: The ``Load`` object associated with the factor.
        """

        return self._load

    @load.setter
    def load(self, load: Load):
        """
        Setter for the ``load`` property
        :param load: The ``Load`` to associate with the factors
        """

        self._load = load
