# coding=utf-8

"""
This file contains a LoadCase class, that will contain a collection of
LoadGroup objects and use them to output relevant load combinations within the
case.
"""

from typing import Dict, List, Union
from LoadGroup import LoadGroup
from exceptions import LoadGroupExistsException, LoadGroupNotPresentException

class LoadCase:
    """
    A ``LoadCase`` object contains a set of ``LoadGroup`` objects and uses them
    to generate appropriate load combinations.
    """

    @property
    def case_name(self) -> str:
        return self._case_name

    @case_name.setter
    def case_name(self, case_name: str):
        self._case_name = case_name

    @property
    def case_no(self) -> int:
        return self._case_no

    @case_no.setter
    def case_no(self, case_no: int):
        self._case_no = case_no

    @property
    def load_groups(self) -> :
        return self._load_groups

    @load_groups.setter
    def load_groups(self,
                    load_group: Union[Dict[str, LoadGroup],
                                      List[LoadGroup], LoadGroup]):
        self._load_groups = {}

        self.add_group(load_group)

    def add_group(self,
                  load_group: Union[Dict[str, LoadGroup],
                                         List[LoadGroup], LoadGroup]):

        if isinstance(load_group, Dict):

            for k, lg in load_group:
                self.add_group(lg)

        elif isinstance(load_group, List):

            for lg in load_group:
                self.add_group(lg)

        else:

            if self.group_exists(load_group) == False:
                self._load_groups[load_group.group_name] = load_group
            else:
                raise LoadGroupExistsException(f'Attempted to add a LoadGroup'
                                               + f' that already exists to the'
                                               + f' LoadCase. '
                                               + f'LoadGroup: {str(load_group)}'
                                               + f', LoadCase.load_groups:'
                                               + f' {str(self.load_groups)}.')

    def del_group(self, group_name: str = None,
                       load_group: LoadGroup = None):

        group_present = self.group_exists(group_name = group_name,
                                          load_group = load_group)

        if group_present != False:
            self._load_groups.pop(group_present)
        else:
            raise LoadGroupNotPresentException(f'Attempted to delete LoadGroup'
                                               + f' which did not exist.')

    def group_exists(self, group_name: str = None,
                     load_group: LoadGroup = None):

        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
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

