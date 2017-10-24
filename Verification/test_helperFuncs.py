# coding=utf-8

import math
from unittest import TestCase
from HelperFuncs import linear_interp, sine_interp_90, sine_interp


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

        #first run the tests from before, as the 90degree range is expected
        #to be the same.

        range = 90
        x = 15

        results = sine_interp(range = range, x = x)

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = 60

        results = sine_interp(range = range, x = x)

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = -5

        self.assertRaises(ValueError, sine_interp, range, x)

        x = 95

        self.assertRaises(ValueError, sine_interp, range, x)

        self.assertRaises(ValueError, sine_interp, range, x)

        #next reset the range and re-run results.

        range = 45
        x = 7.5

        results = sine_interp(range = range, x = x)

        x = 15 #need to reset x before calculting the expected sine value

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)

        x = 30

        results = sine_interp(range = range, x = x)

        x = 60 #resst x before re-calculating.

        LHS_exp = math.cos(math.radians(x))
        RHS_exp = math.sin(math.radians(x))

        self.assertAlmostEqual(first = results.left, second = LHS_exp)
        self.assertAlmostEqual(first = results.right, second = RHS_exp)


    def test_wind_interp_85(self):
        self.fail()


    def test_req_angles_int(self):
        self.fail()


    def req_angles_list(self):
        self.fail()


    def req_angles_chooser(self):
        self.fail()