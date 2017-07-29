# coding=utf-8

"""
Unit test for the LoadGroup class.
"""

from unittest import TestCase
from LoadGroup import LoadGroup, LoadFactor
from Load import Load, RotatableLoad, ScalableLoad, WindLoad


class TestLoadGroup(TestCase):
    def test_basic(self):
        """
        Test basic functionality - can the class be instantiated and can the str
        and repr methods be used.
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
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

    def test_group_name(self):
        """
        Test the group_name getter / setter.
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.group_name, second = group_name)

        group_name = 'Group 2'
        LG.group_name = group_name

        self.assertEqual(first = LG.group_name, second = group_name)

    def test_loads(self):
        """
        Test the loads getter / setter
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.loads, second = loads)

        loads = [l1, l2]

        LG.loads = loads

        self.assertEqual(first = LG.loads, second = loads)

    def test_abbrev(self):
        """
        Test the abbrev getter / setter
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.abbrev, second = abbrev)

        abbrev = 'GP 2'

        LG.abbrev = abbrev

        self.assertEqual(first = LG.abbrev, second = abbrev)

    def test_generate_cases(self):
        """
        Test the generate_cases method.
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        # next build the list of expected return loads. This is simply all of
        # the loads in a LoadFactor object.

        LF1 = LoadFactor(load = l1, load_factor = 1.0, add_info = '')
        LF2 = LoadFactor(load = l2, load_factor = 1.0, add_info = '')
        LF3 = LoadFactor(load = l3, load_factor = 1.0, add_info = '')
        LF4 = LoadFactor(load = l4, load_factor = 1.0, add_info = '')

        # create a tuple of load factors. This is one "load combination"
        LC = (LF1, LF2, LF3, LF4)
        LC = (LC,)  # wrap in another tuple because the default generator method
                    # should return a list of load combinations. In this case,
                    # for a basic load group there is only 1x combination but
                    # for consistency through classes return a tuple of all
                    # possible load combinations.

        print(LC)
        print(tuple(LG.generate_cases()))

        self.assertEqual(first = tuple(LG.generate_cases()), second = LC)
