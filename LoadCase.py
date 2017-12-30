# coding=utf-8

"""
This file contains a LoadCase class, that will contain a collection of
LoadGroup objects and use them to output relevant load combinations within the
case.
"""

from typing import Dict, List, Union, Tuple
from LoadGroup import LoadGroup
from exceptions import (LoadGroupExistsException, LoadGroupNotPresentException,
                        InvalidCombinationFactor)
from GroupFactor import GroupFactor
import itertools

class LoadCase:
    """
    A ``LoadCase`` object contains a set of ``LoadGroup`` objects and uses them
    to generate appropriate load combinations.
    """

    def __init__(self, *, case_name: str, case_no: int,
                 load_groups: Union[Dict[str, GroupFactor],
                                          List[GroupFactor],
                                          GroupFactor],
                 abbrev: str = ''):
        """
        The constructor for a ``LoadCase`` object.

        :param case_name: The ``LoadCase`` name.
        :param case_no: The ``LoadCase`` ``case_no``.
        :param load_groups: The ``load_groups`` to add to the ``LoadCase``.
            This should be a dictionary of the following format:

            ``{group_name: GroupFactor}``

            where ``GroupFactor`` is a ``GroupFactor`` object containing a
            ``LoadGroup`` object and the factor to be applied to the
            results from the ``LoadGroup.generate_groups`` method.
            I.e. for a LoadCase which is 1.35 x Dead Load + 1.5 x Live Load
            the load_groups would be:

            ``{'Dead Load': (Dead Load LoadGroup, 1.35),
               'Live Load': (Live Load LoadGroup, 1.50)}``.

            Alternatively a List of ``[GroupFactor, ...]``
            or a single ``GroupFactor`` can be provided.
        :param abbrev: The abbreviation of the ``LoadCase``.
        """

        self.case_name = case_name
        self.case_no = case_no
        self.load_groups = load_groups
        self.abbrev = abbrev

    @property
    def case_name(self) -> str:
        """
        Get / set the ``LoadCase`` name.

        :return: The ``LoadCase`` name.
        """

        return self._case_name

    @case_name.setter
    def case_name(self, case_name: str):
        """
        Get / set the ``LoadCase`` name.

        :param case_name: The ``LoadCase`` name.
        """

        self._case_name = case_name

    @property
    def case_no(self) -> int:
        """
        Get/set the ``LoadCase`` ``case_no``.

        :return: The ``LoadCase`` ``case_no``.
        """

        return self._case_no

    @case_no.setter
    def case_no(self, case_no: int):
        """
        Get/set the ``LoadCase`` ``case_no``.

        :param case_no: The ``LoadCase`` ``case_no``.
        """

        self._case_no = case_no

    @property
    def load_groups(self) -> Dict[str, GroupFactor]:
        """
        Get / set the ``LoadCase`` ``load_groups``.

        :return: The ``load_groups`` in the ``LoadCase``.
            This will be a dictionary of the following format:

            ``{group_name: GroupFactor}``

            where ``GroupFactor`` is a ``GroupFactor`` object containing a
            ``LoadGroup`` object and the factor to be applied to the
            results from the ``LoadGroup.generate_groups`` method.
            I.e. for a LoadCase which is 1.35 x Dead Load + 1.5 x Live Load
            the load_groups would be:

            ``{'Dead Load': (Dead Load LoadGroup, 1.35),
               'Live Load': (Live Load LoadGroup, 1.50)}``.
        """

        return self._load_groups

    @load_groups.setter
    def load_groups(self,
                    load_groups: Union[Dict[str, GroupFactor],
                                          List[GroupFactor],
                                          GroupFactor]
                    ):
        """
        Get / set the ``LoadCase`` ``load_groups``.

        :param load_groups: The ``load_groups`` to add to the ``LoadCase``.
            This should be a dictionary of the following format:

            ``{group_name: GroupFactor}``

            where ``GroupFactor`` is a ``GroupFactor`` object containing a
            ``LoadGroup`` object and the factor to be applied to the
            results from the ``LoadGroup.generate_groups`` method.
            I.e. for a LoadCase which is 1.35 x Dead Load + 1.5 x Live Load
            the load_groups would be:

            ``{'Dead Load': (Dead Load LoadGroup, 1.35),
               'Live Load': (Live Load LoadGroup, 1.50)}``.

            Alternatively a List of ``[GroupFactor, ...]``
            or a single ``GroupFactor`` can be provided.
        """

        # if setting via load_groups, the assumption is that the entire
        # self._load_groups object is being overwritten:

        self._load_groups = {}

        # use the add_group method to add LoadGroups, to check for duplicates
        # etc.

        self.add_group(load_groups)

    def add_group(self,
                  load_group: Union[Dict[str, GroupFactor],
                                          List[GroupFactor],
                                          GroupFactor]
                  ):
        """
        Add a ``LoadGroup`` into the LoadCase.
        :param load_group: The ``load_groups`` to add to the ``LoadCase``.
            This should be a dictionary of the following format:

            ``{group_name: GroupFactor}``

            where ``GroupFactor`` is a ``GroupFactor`` object containing a
            ``LoadGroup`` object and the factor to be applied to the
            results from the ``LoadGroup.generate_groups`` method.
            I.e. for a LoadCase which is 1.35 x Dead Load + 1.5 x Live Load
            the load_groups would be:

            ``{'Dead Load': (Dead Load LoadGroup, 1.35),
               'Live Load': (Live Load LoadGroup, 1.50)}``.

            Alternatively a List of ``[GroupFactor, ...]``
            or a single ``GroupFactor`` can be provided.
        """

        if isinstance(load_group, Dict):

            for k, lg in load_group.items():
                self.add_group(lg)

        elif isinstance(load_group, List):

            for lg in load_group:
                self.add_group(lg)

        else:

            if not isinstance(load_group, GroupFactor):
                # raise error if the load_group object isn't a GroupFactor
                # object.

                raise InvalidCombinationFactor(f'Expected load_group to be '
                                               + f'a GroupFactor object. '
                                               + f' Actual value: {load_group}.'
                                               )

            if not isinstance(load_group.load_group, LoadGroup) \
                    or not isinstance(load_group.group_factor, float):
                # next raise error if the first or last values are not
                # a LoadGroup or a float

                raise InvalidCombinationFactor(f'Expected load_group to be '
                                               + f'a GroupFactor object. '
                                               + f' Actual value: {load_group}.'
                                               )


            if self.group_exists(load_group = load_group.load_group) == False:

                self._load_groups[load_group.load_group.group_name] = load_group

            else:

                raise LoadGroupExistsException(f'Attempted to add a LoadGroup'
                                               + f' that already exists to the'
                                               + f' LoadCase. LoadGroup:'
                                               + f' {str(load_group.load_group)}'
                                               + f', LoadCase.load_groups:'
                                               + f' {str(self.load_groups)}.')

    def del_group(self, *, group_name: str = None, abbrev: str = None,
                  load_group: LoadGroup = None):
        """
        A method to delete a single ``LoadGroup`` from the ``self.load_groups``
        property.

        The ``LoadGroup`` to delete can be specified by either the
        ``group_name`` or ``abbrev`` properties of the ``LoadGroup``, or a
        ``LoadGroup`` object can be passed in directly.

        It should be noted that if more than one parameter is given the search
        will only be carried out based on the first provided parameter -
        providing multiple parameters does not result in a search by multiple
        parameters.

        This method does not curently return information on the status of the
        deletion operation. If it is necessary to know if the deletion was
        successful or not the user should ensure they check for it directly.

        :param group_name: The load_name of the load to delete.
        :param abbrev:  The abbreviation of the load to delete.
        :param load_group: A ``LoadGroup`` object to check for.
        """

        group_present = self.group_exists(group_name = group_name,
                                          abbrev = abbrev,
                                          load_group = load_group)

        if group_present != False:
            self._load_groups.pop(group_present)

        else:
            raise LoadGroupNotPresentException(f'Attempted to delete LoadGroup'
                                               + f' which did not exist.')

    def group_exists(self, *, group_name: str = None, abbrev: str = None,
                     load_group: LoadGroup = None):
        """
        This method searches the ``self.load_groups`` property of the
        ``LoadCase`` to determine if a ``LoadGroup`` exists in it.
        It will search by either the ``group_name`` or ``abbrev`` properties of
        the ``LoadGroup``, or can search using a given ``LoadGroup`` object.

        It should be noted that if  more than one parameter is given the search
        will only be carried out based on the first provided parameter -
        providing multiple parameters does not result in a search by multiple
        parameters.

        :param group_name: The load_name of the load to delete.
        :param abbrev:  The abbreviation of the load to delete.
        :param load_group: A ``LoadGroup`` object to check for.
        :returns: Either the ``group_name`` of the load_group object (if found)
            or ``False``.
        """

        # if the self._load_groups property is empty the load_group obviously
        # cannot exist.

        if len(self.load_groups) == 0:
            return False

        # else need to search for the LoadGroup

        if group_name != None:

            if group_name in self.load_groups:
                return group_name
            else:
                return False

        elif abbrev != None:
            # if abbrev is provided, need to search all items:

            for k, lg in self.load_groups.items():

                if abbrev == lg.load_group.abbrev:
                    return k

            # else haven't found so return false
            return False

        elif load_group != None:

            for k, lg in self.load_groups.items():

                if load_group.group_name == k or lg.load_group == load_group:
                    return k

            # else haven't found it so return False
            return False

        else:
            raise ValueError(f'To check if a LoadGroup exists a LoadGroup needs'
                             + f' to be provided. No information provided.')

    def get_factor(self, *, group_name: str = None,
                   load_group: LoadGroup = None) -> float:
        """
        Gets the ``load_factor`` for a given ``LoadGroup`` from the
        ``self.load_groups`` dictionary.

        The ``LoadGroup`` can either be specified by the ``group_name`` or a
        ``LoadGroup`` object can be provided directly.

        :param group_name: The ``group_name`` of the ``LoadGroup`` for which the
            ``load_factor is required.
        :param load_group: A ``LoadGroup`` object for which the ``load_factor``
            is required.
        :return: Returns the ``load_factor`` for the ``LoadGroup`` specified.
        """

        if load_group != None:

            group_name = self.group_exists(load_group = load_group)

        elif group_name == None:
            # if both load_group and group_name == None then we cannot get
            # the load_factor and need to raise an error.

            raise ValueError(f'To get a load_factor a LoadGroup needs to be '
                             + f'specified - none specified.')

        return self.load_groups[group_name].group_factor


    def set_factor(self, *, group_name: str = None,
                   load_group: LoadGroup = None,
                   load_factor: float = 1.0):
        """
        Sets the ``load_factor`` in the ``self.load_groups`` dictionary for a
        given ``LoadGroup``.

        The ``LoadGroup`` can either be specified by the ``group_name`` or a
        ``LoadGroup`` object can be provided directly.

        :param group_name: The ``group_name`` of the ``LoadGroup`` for which the
            ``load_factor is required.
        :param load_group: A ``LoadGroup`` object for which the ``load_factor``
            is required.
        :param load_factor: The ``load_factor`` for the specified ``LoadGroup``
        """

        if load_group != None:

            group_name = self.group_exists(load_group = load_group)

        elif group_name == None:
            # if both load_group and group_name == None then we cannot get
            # the load_factor and need to raise an error.

            raise ValueError(f'To get a load_factor a LoadGroup needs to be '
                             + f'specified - none specified.')

        self._load_groups[group_name].group_factor = load_factor

    @property
    def abbrev(self) -> str:
        """
        The abbreviation of the ``LoadCase``.

        :return: The abbreviation of the ``LoadCase``.
        """
        return self._abbrev

    @abbrev.setter
    def abbrev(self, abbrev: str):
        """
        The abbreviation of the ``LoadCase``.

        :param abbrev: The abbreviation of the ``LoadCase``.
        """

        self._abbrev = abbrev

    def generate_cases(self):
        """
        Generates a generator that generates ``LoadCombination`` objects, which
        generates all possible load combinations from the case.

        :return: Returns a generator which generates all possible load
            combinations from the case.
        """

        # first generate a list of all possible combinations then return them
        # in the generator.

        group_list = []

        for k, g in self.load_groups.items():

            # from each item in the list, make a temporary list. This will be a
            # list of the following format:
            # [(LF1, ..., LFn), (LF1, ..., LFn)]
            # where each Tuple contains 1 or more ``LoadFactor`` objects, and
            # corresponds to a separate group of possible loads that come out
            # of the group.

            temp_list = list(g.load_group.generate_groups(group_factor = g.group_factor))

            # if the list has a length of 0 then just skip to the next group
            if len(temp_list) == 0:
                continue

            # finally add the list to the group_list
            group_list.append(temp_list)

        # we now have a list of all load factors that are output from the
        # ``LoadGroups``, updated with the appropriate group_factors.
        # we then need to develop all the possible combinations.

        # first throw error if no combinations available at all.
        if len(group_list) == 0:
            raise ValueError(f'Expected at least 1x combination. No '
                             + f'combinations generated.')

        print(group_list)

        # next generate a list to output the combinations

        i = 1

        for g in group_list:

            i *= len(g)

        comb_list = []

        for j in range(i):
            comb_list.append([])

        print(comb_list)

        # next, go through the list and append the group load factors
        # by cycling through each element in the group_list. This will ensure.
        # that the full list of combinations is generated.

        for g in group_list:
            cycle = itertools.cycle(g)
            for i in comb_list:
                i.append(next(cycle))

        # we now have combinations that are in the following format:
        # [[(LF1, ..., LFn), ...,(LF1, ..., LFn)],[(), ...()]
        # where each list is a separate possible combination.

        # these combinations now need to be flattened if possible.
        for c in comb_list:
            c = list(itertools.chain(*c))
            print(c)

        # we should now have a list of lists, containing the possible
        # combinations in the load:
        # [[combination_1], ..., [combination_n]]

        raise NotImplementedError

    def __str__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.

        return (f'{type(self).__name__}: '
                + f'{self.case_name}, '
                + f'loads: {self.load_groups}')

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadCase without change.

        return (f'{type(self).__name__}('
                + f'case_name = {repr(self.case_name)}, '
                + f'case_no = {repr(self.case_no)}, '
                + f'load_groups = {repr(self.load_groups)}, '
                + f'abbrev = {repr(self.abbrev)}'
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
