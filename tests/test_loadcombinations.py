# coding=utf-8

from unittest import TestCase
from LoadCombination.LoadCombinations import LoadCombinations
from LoadCombination.Load import Load
from LoadCombination.LoadGroup import LoadGroup
from LoadCombination.GroupFactor import GroupFactor
from LoadCombination.LoadCase import LoadCase
from LoadCombination.exceptions import (LoadExistsException,
                                        LoadNotPresentException)

class TestLoadCombination(TestCase):

    def test_loadcombination_basic(self):
        """
        Basic test for the class - can it even be instantiated?
        """

        LC = LoadCombinations()

        print(LC)

        print(repr(LC))

    def test_add_load(self):
        """
        Test the add_load method.
        """

        l1 = Load(load_name='Load 1',
                  load_no=1,
                  abbrev='l1')

        l2 = Load(load_name='Load 2',
                  load_no=2,
                  abbrev='l2')

        l3 = Load(load_name='Load 3',
                  load_no=3,
                  abbrev='l3')

        LC = LoadCombinations()

        LC.add_load(l1)
        LC.add_load(l2)

        loads = {1: l1,
                 2: l2}

        self.assertEqual(first=loads, second=LC.loads)

        # test adding a list

        list_loads = [l1, l3]

        LC.loads = {}
        LC.add_load(list_loads)

        loads = {1: l1,
                 3: l3}

        self.assertEqual(first=loads, second=LC.loads)

        # test adding a dictionary

        loads = {2: l2,
                 3: l3}

        LC.loads = {}
        LC.add_load(loads)

        self.assertEqual(first=loads, second=LC.loads)

        # check that it raises an error if trying to add something that already
        # exists.

        self.assertRaises(LoadExistsException, LC.add_load, l2)

        # check that it raises an error if trying to add a load that has a no.
        # that matches something already in the dictionary

        le = Load(load_name='Cause Error',
                  load_no=2,
                  abbrev='CE')

        self.assertRaises(LoadExistsException, LC.add_load, le)

    def test_del_load(self):
        """
        Test the del_load method.
        """

        l1 = Load(load_name='Load 1',
                  load_no=1,
                  abbrev='l1')

        l2 = Load(load_name='Load 2',
                  load_no=2,
                  abbrev='l2')

        l3 = Load(load_name='Load 3',
                  load_no=3,
                  abbrev='l3')

        LC = LoadCombinations()

        LC.add_load(l1)
        LC.add_load(l2)
        LC.add_load(l3)

        loads = {1: l1,
                 2: l2}

        LC.del_load(load_no=3)

        self.assertEqual(first=loads, second=LC.loads)

        loads = {1: l1}

        LC.del_load(load=l2)

        self.assertEqual(first=loads, second=LC.loads)

        # Test for error if trying to delete load that isn't present

        self.assertRaises(LoadNotPresentException, LC.del_load, load_no=3)
        self.assertRaises(LoadNotPresentException, LC.del_load, load=l3)

    def test_load_no_exists(self):
        """
        The the load_no_exists method.
        """

        l1 = Load(load_name='Load 1',
                  load_no=1,
                  abbrev='l1')

        l2 = Load(load_name='Load 2',
                  load_no=2,
                  abbrev='l2')

        l3 = Load(load_name='Load 3',
                  load_no=3,
                  abbrev='l3')

        LC = LoadCombinations()

        LC.add_load(l1)
        LC.add_load(l2)

        self.assertTrue(LC.load_no_exists(load_no=1))
        self.assertTrue(LC.load_no_exists(load=l1))
        self.assertFalse(LC.load_no_exists(load_no=3))
        self.assertFalse(LC.load_no_exists(load=l3))

    def test_load_exists(self):
        """
        The the load_exists method.
        """

        l1 = Load(load_name='Load 1',
                  load_no=1,
                  abbrev='l1')

        l2 = Load(load_name='Load 2',
                  load_no=2,
                  abbrev='l2')

        l3 = Load(load_name='Load 3',
                  load_no=3,
                  abbrev='l3')

        le = Load(load_name='Load Error',
                  load_no=1,
                  abbrev='LE')

        LC = LoadCombinations()

        LC.add_load(l1)
        LC.add_load(l2)

        self.assertTrue(LC.load_exists(load=l1))
        self.assertFalse(LC.load_exists(load=le))
        self.assertFalse(LC.load_exists(load=l3))
