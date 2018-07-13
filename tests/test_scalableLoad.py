"""
Unittests for the ScalableLoad class.
"""

from unittest import TestCase
from LoadCombination.Load import ScalableLoad


class TestScalableLoad(TestCase):

    def test_scalableLoad_basic(self):
        """
        A basic unit test for the ScalableLoad class. can Load objects be
        instantiated, and can their repr and str methods be used.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'
        load_value = 10

        l = ScalableLoad(load_name = load_title, load_no = load_no,
                         load_value = load_value, abbrev = abbrev)

        # the repr method should be able to recreate a Load object
        l2 = eval(repr(l))

        # does printing work?
        print(l)
        print(l2)

        # are the strings of l and l2 the same?
        self.assertEqual(first = str(l), second = str(l2))

    def test_scalableLoad_load_value(self):
        """
        Test the load_value getter / setter.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'
        load_value = 10

        l = ScalableLoad(load_name = load_title, load_no = load_no,
                         load_value = load_value, abbrev = abbrev)

        self.assertEqual(first = l.load_value, second = load_value)

        load_value = 20

        l.load_value = load_value

        self.assertEqual(first = l.load_value, second = load_value)

    def test_scalableLoad_scale_factor(self):
        """
        Test the scale_factor method.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'
        load_value = 10

        l = ScalableLoad(load_name = load_title, load_no = load_no,
                         load_value = load_value, abbrev = abbrev)

        scale_to = 5

        scale_factor = scale_to / load_value

        self.assertEqual(first = l.scale_factor(scale_to = scale_to,
                                                scale = True),
                         second = scale_factor)

        self.assertEqual(first = l.scale_factor(scale_to = scale_to,
                                                scale = False),
                         second = 1.0)
