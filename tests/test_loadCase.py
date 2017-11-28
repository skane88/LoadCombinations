# coding=utf-8

from unittest import TestCase
from LoadCase import LoadCase
from LoadGroup import LoadGroup
from Load import Load, ScalableLoad, RotatableLoad, WindLoad

class TestLoadCase(TestCase):

    def test_basic(self):
        """
        Tests whether the ``LoadGroup`` can be instantiated or not.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        group_name2 = 'Group 2'
        loads2 = [l1, l2, l3, l4]
        abbrev2 = 'Gp 2'

        LG1 = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)
        LG2 = LoadGroup(group_name = group_name2, loads = loads2,
                        abbrev = abbrev2)

        case_name = 'Test Case'
        case_no = 1
        LGs = [(LG1, 1.0), (LG2, 2.0)]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        print(LC)

        # can the repr method instantiate a load group?
        LC2 = eval(repr(LC))

        print(LC2)

        # does the str method work?

        self.assertEqual(first = str(LC), second = str(LC2))

    def test_case_name(self):
        """
        Test the case name getter / setter.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                      wind_speed = 69.0,
                      angle = 0.0, symmetrical = True, abbrev = 'WUx')

        group_name = 'Group 1'
        loads = [l1, l2, l3, l4]
        abbrev = 'Gp 1'

        LG1 = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)

        case_name = 'Test Case'
        case_no = 1
        LGs = (LG1, 1.0)
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = case_name, second = LC.case_name)

        case_name = 'Test Case 2'
        LC.case_name =  case_name

        self.assertEqual(first = case_name, second = LC.case_name)

    def test_case_no(self):
        self.fail()

    def test_load_groups(self):
        self.fail()

    def test_add_group(self):
        self.fail()

    def test_del_group(self):
        self.fail()

    def test_group_exists(self):
        self.fail()

    def test_get_factor(self):
        self.fail()

    def test_set_factor(self):
        self.fail()

    def test_abbrev(self):
        self.fail()

    def test_generate_cases(self):
        self.fail()
