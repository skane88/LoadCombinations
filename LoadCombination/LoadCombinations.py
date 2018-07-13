# coding=utf-8

"""
This contains a class describing a ``LoadCombinations`` object. This will be
used to combine Loads, LoadGroups and LoadCases together into a single simple
object for use by the end user.
"""

from typing import Union, Dict, List
from LoadCombination.Load import Load
from LoadCombination.LoadGroup import LoadGroup
from LoadCombination.exceptions import (LoadExistsException, LoadNotPresentException,
                                        LoadGroupExistsException, LoadGroupNotPresentException)

class LoadCombinations():
    """
    Defines a class that combines ``Load``, ``LoadGroup`` and ``LoadCase``
    objects in a single object to simplify the user interface.
    """

    def __init__(self):
        """
        Initialise a LoadCombinations object. Initalise empty and use "Add"
        methods etc. to add properties, at least until we know how this is going
        to work.
        """

        self._loads = None
        self._load_groups = None
        self._load_cases = None

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

            if not self.load_exists(load = load):

                # next need to check if the load_no is already used by a
                # non-identical load:

                if load.load_no in self.loads:
                    raise LoadExistsException(f'Attempted to add a load to the'
                                              + f' LoadCombination and an '
                                              + f'existing load shares the '
                                              + f'same load_no'
                                              )

                self._loads[load.load_no] = load
            else:
                raise LoadExistsException(f'Attempted to add a load to the '
                                          + f'LoadCombination that already '
                                          + f'exists. '
                                          + f'Load: {str(load)}, '
                                          + f'self.loads: {str(self._loads)}.')

    def del_load(self, *, load_no: int = None, load: Load = None):
        """
        A method to delete a single load from the self.loads property.

        The load to delete can be specified by either the ``load_no``,
        or a ``Load`` object can be passed in directly. If both are passed an
        error is raised.

        This method does not curently return information on the status of the
        deletion operation. If it is necessary to know if the deletion was
        successful or not the user should ensure they check for it directly.

        :param load_no: The load_no of the load to delete.
        :param load: A ``Load`` object to check for.
        """

        load_present = self.load_exists(load_no = load_no,
                                        load = load)

        if load_present:

            if load_no == None:
                load_no = load.load_no

            self._loads.pop(load_no)

        else:
            raise LoadNotPresentException(f'To delete a Load a Load needs to be'
                                          + f'present. Load not present.')

    def load_exists(self, *, load: Load) -> bool:
        """
        This method searches the self.loads property of the ``LoadGroup`` to
        determine if a ``Load`` exists in it.

        :param load: A ``Load`` object to look for.
        :return: Returns the ``load_no`` of the load if the load is found,
            ``False`` otherwise.
        """

        # can shortcut this method if the self._loads method is empty.
        if len(self._loads) == 0:
            # by default the load cannot exist in an empty dictionary.
            return False

        if load.load_no in self.loads:
            # if load_no is in loads, need to check if loads are identical
            if load == self.loads[load.load_no]:
                return load.load_no
            else:
                return False

        # if haven't found in the dictionary, return False.
        return False

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
                  load_group: Union[LoadGroup,
                                    Dict[str, LoadGroup],
                                    List[LoadGroup]]
                  ):
        """
        Adds a LoadGroup to the LoadCombination

        :param load_group: The ``LoadGroup`` to add.
        """

        if isinstance(load_group, List):
            # if a list of groups, recursively add them individually

            for lg in load_group:
                self.add_group(lg)

        if isinstance(load_group, Dict):
            # if a dictionary of groups, recursively add them individually

            for lg in load_group.values():
                self.add_group(lg)

        if not isinstance(load_group, LoadGroup):
            # raise an error if not a LoadGroup

            raise ValueError(f'Expected a LoadGroup object but instead received'
                             + f' a {type(load_group)}')

        # else we have a single load group

        if self.group_exists(load_group = load_group):
            # if the group already exists, raise an error

            raise LoadGroupExistsException(f'Load group {load_group.group_name}'
                                           + f' already exists.')

        # finally add to the self._load_groups dictionary

        # first check if the loads in the load_group already exist in the
        # LoadCombination

        overwrite = {}

        for l in load_group.loads.values():

            if not self.load_exists(load = l):
                # if load doesn't exist, add to the self.loads dictionary
                # so that any changes to the load reflect to all similar groups

                self.add_load(load = l)
            else:
                # else if the load does exist, need to replace the load in the
                # LoadGroup so that references are the same across the objects

                if l is self.loads[l.load_no]:
                    # they are the same object, so ignore
                    pass

                else:
                    overwrite[l.load_no] = self.loads[l.load_no]

        for load, v in overwrite.items():
            # now actually replace the loads in LoadGroup:
            load_group.loads[l] = v

        # finally add to the self._load_groups dictionary

        self._load_groups[load_group.group_name] = load_group

    def del_group(self, *, group_name: str = None, abbrev: str = None,
                  load_group: LoadGroup = None):
        """
        A method to delete a single ``LoadGroup`` from the ``self.load_groups``
        property.

        The ``LoadGroup`` to delete can be specified by either the
        ``group_name`` or ``abbrev`` properties of the ``LoadGroup``, or a
        ``LoadGroup`` object can be passed in directly.

        Only one parameter should be given otherwise an error is raised.

        This method does not currently return information on the status of the
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

    def group_exists(self,
                     group_name: str = None,
                     load_group: LoadGroup = None) -> Union[bool, str]:
        """
        This method searches the ``self.load_groups`` property of the
        ``LoadCombination`` to determine if a ``LoadGroup`` exists in it.
        It will search by either the ``group_name`` property of
        the ``LoadGroup``, or can search using a given ``LoadGroup`` object.

        Only one parameter should be given otherwise an error is raised.

        :param group_name: The load_name of the load to delete.
        :param load_group: A ``LoadGroup`` object to check for.
        :returns: Either the ``group_name`` of the load_group object (if found)
            or ``False``.
        """

        args = [group_name, load_group]
        sumargs = sum(x is not None for x in args)

        if sumargs == 0:
            raise ValueError('No LoadGroup is provided to search for.')
        elif sumargs > 1:
            raise ValueError('More than one parameter is provided to search for'
                             + ' - provide only a single parameter.')

        if len(self.load_groups) == 0:
            # if load_groups is empty, the result is false by inspection
            return False

        # else need to search for the LoadGroup

        if group_name != None:

            if group_name in self.load_groups:
                return group_name
            else:
                return False

        elif load_group != None:

            if load_group.group_name in self.load_groups:
                # if the load group may be in the load_group dictionary
                # then check if it actually is

                if load_group == self.load_groups[load_group.group_name]:
                    return load_group.group_name

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