# coding=utf-8

import math
from unittest import TestCase, expectedFailure
from HelperFuncs import linear_interp, sine_interp_90, sine_interp
from HelperFuncs import wind_interp_85


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

        # Test the function against values calculated in Excel.

        angle = (0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75,
                 80, 85, 90)

        left = (1.00000, 0.99925, 0.99681, 0.99208, 0.98412, 0.97173, 0.95353,
                0.92807, 0.89397, 0.85000, 0.75013, 0.64984, 0.55052, 0.45313,
                0.35819, 0.26583, 0.17576, 0.08742, 0.00000)

        right = (0.00000, 0.08742, 0.17576, 0.26583, 0.35819, 0.45313, 0.55052,
                 0.64984, 0.75013, 0.85000, 0.89397, 0.92807, 0.95353, 0.97173,
                 0.98412, 0.99208, 0.99681, 0.99925, 1.00000)


        for a, l, r in zip(angle, left, right):

            l_exp, r_exp = wind_interp_85(90, a)

            self.assertAlmostEqual(first = l, second = l_exp, places = 5)
            self.assertAlmostEqual(first = r, second = r_exp, places = 5)

        self.assertRaises(ValueError, wind_interp_85, 95, 5)
        self.assertRaises(ValueError, wind_interp_85, 90, -5)
        self.assertRaises(ValueError, wind_interp_85, 90, 95)


    @expectedFailure
    def test_req_angles_int(self):

        self.fail("Method req_angles_int not tested as not currently used.")

    @expectedFailure
    def test_req_angles_list(self):

        self.fail("Method req_angles_list not tested as not currently used.")

    @expectedFailure
    def test_req_angles_chooser(self):

        self.fail("Method req_angles_chooser not tested as not currently used.")
