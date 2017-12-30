# coding=utf-8

"""
Contains a class to store the resulting load combinations.
"""

class Combination:
    """
    Stores the resulting load combinations output from a ``LoadCase`` object.
    """

    @property
    def load_factors(self):
        return self._load_factors

    @load_factors.setter
    def load_factors(self, load_factors):

        self._load_factors = []
        self.add_load_factor(load_factors)

    def add_load_factor(self, load_factors):
        raise NotImplementedError

    @property
    def combination_title(self):
        raise NotImplementedError

    @property
    def list_load_factors(self):
        raise NotImplementedError

    @property
    def list_loads(self):
        raise NotImplementedError