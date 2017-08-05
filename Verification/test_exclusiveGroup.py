# coding=utf-8

"""
Tests the ExclusiveGroup class.
"""

from unittest import TestCase
from LoadGroup import ExclusiveGroup, LoadFactor
from Load import Load, RotatableLoad, WindLoad, ScalableLoad


class TestExclusiveGroup(TestCase):
    def test_basic(self):
        """
        Test basic functionality - can the class be instantiated and can the
        __str__ and __repr__ methods be used.
        """

        l1 = ScalableLoad(load = 'Q1 - 2.5kPa Live Load', load_no = 1,
                          load_value = 2.5, abbrev = 'Q1')
        l2 = ScalableLoad(load = 'Q2 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0.0, 1.0)
        scale_to = 7.5
        scale = True
        abbrev = 'GP 1'

        LG = ExclusiveGroup(group_name = group_name, loads = loads,
                            load_factors = load_factors, scale_to = 7.5,
                            scale = scale, abbrev = abbrev)

        print(LG)

        # can the repr method instantiate a load group?
        LG2 = eval(repr(LG))

        print(LG2)

        # does the str method work?

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_generate_cases(self):
        """
        Test the generate cases method.
        """

        l1 = ScalableLoad(load = 'Q1 - 2.5kPa Live Load', load_no = 1,
                          load_value = 2.5, abbrev = 'Q1')
        l2 = ScalableLoad(load = 'Q2 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0.0, 1.0)
        scale_to = 7.5
        scale = True
        abbrev = 'GP 1'

        LG = ExclusiveGroup(group_name = group_name, loads = loads,
                            load_factors = load_factors, scale_to = 7.5,
                            scale = scale, abbrev = abbrev)

        LC_1 = LoadFactor(load = loads[0],
                          load_factor = load_factors[0]
                                        *loads[0].scale_factor(scale_to =
                                                               scale_to,
                                                               scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_2 = LoadFactor(load = loads[1],
                          load_factor = load_factors[0]
                                        * loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_3 = LoadFactor(load = loads[2],
                          load_factor = load_factors[0]
                                        * loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_4 = LoadFactor(load = loads[0],
                          load_factor = load_factors[1]
                                        * loads[0].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_5 = LoadFactor(load = loads[1],
                          load_factor = load_factors[1]
                                        * loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_6 = LoadFactor(load = loads[2],
                          load_factor = load_factors[1]
                                        * loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_7 = LoadFactor(load = loads[0],
                          load_factor = load_factors[2]
                                        * loads[0].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_8 = LoadFactor(load = loads[1],
                          load_factor = load_factors[2]
                                        * loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC_9 = LoadFactor(load = loads[2],
                          load_factor = load_factors[2]
                                        * loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          add_info = f'(scaled: {scale_to})')

        LC = ((LC_1, ), (LC_2, ), (LC_3, ), (LC_4, ), (LC_5, ), (LC_6, ),
              (LC_7, ), (LC_8, ), (LC_9, ))

        LC_ACT = tuple(LG.generate_cases())

        print(LC)
        print(LC_ACT)

        self.assertEqual(first = tuple(LG.generate_cases()), second = LC)
