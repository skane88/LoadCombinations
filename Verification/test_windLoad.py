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

    def test_load(self):
        """
        Test the load getter / setter
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

        self.assertEqual(first = l.load, second = load_title)

        load_title = 'WX - Wind Load'
        l.load = load_title

        self.assertEqual(first = l.load, second = load_title)

    def test_load_no(self):
        """
        Test the load_no getter / setter
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

        self.assertEqual(first = l.load_no, second = load_no)

        load_no = 2
        l.load_no = load_no

        self.assertEqual(first = l.load_no, second = load_no)

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

    def test_angle(self):
        """
        Test the angle getter / setter.
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

        angle = 450
        angle_exp = 90

        l.angle = angle

        self.assertEqual(first = l.angle, second = angle_exp)

        angle = -450
        angle_exp = 270

        l.angle = angle

        self.assertEqual(first = l.angle, second = angle_exp)

    def test_symmetrical(self):
        """
        Test the symmetrical getter / setter
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

        self.assertEqual(first = l.symmetrical, second = symmetrical)

        symmetrical = False

        l.symmetrical = symmetrical

        self.assertEqual(first = l.symmetrical, second = symmetrical)

    def test_abbrev(self):
        """
        Test the abbrev getter & setter.
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

        self.assertEqual(first = l.abbrev, second = abbrev)
        self.assertEqual(first = l._rotatableload.abbrev, second = abbrev)

        abbrev = 'WX'
        l.abbrev = abbrev

        self.assertEqual(first = l.abbrev, second = abbrev)
        self.assertEqual(first = l._rotatableload.abbrev, second = abbrev)

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

