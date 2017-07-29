"""
Unit test for the LoadGroup class.
"""

from unittest import TestCase
from LoadGroup import LoadGroup
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

        LG = LoadGroup(group_name = group_name, loads =loads, abbrev = abbrev)

        print(LG)

        #can the repr method instantiate a load group?
        LG2 = eval(repr(LG))

        print(LG2)

        #does the str method work?

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
                           load_value = 10, angle = 45.0, abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        self.assertEqual(first = LG.group_name, second = group_name)

        group_name = 'Group 2'
        LG.group_name = group_name

        self.assertEqual(first = LG.group_name, second = group_name)


    def test_loads(self):
        self.fail()

    def test_abbrev(self):
        self.fail()

    def test_generate_cases(self):
        self.fail()
