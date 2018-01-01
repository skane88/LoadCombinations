# coding=utf-8

"""
Contains a class to store the resulting load combinations.
"""

from typing import Dict, List, Tuple, Union
from LoadFactor import LoadFactor

class Combination:
    """
    Stores the resulting load combinations output from a ``LoadCase`` object.
    """

    @property
    def load_factors(self) -> Dict[int, List[LoadFactor]]:
        """
        Returns the self.load_factors dictionary.

        :return: Returns a dictionary containing the load factors in the format
            Dict[int, List[LoadFactor]] where int is the load number for each
            LoadFactor.
        """

        return self._load_factors

    @load_factors.setter
    def load_factors(self, load_factors: Union[Dict[int, List[LoadFactor]],
                                               List[LoadFactor],
                                               Tuple[LoadFactor,...],
                                               LoadFactor]):
        """
        Sets the self.load_factors property.

        :param load_factors: The load_factor to be added. This is expected to be
            a LoadFactor object, or: a Dict[int, List[LoadFactor]] (i.e. in the
            same format as the self.load_factors dictionary), or a
            List[LoadFactor] or Tuple[LoadFactor].
        """

        self._load_factors = {}
        self.add_load_factor(load_factors)

    def add_load_factor(self, load_factor: Union[Dict[int, List[LoadFactor]],
                                                 List[LoadFactor],
                                                 Tuple[LoadFactor,...],
                                                 LoadFactor]
                        ):
        """
        Adds a load_factor to the self.load_factors dictionary.

        :param load_factor: The load_factor to be added. This is expected to be
            a LoadFactor object, or: a Dict[int, List[LoadFactor]] (i.e. in the
            same format as the self.load_factors dictionary), or a
            List[LoadFactor] or Tuple[LoadFactor].
        """

        if isinstance(load_factor, Dict[int, List[LoadFactor]]):
            # if the load_factor list is supplied as a dictionary that already
            # matches the expected format for self._load_factors, then check
            # that load_factors already exists.

            if len(self._load_factors) == 0:
                # if it doesn't, can simply assign load_factors to _load_factors

                self._load_factors = load_factor

            else:
                # otherwise, iterate through the items and recursively call this
                # method

                for k, v in load_factor.items():
                    self.add_load_factor(v)

        elif (isinstance(load_factor, List[LoadFactor]) or
              isinstance(load_factor, Tuple[LoadFactor,...])):
            # if a list of items, recursively call this method on each item.

            for i in load_factor:
                self.add_load_factor(i)

        elif isinstance(load_factor, LoadFactor):
            # if a single load factor then add it to the LoadFactor dictionary
            # based on the rules about allowing multiple LoadFactors etc.

            # first check if the load in the load_factor exists:

            if self.load_exists(load = load_factor.load):
                # if it does, and multiple loads are not allowed, raise an error

                if not self.allow_duplicates:
                    raise ValueError(f'Load already exists and Combination does'
                                     + f' not allow duplicates.')
                # if duplicates are allowed, need to append load factor to
                # load factor dictionary list

                self._load_factors[load_factor.load.load_no].append(load_factor)

            else:
                # if the load doesn't already exist, then need to add the
                # LoadFactor to the dictionary

                self._load_factors[load_factor.load.load_no] = [load_factor]

        else:
            raise ValueError(f'Expected either a LoadFactor object to add, or '
                             + f'a Dict[int, List[LoadFactor]], ''
                             + f'List[LoadFactor] or a Tuple[LoadFactor,...]. '
                             + f'Actual value received was: {load_factor}')

    def del_load_factor(self, load_factor: LoadFactor):
        """
        Deletes all copies of a LoadFactor from the self.load_factors
        dictionary.

        :param load_factor: The LoadFactor object to remove from the
            self.load_factors dictionary.
        """

        # first test if the load_factor exists at all:
        lf_exists = self.load_factor_exists(load_factor = load_factor)

        if not lf_exists:
            raise ValueError(f'Attempted to delete {load_factor} but it does '
                             + f'not exist in the self.load_factors Dict: '
                             + f'{self.load_factors}')

        # if the load factor exists, then need to delete it from the
        # self.load_factors dictionary. Using a While loop to account for
        # the presence of multiple copies of load_factors if
        # self.allow_duplicates is true.
        while load_factor in self.load_factors[lf_exists]:
            self.load_factors[lf_exists].remove(load_factor)

    def del_load(self, load_no = None, load_name = None, load = None):
        raise NotImplementedError

    def load_exists(self, load_no = None, load_name = None, load = None):
        raise NotImplementedError

    def load_factor_exists(self, load_factor):
        raise NotImplementedError

    @property
    def allow_duplicates(self) -> bool:
        """

        :return:
        """

        return self._allow_duplicates

    @allow_duplicates.setter
    def allow_duplicates(self, allow_duplicates: bool = False):
        self._allow_duplicates = allow_duplicates


    @property
    def combination_title(self):
        raise NotImplementedError

    @property
    def list_load_factors(self):
        raise NotImplementedError

    @property
    def list_loads(self):
        raise NotImplementedError