# coding=utf-8

"""
Unit tests for the FactoredGroup class.
"""

from unittest import TestCase
from LoadGroup import FactoredGroup, LoadFactor
from Load import Load, RotatableLoad, ScalableLoad, WindLoad


class TestFactoredGroup(TestCase):
    def test_basic(self):
        """
        Test whether FactoredGroup objects can be instantiated, and the __str__
        and __repr__ methods.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0, symmetrical = True,
                      abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        load_factors = (-1.0, 0.0, 1.0)
        abbrev = 'GP 1'

        LG = FactoredGroup(group_name = group_name, loads = loads,
                           factors = load_factors, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        # can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        # does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_factors(self):
        """
        Test the factors getter / setter
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0, symmetrical = True,
                      abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        factors = (-1.0, 0.0, 1.0)
        abbrev = 'GP 1'

        LG = FactoredGroup(group_name = group_name, loads = loads,
                           factors = factors, abbrev = abbrev)

        self.assertEqual(first = LG.factors, second = factors)

        factors = (-0.5, -1.0, 0.25, 0.33, -5, 10)

        LG.factors = factors

        self.assertEqual(first = LG.factors, second = factors)

    def test_generate_cases(self):
        """
        Test the generate_groups function that generates the return load
        combinations
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0, angle = 0.0, symmetrical = True,
                      abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        load_factors = (-1.0, 0.0, 1.0)
        abbrev = 'GP 1'

        LG = FactoredGroup(group_name = group_name, loads = loads,
                           factors = load_factors, abbrev = abbrev)

        LC1_1 = LoadFactor(load = l1, base_factor = -1.0)
        LC2_1 = LoadFactor(load = l2, base_factor = -1.0)
        LC3_1 = LoadFactor(load = l3, base_factor = -1.0)
        LC4_1 = LoadFactor(load = l4, base_factor = -1.0)

        LC_1 = (LC1_1, LC2_1, LC3_1, LC4_1)

        LC1_2 = LoadFactor(load = l1, base_factor = 0.0)
        LC2_2 = LoadFactor(load = l2, base_factor = 0.0)
        LC3_2 = LoadFactor(load = l3, base_factor = 0.0)
        LC4_2 = LoadFactor(load = l4, base_factor = 0.0)

        LC_2 = (LC1_2, LC2_2, LC3_2, LC4_2)

        LC1_3 = LoadFactor(load = l1, base_factor = 1.0)
        LC2_3 = LoadFactor(load = l2, base_factor = 1.0)
        LC3_3 = LoadFactor(load = l3, base_factor = 1.0)
        LC4_3 = LoadFactor(load = l4, base_factor = 1.0)

        LC_3 = (LC1_3, LC2_3, LC3_3, LC4_3)

        LC = (LC_1, LC_2, LC_3)

        print(LC[0])
        print(LC[1])
        print(LC[2])

        LC_act = tuple(LG.generate_groups())

        print(LC_act[0])
        print(LC_act[1])
        print(LC_act[2])

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)
