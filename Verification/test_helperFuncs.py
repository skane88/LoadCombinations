# coding=utf-8

import math
from unittest import TestCase
from HelperFuncs import linear_interp, sine_interp_90


class test_helper_funcs(TestCase):

    def test_linear_interp(self):

        range = 10
        x = 2

        results = linear_interp(range = range, x = x)

        LHS_exp = 0.8
        RHS_exp = 0.2

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        range = 50
        x = 37.5

        results = linear_interp(range = range, x = x)

        LHS_exp = 0.25
        RHS_exp = 0.75

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = -5
        range = 10

        self.assertRaises(ValueError, linear_interp, range, x)

        x = 15

        self.assertRaises(ValueError, linear_interp, range, x)

    def test_sine_interp_90(self):
        range = 90
        x = 15

        results = sine_interp_90(range = range, x = x)

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = 60

        results = sine_interp_90(range = range, x = x)

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = -5

        self.assertRaises(ValueError, sine_interp_90, range, x)

        x = 95

        self.assertRaises(ValueError, sine_interp_90, range, x)

        self.assertRaises(ValueError, sine_interp_90, range, x)


    def test_sine_interp(self):
        self.fail()


    def test_wind_interp_85(self):
        self.fail()


    def test_req_angles_int(self):
        self.fail()


    def req_angles_list(self):
        self.fail()


    def req_angles_chooser(self):
        self.fail()