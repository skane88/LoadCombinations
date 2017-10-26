"""
Unittest for the WindLoad class.
"""

from unittest import TestCase
from Load import WindLoad


class TestWindLoad(TestCase):

    def test_basic(self):
        """
        A basic unit test for the WindLoad class. can Load objects be
        instantiated, and can their repr and str methods be used.
        """

        load_title = 'WU - Wind Load'
        load_no = 1
        abbrev = 'WU'
        wind_speed = 69.3
        angle = 100
        symmetrical = True

        l = WindLoad(load = load_title, load_no = load_no,
                     wind_speed = wind_speed, angle = angle,
                     symmetrical = symmetrical, abbrev = abbrev)

        # the repr method should be able to recreate a Load object
        l2 = eval(repr(l))

        # does printing work?
        print(l)
        print(l2)

        # are the strings of l and l2 the same?
        self.assertEqual(first = str(l), second = str(l2))

    def test_wind_speed(self):
        """
        Test the wind_speed getter / setter
        """

        load_title = 'WU - Wind Load'
        load_no = 1
        abbrev = 'WU'
        wind_speed = 69.3
        angle = 100
        symmetrical = True

        l = WindLoad(load = load_title, load_no = load_no,
                     wind_speed = wind_speed, angle = angle,
                     symmetrical = symmetrical, abbrev = abbrev)

        self.assertEqual(first = l.wind_speed, second = wind_speed)

        wind_speed = 50.0
        l.wind_speed = wind_speed

        self.assertEqual(first = l.wind_speed, second = wind_speed)

    def test_scale_speed(self):
        """
        Test the scale_speed method.
        """

        load_title = 'WU - Wind Load'
        load_no = 1
        abbrev = 'WU'
        wind_speed = 69.3
        angle = 100
        symmetrical = True

        l = WindLoad(load = load_title, load_no = load_no,
                     wind_speed = wind_speed, angle = angle,
                     symmetrical = symmetrical, abbrev = abbrev)

        wind_speed_to = 25.0

        scale_factor = (wind_speed_to**2) / (wind_speed**2)

        self.assertEqual(first = l.scale_speed(wind_speed_to = wind_speed_to,
                                               scale = True),
                         second = scale_factor)

        self.assertEqual(first = l.scale_speed(wind_speed_to = wind_speed_to,
                                               scale = False),
                         second = 1.0)

