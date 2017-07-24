"""
Unittests for the RotatableLoad class.
"""

from unittest import TestCase
from Load import RotatableLoad


class TestRotatableLoad(TestCase):
    def test_basic(self):
        """
        A basic unit test for the RotatableLoad class. Can RotatableLoad objects
        be instantiated, and can their repr and str methods be used.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'
        load_value = 10
        angle = 100

        l = RotatableLoad(load = load_title, load_no = load_no,
                          load_value = load_value, angle = angle,
                          abbrev = abbrev)

        # the repr method should be able to recreate a Load object
        l2 = eval(repr(l))

        # does printing work?
        print(l)
        print(l2)

        # are the strings of l and l2 the same?
        self.assertEqual(first = str(l), second = str(l2))

    def test_angle(self):
        """
        Test the angle getter / setter.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'
        load_value = 10
        angle = 100

        l = RotatableLoad(load = load_title, load_no = load_no,
                          load_value = load_value, angle = angle,
                          abbrev = abbrev)

        self.assertEqual(first = l.angle, second = angle)

        angle = 450
        angle_exp = 90

        l.angle = angle

        self.assertEqual(first = l.angle, second = angle_exp)

        angle = -450
        angle_exp = 270

        l.angle = angle

        self.assertEqual(first = l.angle, second = angle_exp)

