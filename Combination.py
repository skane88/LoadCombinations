# coding=utf-8

"""
Contains a class to store the resulting load combinations.
"""

from typing import Dict, List, Tuple, Union
from LoadFactor import LoadFactor
from Load import Load

class Combination:
    """
    Stores the resulting load combinations output from a ``LoadCase`` object.
    """

    def __init__(self, *,
                 load_case_no: int,
                 load_case: str,
                 load_case_abbrev,
                 load_factors:Union[Dict[int, List[LoadFactor]],
                                    List[LoadFactor],
                                    Tuple[LoadFactor,...],
                                    LoadFactor],
                 allow_duplicates: bool = False):
        """

        :param load_case_no: The load case no. of the LoadCase that generated
            the combination
        :param load_case: The title of the load case that generated the
            combination.
        :param load_case_abbrev: The abbreviation for the load case that
            generated the combination.
        :param load_factors: The load_factor to be added. This is expected to be
            a LoadFactor object, or: a Dict[int, List[LoadFactor]] (i.e. in the
            same format as the self.load_factors dictionary), or a
            List[LoadFactor] or Tuple[LoadFactor].
        :param allow_duplicates: A boolean specifying if duplicate load_factors
            are allowed for each load in the combination?
        """

        self.load_case_no = load_case_no
        self.load_case = load_case
        self.load_case_abbrev = load_case_abbrev
        self.allow_duplicates = allow_duplicates
        self.load_factors = load_factors

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

        if isinstance(load_factor, dict):
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

        elif (isinstance(load_factor, list) or
              isinstance(load_factor, tuple)):
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
                             + f'a Dict[int, List[LoadFactor]], '
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

    def del_load(self, load_no: int = None, load_name: str = None,
                 load: Load = None):
        """
        Delete a load from the self.load_factors dictionary entirely.

        Note that the load can be specified via load_no, load_name or directly,
        but if more than one way is provided only the first is actually used.

        :param load_no: The no. of the load to search for.
        :param load_name: The name of the load to search for.
        :param load: A Load object to search for.
        """

        # first test if the load exists at all in the self.load_factors dict.
        ld_exists = self.load_exists(load_no = load_no,
                                     load_name = load_name,
                                     load = load)

        if not ld_exists:
            if load_no != None:
                ld_to_delete = f'Load no: {load_no}'
            elif load_name != None:
                ld_to_delete = f'Load name: {load_name}'
            else:
                ld_to_delete = f'Load: {load}'

            raise ValueError(f'Attempted to delete load: ({ld_to_delete}) from '
                             + f'the self.load_factors dictionary, but it does '
                             + f'not exist. self.load_factors: '
                             + f'{self.load_factors}.')

        # if the load exists, then simply delete the key from the dictionary.
        del self.load_factors[ld_exists]

    def load_exists(self,
                    load_no: int = None,
                    load_name: str = None,
                    load: Load = None) -> Union[bool, int]:
        """
        Search through the self.load_factors dictionary and determine if a load
        exists.

        Note that the load can be specified via load_no, load_name or directly,
        but if more than one way is provided only the first is actually used.

        :param load_no: The no. of the load to search for.
        :param load_name: The name of the load to search for.
        :param load: A Load object to search for.
        :return: Return False if the load does not exist, alternatively return
            the key at which the load exists in the self.load_factor dictionary.
        """

        if load_no != None:
            # if the load_no is provided, a simple key lookup into the
            # self.load_factors dictionary is all that is required.

            if load_no in self.load_factors:
                return load_no
            else:
                return False

        elif load_name != None:
            # if the load_name is provided, then the dictionary needs to be
            # iterated over.

            for k, v in self.load_factors.items():
                # The value is a List[LoadFactor] and therefore will also have
                # to be iterated over

                for LF in v:

                    if LF.load.load_name == load_name:
                        return k

            # only if we iterate entirely through the dictionary do we know that
            # the load does not exist.

            return False

        else:
            # if the load is provided as a Load object, need to iterate through
            # the self.load_factors dictionary.
            # Note that as we have the load, we know the load_no and could
            # simply jump to it, but in case of inappropriately added objects
            # we will brute force search the dictionary.

            for k, v in self.load_factors.items():
                # the value is a List[LoadFactor] and therefore will also have
                # to be iterated over

                for LF in v:

                    if LF.load == load:
                        return k

            # only if we complete the iteration do we know that the load
            # does not exist

            return False

    def load_factor_exists(self, load_factor: LoadFactor) -> Union[bool, int]:
        """
        Determines if a LoadFactor object exists in the self.load_factors
        Dictionary.

        :param load_factor: A LoadFactor object to search for.
        :return: Returns False if the object is not found, otherwise returns the
            key at which the LoadFactor can be found in the self.load_factors
            Dictionary.
        """

        # to determine if load_factor exists, we iterate through the
        # self.load_factors dictionary. Given we have the LoadFactor object we
        # could jump straight to its location in the dictionary, but in case of
        # mis-added objects we will brute force search the dictionary.

        for k, v in self.load_factors.items():
            # The values are a List[LoadFactor] and therefore we need to iterate
            # through these as well:

            for LF in v:
                if LF == load_factor:
                    return k

        # only if we complete our iteration can be return False:
        return False

    @property
    def allow_duplicates(self) -> bool:
        """
        Are duplicate load_factors allowed for each load in the combionation?
        :return: Returns the allow_duplicates property.
        """

        return self._allow_duplicates

    @allow_duplicates.setter
    def allow_duplicates(self, allow_duplicates: bool = False):
        """
        Are duplicate load_factors allowed for each load in the combination?

        :param allow_duplicates: A boolean specifying if duplicate load_factors
            are allowed for each load in the combination?
        """

        self._allow_duplicates = allow_duplicates

    @property
    def load_case(self) -> str:
        """
        Getter / setter for the self.load_case property.

        :return: The title of the load case that generated the combination.
        """

        return self._load_case

    @load_case.setter
    def load_case(self, load_case: str):
        """
        Getter / setter for the self.load_case property.

        :param load_case: The title of the load case that generated the
            combination.
        """

        self._load_case = load_case

    @property
    def load_case_abbrev(self) -> str:
        """
        Getter / setter for the self.load_case_abbrev property

        :return: The abbreviation for the load case that generated the
            combination
        """

        return self._load_case_abbrev

    @load_case_abbrev.setter
    def load_case_abbrev(self, load_case_abbrev: str):
        """
        Getter / setter for the self.load_case_abbrev parameter.

        :param load_case_abbrev: The abbreviation for the load case that
            generated the combination.
        """

        self._load_case_abbrev = load_case_abbrev

    @property
    def load_case_no(self) -> int:
        """
        Getter / setter for the load_case_no property
        :return: Return the load case no. of the LoadCase that generated the
            combination
        """

        return self._load_case_no

    @load_case_no.setter
    def load_case_no(self, load_case_no: int):
        """
        Getter / setter for the load_case_no property.

        :param load_case_no: The load case no. of the LoadCase that generated
            the combination
        """

        self._load_case_no = load_case_no


    def combination_title(self,
                          abbreviate: bool = False,
                          combine_same_loads: bool = True) -> str:
        """
        Generates a title for the combination based on the LoadFactors in it.

        The resulting title will be sorted by the load_no.

        :param abbreviate: Use abbreviations where possible.
        :param combine_same_loads: Where multiple LoadFactors of the same Load
            are included then combine them into a single factor
        :return: Return a title for the combination based on the LoadFactors in
            it.
        """

        title = '' # string for resulting title
        load_list = self.list_loads_with_factors
        load_nos = sorted(load_list.keys())

        for i in load_nos:
            data = load_list[i]

            title_list = []

            if len(data[2]) > 1 and not combine_same_loads:
                # if there are multiple LoadFactors and
                # combine_same_loads is False
                # then we need multiple elements for each load factor

                for LF in data[2]:
                    case_factor = str(LF.factor)

                    if abbreviate:
                        case_title = LF.load.abbrev
                    else:
                        case_title = LF.load.load_name

                    title_list.append(case_factor + case_title)

            else:
                # else we only have 1x name to make

                if abbreviate:
                    case_title = data[1].abbrev
                else:
                    case_title = data[1].load_name

                case_factor = str(data[0])

                title_list.append(case_factor + case_title)

            # now we have a list of loads + factors to add together for the
            # final title

            for t in title_list:
                title += '+' + t

        return title

    @property
    def list_load_factors(self) -> List[LoadFactor]:
        """
        Return a list of all LoadFactors in the combination

        :return: Returns an unsorted list of all LoadFactors in the Combination.
        """

        # simply iterate through the self.load_factors dictionary

        ret_list = []

        for k, v in self.load_factors.items():
            # in case a LoadFactor is repeated in multiple locations
            # (it shouldn't be but you never know...), iterate through the
            # value, which is a List[LoadFactor]

            for LF in v:
                if LF not in ret_list:
                    ret_list.append(LF)

        return ret_list

    @property
    def list_loads(self) -> List[Load]:
        """
        Return a list of all Loads in the combination.

        :return: Returns an unsorted list of all Loads in the combination.
        """

        ret_list = []

        # simply iterate through all the load_factors in the self.load_factors
        # dictionary. Use the self.list_load_factors method to simplify things.
        for LF in self.list_load_factors:

            if LF.load not in ret_list:

                ret_list.append(LF.load)

        return ret_list

    @property
    def list_loads_with_factors(self) -> Dict[int,
                                              Tuple[float,
                                                    Load,
                                                    List[LoadFactor]]]:
        """
        Returns a dictionary containing the loads and the factors applied to
        them.

        :return: Returns a Dictionary of the following format:
            ``{load_no: (factor, Load, List[LoadFactor])}``

            where ``factor`` is the total factor to apply to the load.
        """

        load_dict = {}

        # to build the load list, iterate through all the load factors:

        for LF in self.list_load_factors:

            # if the load is already in the dictionary we just amend the
            # dictionary

            if LF.load.load_no in load_dict:
                exist = load_dict[LF.load.load_no]

                factor = exist[0]
                load = exist[1]
                lfs = exist[2]

                new_factor = factor + LF.factor
                new_lfs = lfs.append(LF)

                new = (new_factor, load, new_lfs)

                load_dict[LF.load.load_no] = new

            else:
                # else we create the entry in the load dictionary

                load_dict[LF.load.load_no] = (LF.factor, LF.load, [LF])

        return load_dict