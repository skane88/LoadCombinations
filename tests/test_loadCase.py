# coding=utf-8

from unittest import TestCase
from LoadCase import LoadCase
from LoadGroup import LoadGroup
from Load import Load, ScalableLoad, RotatableLoad, WindLoad
from exceptions import (LoadGroupExistsException, LoadGroupNotPresentException,
                        InvalidCombinationFactor)

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
        LGs = [[LG1, 1.0], [LG2, 2.0]]
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
        LGs = [LG1, 1.0]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = case_name, second = LC.case_name)

        case_name = 'Test Case 2'
        LC.case_name =  case_name

        self.assertEqual(first = case_name, second = LC.case_name)

    def test_case_no(self):
        """
        Test the case no getter / setter.
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
        LGs = [LG1, 1.0]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = case_no, second = LC.case_no)

        case_no = 2
        LC.case_no = case_no

        self.assertEqual(first = case_no, second = LC.case_no)

    def test_load_groups(self):
        """
        Test the load groups getter / setter.
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
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = LGs, second = LC.load_groups)

        LGs = {group_name2: (LG2, 2.0)}

        LC.load_groups = LGs

        self.assertEqual(first = LGs, second = LC.load_groups)

        #test the case where input is as a list of load groups
        LGs2 = [(LG2, 2.0)]
        LC.load_groups = LGs2

        self.assertEqual(first = LGs, second = LC.load_groups)

        #finally test the case where input is as a single tuple.

        LGs2 = (LG2, 2.0)
        LC.load_groups = LGs2

        self.assertEqual(first = LGs, second = LC.load_groups)

    def test_add_group(self):
        """
        Test the ``add_group`` method.
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
        LGs = {group_name: [LG1, 1.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        #first check the input is OK
        self.assertEqual(first = LGs, second = LC.load_groups)

        #next add a new load group
        LC.add_group([LG2, 2.0])
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}

        self.assertEqual(first = LGs, second = LC.load_groups)

        # next delete the load groups to prepare the way for adding multiple
        # loads at once
        LC.del_group(load_group = LG1)
        LC.del_group(load_group = LG2)

        #now add 2x load gropus at once.
        LGs2 = [[LG1, 1.0], [LG2, 2.0]]
        LC.add_group(LGs2)

        self.assertEqual(first = LGs, second = LC.load_groups)

        #now delete them again and test the method of adding as a dictionary
        LC.del_group(load_group = LG1)
        LC.del_group(load_group = LG2)

        LC.add_group(LGs)

        self.assertEqual(first = LGs, second = LC.load_groups)

        # next test that an error is raised if the same group is added
        self.assertRaises(LoadGroupExistsException, LC.add_group, [LG2, 1.0])

        # next delete the group so we can test some other potential errors
        LC.del_group(load_group = LG2)

        self.assertRaises(InvalidCombinationFactor, LC.add_group, LG2)
        self.assertRaises(InvalidCombinationFactor, LC.add_group, (2.0, LG2))
        self.assertRaises(InvalidCombinationFactor, LC.add_group, (LG2, '2.0'))

    def test_del_group(self):
        """
        Test the ``del_group`` method.
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
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        # has the object been instantiated correctly
        self.assertEqual(first = LGs, second = LC.load_groups)

        #test a basic delete
        LC.del_group(load_group = LG2)
        LGs2 = {group_name: [LG1, 1.0]}

        self.assertEqual(first = LGs2, second = LC.load_groups)

        #add LG2 back in and re-test
        LC.add_group([LG2, 2.0])
        self.assertEqual(first = LGs, second = LC.load_groups)
        LC.del_group(group_name = LG2.group_name)
        self.assertEqual(first = LGs2, second = LC.load_groups)

        # add LG2 back in and re-test
        LC.add_group([LG2, 2.0])
        self.assertEqual(first = LGs, second = LC.load_groups)
        LC.del_group(abbrev = LG2.abbrev)
        self.assertEqual(first = LGs2, second = LC.load_groups)

        #finally test the error checking
        self.assertRaises(LoadGroupNotPresentException, LC.del_group,
                          load_group = LG2)

    def test_group_exists(self):
        """
        Test the ``group_exists`` method.
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
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        # has the object been instantiated correctly
        self.assertEqual(first = LGs, second = LC.load_groups)

        #now test for something that should return true
        self.assertEqual(first = LG1.group_name,
                         second = LC.group_exists(load_group = LG1))
        self.assertEqual(first = LG1.group_name,
                         second = LC.group_exists(group_name = LG1.group_name))
        self.assertEqual(first = LG1.group_name,
                         second = LC.group_exists(abbrev = LG1.abbrev))

        # now test for something that should return false
        LC.del_group(load_group = LG2)
        LGs = {group_name: [LG1, 1.0]}

        # did hte delete work:
        self.assertEqual(first = LGs, second = LC.load_groups)

        # now check for false returns
        self.assertFalse(LC.group_exists(load_group = LG2))
        self.assertFalse(LC.group_exists(group_name = LG2.group_name))
        self.assertFalse(LC.group_exists(abbrev = LG2.abbrev))

    def test_get_factor(self):
        """
        Test the ``get_factor`` method.
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
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        # has the object been instantiated correctly
        self.assertEqual(first = LGs, second = LC.load_groups)

        # now test the factors
        self.assertEqual(first = 1.0, second = LC.get_factor(load_group = LG1))
        self.assertEqual(first = 1.0,
                         second = LC.get_factor(group_name = LG1.group_name))

        self.assertEqual(first = 2.0, second = LC.get_factor(load_group = LG2))
        self.assertEqual(first = 2.0,
                         second = LC.get_factor(group_name = LG2.group_name))

    def test_set_factor(self):
        """
        Test the ``set_factor`` method.
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
        LGs = {group_name: [LG1, 1.0], group_name2: [LG2, 2.0]}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        # has the object been instantiated correctly
        self.assertEqual(first = LGs, second = LC.load_groups)

        # now set the factors
        LC.set_factor(load_group = LG1, load_factor = 2.0)
        LC.set_factor(group_name = LG2.group_name, load_factor = 3.0)

        self.assertEqual(first = 2.0, second = LC.get_factor(load_group = LG1))
        self.assertEqual(first = 3.0, second = LC.get_factor(load_group = LG2))

    def test_abbrev(self):
        """
        Test the case abbrev getter / setter.
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
        LGs = [LG1, 1.0]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = abbrev, second = LC.abbrev)

        abbrev = 'TC2'
        LC.abbrev = abbrev

        self.assertEqual(first = abbrev, second = LC.abbrev)

    def test_generate_cases(self):
        self.fail()
