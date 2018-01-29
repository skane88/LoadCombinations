# coding=utf-8

"""
This contains a class describing a ``LoadCombinations`` object. This will be
used to combine Loads, LoadGroups and LoadCases together into a single simple
object for use by the end user.
"""

from typing import Union, Dict, List, Tuple
from Load import Load
from LoadGroup import LoadGroup
from exceptions import (LoadExistsException, LoadNotPresentException,
                        InvalidCombinationFactor)

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

    def add_load(self, load: Union[Load, Dict[int, Load], List[Load]]
                 ):
        """
        A method to add loads into the self.loads that make up the group,
        without having to overwrite the entire self.loads dictionary.

        :param load: The load to add. Can be a single ``Load`` object, a
            ``Dict[int, Load]`` or a ``List[Load]``.
        """

        if isinstance(load, Dict):

            # iterate through all the dictionary items and add_load
            for k in load:
                self.add_load(load[k])

        elif isinstance(load, List):
            # if the load is a List then iterate through the List and add all
            # loads.

            for l in load:
                self.add_load(l)

        else:
            #first check if the load exists in the self._loads dictionary

            if self.load_exists(load = load) == False:
                self._loads[load.load_no] = load
            else:
                raise LoadExistsException(f'Attempted to add a load to the '
                                          + f'LoadGroup that already exists. '
                                          + f'Load: {str(load)}, '
                                          + f'self.loads: {str(self._loads)}.')

    def del_load(self, *, load_no: int = None, load_name: str = None,
                    abbrev: str = None, load: Load = None):
        """
        A method to delete a single load from the self.loads property.

        The load to delete can be specified by either the ``load_no``,
        ``load_name`` or ``abbrev`` properties of the ``Load``, or a ``Load``
        object can be passed in directly. It should be noted that if
        more than one parameter is given the search will only be carried out
        based on the first provided parameter - providing multiple parameters
        does not result in a search by multiple parameters.

        This method does not curently return information on the status of the
        deletion operation. If it is necessary to know if the deletion was
        successful or not the user should ensure they check for it directly.

        :param load_no: The load_no of the load to delete.
        :param load_name: The load_name of the load to delete.
        :param abbrev:  The abbrev of the load to delete.
        :param load: A ``Load`` object to check for.
        """

        load_present = self.load_exists(load_no = load_no,
                                        load_name = load_name,
                                        abbrev = abbrev,
                                        load = load)

        if load_present != False:

            self._loads.pop(load_present)

        else:
            raise LoadNotPresentException(f'To delete a Load a Load needs to be'
                                          + f'present. Load not present.')

    def load_exists(self, *, load_no: int = None, load_name: str = None,
                    abbrev: str = None, load: Load = None) -> Union[bool, int]:
        """
        This method searches the self.loads property of the ``LoadGroup`` to
        determine if a ``Load`` exists in it. It will search by either the
        ``load_no``, ``load_name`` or ``abbrev`` properties of the ``Load``, or
        can search using a given ``Load`` object. It should be noted that if
        more than one parameter is given the search will only be carried out
        based on the first provided parameter - providing multiple parameters
        does not result in a search by multiple parameters.

        :param load_no: The ``load_no`` of the load to check.
        :param load_name: The ``load_name`` of the load to check.
        :param abbrev: The ``abbrev`` of the load to check.
        :param load: A ``Load`` object to look for.
        :return: Returns the ``load_no`` of the load if the load is found,
            ``False`` otherwise.
        """

        # can shortcut this method if the self._loads method is empty.
        if len(self._loads) == 0:
            # by default the load cannot exist in an empty dictionary.
            return False

        if load_no != None:
            # if provided the load no. the search is via the key of the
            # self._load dictionary

            if load_no in self._loads:
                return load_no
            else:
                return False

        elif load_name != None:
            # if provided with the load name, the search needs to go through all
            # the items in the dictionary

            for k, l in self._loads.items():

                if load_name == l.load_name:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        elif abbrev != None:
            # similar with abbrev, the search needs to go through all the items
            # in the dictionary

            for k, l in self._loads.items():
                if abbrev == l.abbrev:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        elif load != None:
            # if provided a load we have to search through all the items in the
            # self._loads dictionary to check for it.

            for k, l in self._loads.items():

                # to avoid silently closing this method if loads share the same
                # load_no we need to return the load_no if either of the
                # following are true:
                # the load_no is the same as an existing load_no OR
                # the load is == to an existing load.

                if load.load_no == k or load == l:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        else:
            raise ValueError(f'To check if a Load exists a Load needs to be'
                             + f'provided. No load information provided.')

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

        # use the add_group method to add LoadGroups, to check for duplicates
        # etc.

        self.add_group(load_groups)

    def add_group(self,
                  load_group: Union[Dict[str, LoadGroup],
                                          List[LoadGroup],
                                          LoadGroup]):
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

            if not isinstance(load_group, LoadGroup):
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
        """"
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

        self.add_case(load_cases)

    def add_case(self, load_cases):
        """

        :param load_cases:
        :return:
        """

        raise NotImplementedError

    def del_case(self, load_case_no = None, load_case = None):
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