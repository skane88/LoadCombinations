# coding=utf-8

"""
Tests for the RotataionalGroup class.
"""

from unittest import TestCase
from LoadGroup import RotationalGroup, LoadFactor
from Load import RotatableLoad
from HelperFuncs import sine_interp

class TestRotationalGroup(TestCase):

    def test_basic(self):

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
        self.fail()

    def test_half_list(self):
        self.fail()

    def test_interp_func(self):
        self.fail()

    def test_req_angles(self):
        self.fail()

    def test_set_req_angles_int(self):
        self.fail()

    def test_generate_cases(self):
        self.fail()
