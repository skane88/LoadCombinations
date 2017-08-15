# coding=utf-8

"""
Tests for the RotataionalGroup class.
"""

from unittest import TestCase
from LoadGroup import RotationalGroup, LoadFactor
from Load import RotatableLoad
from HelperFuncs import sine_interp, linear_interp

class TestRotationalGroup(TestCase):

    def test_basic(self):
        '''
        Test the initialisation and __str__ and __repr__ methods.
        '''

        l1 = RotatableLoad(load = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           load_value = 2.5, angle = 22.5, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        # can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        # does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))


    def test_loads(self):
        '''
        Test the load getter / setter.
        '''

        l1 = RotatableLoad(load = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           load_value = 2.5, angle = 22.5, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)

        l1 = RotatableLoad(load = 'R1 - Rotating Load, 25 kPa', load_no = 3,
                           load_value = 25, angle = 75.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           load_value = 2.5, angle = 33.3, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load = 'R3 - Rotating Load, -5 kPa', load_no = 3,
                           load_value = -5, angle = -25, symmetrical = True,
                           abbrev = 'R3')

        loads = [l1, l2, l3]

        LG.loads = loads

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)


    def test_req_angles(self):
        '''
        Test the getter / setter
        '''

        l1 = RotatableLoad(load = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           load_value = 2.5, angle = 22.5, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        self.assertEqual(first = LG.req_angles, second = req_angles)

        req_angles = (0.0, 25.0, 145.0, 210.0, 450.0, -90.0, 570.0)

        LG.req_angles = req_angles

        req_angles = (0.0, 25.0, 90.0, 145.0, 210.0, 270.0)

        self.assertEqual(first = LG.req_angles, second = req_angles)


    def test_interp_func(self):
        '''
        Test the interp_func getter / setter
        '''

        l1 = RotatableLoad(load = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           load_value = 2.5, angle = 22.5, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        self.assertEqual(first = LG.interp_func, second = sine_interp)

        LG.interp_func = linear_interp

        self.assertEqual(first = LG.interp_func, second = linear_interp)


    def test_generate_cases(self):
        self.fail()
