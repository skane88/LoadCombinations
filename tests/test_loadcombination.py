# coding=utf-8

from unittest import TestCase
from LoadCombination.LoadCombinations import LoadCombinations
from LoadCombination.Load import Load
from LoadCombination.LoadGroup import LoadGroup
from LoadCombination.GroupFactor import GroupFactor
from LoadCombination.LoadCase import LoadCase

class TestLoadCombination(TestCase):

    def test_loadcombination_basic(self):
        """
        Basic test for the class - can it even be instantiated?
        """

        l1 = Load(load_name='Test Load',
                  load_no=1,
                  abbrev='TL1')

        LG1 = LoadGroup(group_name='Test Group',
                        loads=l1,
                        abbrev="TG")

        LC1 = LoadCase(case_name='Case 1',
                       case_no = 1,
                       load_groups= GroupFactor(load_group = LG1,
                                                group_factor=1.5)
                       )



        self.fail()