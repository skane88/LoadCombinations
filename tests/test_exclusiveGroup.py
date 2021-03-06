# coding=utf-8

"""
Tests the ExclusiveGroup class.
"""

from unittest import TestCase
from LoadCombination.LoadGroup import ExclusiveGroup, LoadFactor
from LoadCombination.Load import RotatableLoad, ScalableLoad


class TestExclusiveGroup(TestCase):

    def test_exclusiveGroup_basic(self):
        """
        Test basic functionality - can the class be instantiated and can the
        __str__ and __repr__ methods be used.
        """

        l1 = ScalableLoad(load_name = 'Q1 - 2.5kPa Live Load', load_no = 1,
                          load_value = 2.5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        factors = (-1.0, 0.0, 1.0)
        scale_to = 7.5
        scale = True
        abbrev = 'GP 1'

        LG = ExclusiveGroup(group_name = group_name, loads = loads,
                            factors = factors, scale_to = scale_to,
                            scale = scale, abbrev = abbrev)

        print(LG)

        # can the repr method instantiate a load group?
        LG2 = eval(repr(LG))

        print(LG2)

        # does the str method work?

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_exclusiveGroup_generate_cases(self):
        """
        Test the generate cases method.
        """

        l1 = ScalableLoad(load_name = 'Q1 - 2.5kPa Live Load', load_no = 1,
                          load_value = 2.5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        factors = (-1.0, 0.0, 1.0)
        scale_to = 7.5
        scale = True
        abbrev = 'GP 1'

        LG = ExclusiveGroup(group_name = group_name, loads = loads,
                            factors = factors, scale_to = 7.5,
                            scale = scale, abbrev = abbrev)

        LC_1 = LoadFactor(load = loads[0],
                          base_factor = factors[0],
                          scale_factor = loads[0].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_2 = LoadFactor(load = loads[1],
                          base_factor = factors[0],
                          scale_factor = loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_3 = LoadFactor(load = loads[2],
                          base_factor = factors[0],
                          scale_factor = loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_4 = LoadFactor(load = loads[0],
                          base_factor = factors[1],
                          scale_factor = loads[0].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_5 = LoadFactor(load = loads[1],
                          base_factor = factors[1],
                          scale_factor = loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_6 = LoadFactor(load = loads[2],
                          base_factor = factors[1],
                          scale_factor = loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_7 = LoadFactor(load = loads[0],
                          base_factor = factors[2],
                          scale_factor = loads[0].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_8 = LoadFactor(load = loads[1],
                          base_factor = factors[2],
                          scale_factor = loads[1].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC_9 = LoadFactor(load = loads[2],
                          base_factor = factors[2],
                          scale_factor = loads[2].scale_factor(scale_to =
                                                                scale_to,
                                                                scale = scale),
                          info = {'scale_to': scale_to,
                                  'is_scaled': scale})

        LC = ((LC_1,), (LC_2,), (LC_3,), (LC_4,), (LC_5,), (LC_6,),
              (LC_7,), (LC_8,), (LC_9,))

        LC_ACT = tuple(LG.generate_groups())

        print(LC)
        print(LC_ACT)

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)
