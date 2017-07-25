"""
Unittest for the Load class.
"""

from unittest import TestCase
from Load import Load

class TestLoad(TestCase):

    def test_basic(self):
        """
        A basic unit test for the Load class. can Load objects be instantiated,
        and can their repr and str methods be used.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'

        l = Load(load = load_title, load_no = load_no, abbrev = abbrev)

        #the repr method should be able to recreate a Load object
        l2 = eval(repr(l))

        #does printing work?
        print(l)
        print(l2)

        #are the strings of l and l2 the same?
        self.assertEqual(first = str(l), second = str(l2))

    def test_load(self):
        """
        Test the load getter & setter.
        """

        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'

        l = Load(load = load_title, load_no = load_no, abbrev = abbrev)

        self.assertEqual(first = l.load, second = load_title)

        load_title = 'Changed Load'

        l.load = load_title

        self.assertEqual(first = l.load, second = load_title)

    def test_load_no(self):
        """
        Test the load_no getter & settter.
        """
        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'

        l = Load(load = load_title, load_no = load_no, abbrev = abbrev)

        self.assertEqual(first = l.load_no, second = load_no)

        load_no = 2

        l.load_no = load_no

        self.assertEqual(first = l.load_no, second = load_no)

    def test_abbrev(self):
        """
        Test the abbrev getter & settter.
        """
        load_title = 'G1 - Dead Load'
        load_no = 1
        abbrev = 'G1'

        l = Load(load = load_title, load_no = load_no, abbrev = abbrev)

        self.assertEqual(first = l.abbrev, second = abbrev)

        abbrev = 'G2'

        l.abbrev = abbrev

        self.assertEqual(first = l.abbrev, second = abbrev)