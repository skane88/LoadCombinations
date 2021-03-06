# coding=utf-8

"""
Unit test for the LoadGroup class.
"""

from unittest import TestCase
from LoadCombination.LoadGroup import LoadGroup, LoadFactor
from LoadCombination.Load import Load, RotatableLoad, ScalableLoad, WindLoad
from LoadCombination.exceptions import LoadExistsException, LoadNotPresentException


class TestLoadGroup(TestCase):

    def test_loadGroup_basic(self):
        """
        Test basic functionality - can the class be instantiated and can the
        __str__ and __repr__ methods be used.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        print(LG)

        # can the repr method instantiate a load group?
        LG2 = eval(repr(LG))

        print(LG2)

        # does the str method work?

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_loadGroup_group_name(self):
        """
        Test the group_name getter / setter.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.group_name, second = group_name)

        group_name = 'Group 2'
        LG.group_name = group_name

        self.assertEqual(first = LG.group_name, second = group_name)

    def test_loadGroup_loads(self):
        """
        Test the loads getter / setter
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = {1: l1, 2: l2, 3: l3, 4: l4}
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.loads, second = loads)

        loads = {1: l1, 2: l2}

        LG.loads = loads

        self.assertEqual(first = LG.loads, second = loads)

    def test_loadGroup_abbrev(self):
        """
        Test the abbrev getter / setter
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.abbrev, second = abbrev)

        abbrev = 'GP 2'

        LG.abbrev = abbrev

        self.assertEqual(first = LG.abbrev, second = abbrev)

    def test_loadGroup_generate_cases(self):
        """
        Test the generate_groups method.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        # next build the list of expected return loads. This is simply all of
        # the loads in a LoadFactor object.

        LF1 = LoadFactor(load = l1, base_factor = 1.0)
        LF2 = LoadFactor(load = l2, base_factor = 1.0)
        LF3 = LoadFactor(load = l3, base_factor = 1.0)
        LF4 = LoadFactor(load = l4, base_factor = 1.0)

        # create a tuple of load factors. This is one "load combination"
        LC = (LF1, LF2, LF3, LF4)
        LC = (LC,)  # wrap in another tuple because the default generator method
                    # should return a list of load combinations. In this case,
                    # for a basic load group there is only 1x combination but
                    # for consistency through classes return a tuple of all
                    # possible load combinations.

        print(LC)
        print(tuple(LG.generate_groups()))

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)

    def test_loadGroup_add_load(self):
        """
        Test the add_load method.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0,
                      symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = []
        abbrev = 'GP 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.loads, second = {})

        LG.add_load(l1)

        loads = {1: l1}

        self.assertEqual(first = LG.loads, second = loads)

        LG.add_load(l2)

        loads = {1: l1, 2: l2}

        self.assertEqual(first = LG.loads, second = loads)

        LG.add_load([l3, l4])

        loads = {1: l1, 2: l2, 3: l3, 4: l4}

        self.assertEqual(first = LG.loads, second = loads)

        LG.loads = {}

        self.assertEqual(first = LG.loads, second = {})

        LG.loads = loads

        self.assertEqual(first = LG.loads, second = loads)

    def test_loadGroup_add_load_exception(self):
        """
        Test the add_load method raises an exception when adding an already
        existing load.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0,
                      symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'GP 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertRaises(LoadExistsException, LG.add_load, l4)

    def test_loadGroup_del_load(self):
        """
        Test the del_load method
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0,
                      symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'GP 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        LG.del_load(load = l4)

        loads = {1: l1, 2: l2, 3: l3}

        self.assertEqual(first = LG.loads, second = loads)

        LG.del_load(load_no = 3)

        loads = {1: l1, 2: l2}

        self.assertEqual(first = LG.loads, second = loads)

        LG.del_load(load_name = l2.load_name)
        LG.del_load(abbrev = l1.abbrev)

        self.assertEqual(first = LG.loads, second = {})

    def test_loadGroup_del_load_exception(self):
        """
        Test the del_load method raises an exception when deleting a
        non-existent load.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0,
                      symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = []
        abbrev = 'GP 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertRaises(LoadNotPresentException, LG.del_load, load = l4)

        self.assertRaises(LoadNotPresentException, LG.del_load,
                          load_name = l3.load_name)

        self.assertRaises(LoadNotPresentException, LG.del_load,
                          load_no = l2.load_no)

        self.assertRaises(LoadNotPresentException, LG.del_load,
                          abbrev = l1.abbrev)

    def test_loadGroup_load_exists(self):
        """
        Test the load_exists method.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0,
                      symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        abbrev = 'GP 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertFalse(LG.load_exists(load = l4))
        self.assertTrue(LG.load_exists(load = l3))

        self.assertFalse(LG.load_exists(load_no = 4))
        self.assertTrue(LG.load_exists(load_no = 3))

        self.assertFalse(LG.load_exists(load_name = l4.load_name))
        self.assertTrue(LG.load_exists(load_name = l3.load_name))

        self.assertFalse(LG.load_exists(abbrev = l4.abbrev))
        self.assertTrue(LG.load_exists(abbrev = l3.abbrev))

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')

        LG.loads = {1: l1}

        # the following should return true because l1 and l2 share the same
        # load_no
        self.assertTrue(LG.load_exists(load = l2))
