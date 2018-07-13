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

        LC = LoadCombinations()

        print(LC)

        print(repr(LC))