# coding=utf-8

"""
This file contains a LoadCase class, that will contain a collection of
LoadGroup objects and use them to output relevant load combinations within the
case.
"""

class LoadCase:
    """
    A LoadCase object contains a set of LoadGroup objects and uses them to
    generate appropriate load combinations.
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
    def load_groups(self):
        return self._load_groups

    @load_groups.setter
    def load_groups(self, load_groups):
        self._load_groups = load_groups

    def add_load_group(self):
        raise NotImplementedError

    def remove_load_group(self):
        raise NotImplementedError
