# coding=utf-8

"""
Test the ScaledGroup class.
"""

from unittest import TestCase
from LoadGroup import ScaledGroup, LoadFactor
from Load import ScalableLoad, RotatableLoad


class TestScaledGroup(TestCase):

    def test_scaledGroup_basic(self):
        """
        Test that a ScalableLoad can be instantiated, and that the __str__ and
        __repr__ methods work.
        """

        l1 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 5kPa Live Load 2', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        abbrev = 'GP 1'

        LG = ScaledGroup(group_name = group_name, loads = loads,
                         factors = load_factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        # can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        # does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_scaledGroup_scale_to(self):
        """
        Test the scale_to getter / setter
        """

        l1 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 5kPa Live Load 2', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        abbrev = 'GP 1'

        LG = ScaledGroup(group_name = group_name, loads = loads,
                         factors = load_factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        self.assertEqual(first = LG.scale_to, second = scale_to)

        scale_to = 3.0
        LG.scale_to = scale_to

        self.assertEqual(first = LG.scale_to, second = scale_to)

    def test_scaledGroup_scale(self):
        """
        Test the scale getter / setter
        """

        l1 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 5kPa Live Load 2', load_no = 2,
                          load_value = 5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        abbrev = 'GP 1'

        LG = ScaledGroup(group_name = group_name, loads = loads,
                         factors = load_factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        self.assertEqual(first = LG.scale, second = scale)

        scale = False
        LG.scale = scale

        self.assertEqual(first = LG.scale, second = scale)

    def test_scaledGroup_generate_cases(self):
        """
        Test the generate_groups method.
        """

        l1 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 2.5kPa Live Load 2', load_no = 2,
                          load_value = 2.5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load, 10 kPa',
                           load_no = 3, load_value = 10, angle = 45.0,
                           symmetrical = True, abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        abbrev = 'GP 1'

        LG = ScaledGroup(group_name = group_name, loads = loads,
                         factors = load_factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        LC1_1 = LoadFactor(load = l1,
                           base_factor = load_factors[0],
                           scale_factor = l1.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC2_1 = LoadFactor(load = l2,
                           base_factor = load_factors[0],
                           scale_factor = l2.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC3_1 = LoadFactor(load = l3,
                           base_factor = load_factors[0],
                           scale_factor = l3.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})

        LC_1 = (LC1_1, LC2_1, LC3_1)

        LC1_2 = LoadFactor(load = l1,
                           base_factor = load_factors[1],
                           scale_factor = l1.scale_factor(scale_to = scale_to,
                                                         scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC2_2 = LoadFactor(load = l2,
                           base_factor = load_factors[1],
                           scale_factor = l2.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC3_2 = LoadFactor(load = l3,
                           base_factor = load_factors[1],
                           scale_factor = l3.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})

        LC_2 = (LC1_2, LC2_2, LC3_2)

        LC1_3 = LoadFactor(load = l1,
                           base_factor = load_factors[2],
                           scale_factor = l1.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC2_3 = LoadFactor(load = l2,
                           base_factor = load_factors[2],
                           scale_factor = l2.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})
        LC3_3 = LoadFactor(load = l3,
                           base_factor = load_factors[2],
                           scale_factor = l3.scale_factor(scale_to = scale_to,
                                                          scale = scale),
                           info = {'scale_to': scale_to,
                                   'is_scaled': scale})

        LC_3 = (LC1_3, LC2_3, LC3_3)

        LC = (LC_1, LC_2, LC_3)

        print(LC[0])
        print(LC[1])
        print(LC[2])

        LC_act = tuple(LG.generate_groups())

        print(LC_act[0])
        print(LC_act[1])
        print(LC_act[2])

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)
        
    def test_scaledGroup_scale_factors(self):
        l1 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 1,
                          load_value = 5, abbrev = 'Q1')
        l2 = ScalableLoad(load_name = 'Q2 - 2.5kPa Live Load 2', load_no = 2,
                          load_value = 2.5, abbrev = 'Q2')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load, 10 kPa',
                           load_no = 3, load_value = 10, angle = 45.0,
                           symmetrical = True, abbrev = 'R1')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        abbrev = 'GP 1'

        LG = ScaledGroup(group_name = group_name, loads = loads,
                         factors = load_factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        scale_factors = {1: 4.0 / 5.0, 2: 4.0 / 2.5, 3: 4.0 / 10.0}

        self.assertEqual(first = LG.scale_factors(), second = scale_factors)
