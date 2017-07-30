from unittest import TestCase
from LoadGroup import FactoredGroup
from Load import Load, RotatableLoad, ScalableLoad, WindLoad

class TestFactoredGroup(TestCase):
    def test_basic(self):
        """
        Test whether FactoredGroup objects can be instantiated, and the __str__
        and __repr__ methods.
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        load_factors = (-1.0, 0.0, 1.0)
        abbrev = 'GP 1'

        LG = FactoredGroup(group_name = group_name, loads = loads,
                           load_factors = load_factors, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        #can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        #does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_load_factors(self):
        """
        Test the load_factors getter / setter
        """

        l1 = Load(load = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load = 'WUx - Wind Load', load_no = 4, wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        load_factors = (-1.0, 0.0, 1.0)
        abbrev = 'GP 1'

        LG = FactoredGroup(group_name = group_name, loads = loads,
                           load_factors = load_factors, abbrev = abbrev)

        self.assertEqual(first = LG.load_factors, second = load_factors)

        load_factors = (-0.5, -1.0, 0.25, 0.33, -5, 10)

        LG.load_factors = load_factors

        self.assertEqual(first = LG.load_factors, second = load_factors)

    def test_generate_cases(self):
        self.fail()
