# coding=utf-8

from unittest import TestCase
from LoadCase import LoadCase
from LoadGroup import LoadGroup, FactoredGroup, ScaledGroup, WindGroup
from Load import Load, ScalableLoad, RotatableLoad, WindLoad
from exceptions import (LoadGroupExistsException, LoadGroupNotPresentException,
                        InvalidCombinationFactor)
from LoadFactor import LoadFactor
from GroupFactor import GroupFactor
from HelperFuncs import wind_interp_85
from Combination import Combination

class TestLoadCase(TestCase):

    def test_loadCase_basic(self):
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
        LGs = [GroupFactor(load_group =  LG1, group_factor = 1.0),
               GroupFactor(load_group = LG2, group_factor = 2.0)]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        print(LC)

        # can the repr method instantiate a load group?
        LC2 = eval(repr(LC))

        print(LC2)

        # does the str method work?

        self.assertEqual(first = str(LC), second = str(LC2))

    def test_loadCase_case_name(self):
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
        LGs = GroupFactor(load_group = LG1, group_factor = 1.0)
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = case_name, second = LC.case_name)

        case_name = 'Test Case 2'
        LC.case_name =  case_name

        self.assertEqual(first = case_name, second = LC.case_name)

    def test_loadCase_case_no(self):
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
        LGs = GroupFactor(load_group = LG1, group_factor = 1.0)
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = case_no, second = LC.case_no)

        case_no = 2
        LC.case_no = case_no

        self.assertEqual(first = case_no, second = LC.case_no)

    def test_loadCase_load_groups(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = LGs, second = LC.load_groups)

        LGs = {group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}

        LC.load_groups = LGs

        self.assertEqual(first = LGs, second = LC.load_groups)

        #test the case where input is as a list of load groups
        LGs2 = [GroupFactor(load_group = LG2, group_factor = 2.0)]
        LC.load_groups = LGs2

        self.assertEqual(first = LGs, second = LC.load_groups)

        #finally test the case where input is as a single tuple.

        LGs2 = GroupFactor(load_group = LG2, group_factor = 2.0)
        LC.load_groups = LGs2

        self.assertEqual(first = LGs, second = LC.load_groups)

    def test_loadCase_add_group(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0)}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        #first check the input is OK
        self.assertEqual(first = LGs, second = LC.load_groups)

        #next add a new load group
        LC.add_group(GroupFactor(load_group = LG2, group_factor = 2.0))
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}

        self.assertEqual(first = LGs, second = LC.load_groups)

        # next delete the load groups to prepare the way for adding multiple
        # loads at once
        LC.del_group(load_group = LG1)
        LC.del_group(load_group = LG2)

        #now add 2x load groups at once.
        LGs2 = [GroupFactor(load_group = LG1, group_factor = 1.0),
                GroupFactor(load_group = LG2, group_factor = 2.0)]
        LC.add_group(LGs2)

        self.assertEqual(first = LGs, second = LC.load_groups)

        #now delete them again and test the method of adding as a dictionary
        LC.del_group(load_group = LG1)
        LC.del_group(load_group = LG2)

        LC.add_group(LGs)

        self.assertEqual(first = LGs, second = LC.load_groups)

        # next test that an error is raised if the same group is added
        self.assertRaises(LoadGroupExistsException, LC.add_group,
                          GroupFactor(load_group = LG2, group_factor = 1.0))

        # next delete the group so we can test some other potential errors
        LC.del_group(load_group = LG2)

        self.assertRaises(InvalidCombinationFactor, LC.add_group, LG2)
        self.assertRaises(InvalidCombinationFactor, LC.add_group, (2.0, LG2))
        self.assertRaises(InvalidCombinationFactor, LC.add_group, (LG2, '2.0'))

    def test_loadCase_del_group(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        # has the object been instantiated correctly
        self.assertEqual(first = LGs, second = LC.load_groups)

        #test a basic delete
        LC.del_group(load_group = LG2)
        LGs2 = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0)}

        self.assertEqual(first = LGs2, second = LC.load_groups)

        #add LG2 back in and re-test
        LC.add_group(GroupFactor(load_group = LG2, group_factor = 2.0))
        self.assertEqual(first = LGs, second = LC.load_groups)
        LC.del_group(group_name = LG2.group_name)
        self.assertEqual(first = LGs2, second = LC.load_groups)

        # add LG2 back in and re-test
        LC.add_group(GroupFactor(load_group = LG2, group_factor = 2.0))
        self.assertEqual(first = LGs, second = LC.load_groups)
        LC.del_group(abbrev = LG2.abbrev)
        self.assertEqual(first = LGs2, second = LC.load_groups)

        #finally test the error checking
        self.assertRaises(LoadGroupNotPresentException, LC.del_group,
                          load_group = LG2)

    def test_loadCase_group_exists(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0)}

        # did hte delete work:
        self.assertEqual(first = LGs, second = LC.load_groups)

        # now check for false returns
        self.assertFalse(LC.group_exists(load_group = LG2))
        self.assertFalse(LC.group_exists(group_name = LG2.group_name))
        self.assertFalse(LC.group_exists(abbrev = LG2.abbrev))

    def test_loadCase_get_factor(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}
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

    def test_loadCase_set_factor(self):
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
        LGs = {group_name: GroupFactor(load_group = LG1, group_factor = 1.0),
               group_name2: GroupFactor(load_group = LG2, group_factor = 2.0)}
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

    def test_loadCase_abbrev(self):
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
        LGs = GroupFactor(load_group = LG1, group_factor = 1.0)
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        self.assertEqual(first = abbrev, second = LC.abbrev)

        abbrev = 'TC2'
        LC.abbrev = abbrev

        self.assertEqual(first = abbrev, second = LC.abbrev)

    def test_loadCase_generate_cases(self):
        """
        Test the generate_cases method.
        """

        l1 = Load(load_name = 'G1 - Mechanical Dead Load', load_no = 1,
                  abbrev = 'G1')
        l2 = ScalableLoad(load_name = 'Q1 - 5kPa Live Load', load_no = 2,
                          load_value = 5, abbrev = 'Q1')
        l3 = RotatableLoad(load_name = 'R1 - Rotating Load', load_no = 3,
                           load_value = 10, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')
        l4_1 = WindLoad(load_name = 'WUx - Wind Load', load_no = 4,
                        wind_speed = 69.0,
                        angle = 0.0, symmetrical = True, abbrev = 'WUx')
        l4_2 = WindLoad(load_name = 'WUz - Wind Load', load_no = 5,
                        wind_speed = 69.0,
                        angle = 90.0, symmetrical = True, abbrev = 'WUz')
        l4_3 = WindLoad(load_name = 'WU-x - Wind Load', load_no = 6,
                        wind_speed = 69.0,
                        angle = 180.0, symmetrical = True, abbrev = 'WU-x')
        l4_4 = WindLoad(load_name = 'WU-z - Wind Load', load_no = 7,
                        wind_speed = 69.0,
                        angle = 270.0, symmetrical = True, abbrev = 'WU-z')

        group_name = 'Group 1'
        loads = [l1]
        abbrev = 'Gp 1'

        LF1 = LoadFactor(load = l1, base_factor = 1.0, scale_factor = 1.0,
                         rotational_factor = 1.0, symmetry_factor = 1.0,
                         group_factor = 1.0)

        group_name2 = 'Group 2'
        loads2 = [l2]
        factors2 = (-1.0, 1.0)
        abbrev2 = 'Gp 2'

        LF2_1 = LoadFactor(load = l2, base_factor = -1.0, scale_factor = 1.0,
                           rotational_factor = 1.0, symmetry_factor = 1.0,
                           group_factor = 2.0)
        LF2_2 = LoadFactor(load = l2, base_factor = 1.0, scale_factor = 1.0,
                           rotational_factor = 1.0, symmetry_factor = 1.0,
                           group_factor = 2.0)

        group_name3 = 'Group 3'
        loads3 = [l3]
        factors3 = (-1.0, 1.0)
        abbrev3 = 'Gp 3'

        LF3_1 = LoadFactor(load = l3, base_factor = -1.0, scale_factor = 0.5,
                           rotational_factor = 1.0, symmetry_factor = 1.0,
                           group_factor = 1.0,
                           info = {'scale_to': 5, 'is_scaled': True})
        LF3_2 = LoadFactor(load = l3, base_factor = 1.0, scale_factor = 0.5,
                           rotational_factor = 1.0, symmetry_factor = 1.0,
                           group_factor = 1.0,
                           info = {'scale_to': 5, 'is_scaled': True})

        group_name4 = 'Group 4'
        loads4 = [l4_1, l4_2, l4_3, l4_4]
        factors4 = (1.0,)
        req_angles4 = (0.0,45.0,90.0, 135.0)
        abbrev4 = 'Gp 4'

        scale_factor = 25*25/69/69
        rot_45 = wind_interp_85(90, 45).left

        LF4_1 = LoadFactor(load = l4_1, base_factor = 1.0,
                           scale_factor = scale_factor,
                           rotational_factor = 1.0,
                           symmetry_factor = 1.0,
                           group_factor = 1.0,
                           info = {'angle': 0.0, 'symmetric': False,
                                   'scale_to': 25, 'is_scaled': True})
        LF4_2_1 = LoadFactor(load = l4_1, base_factor = 1.0,
                             scale_factor = scale_factor,
                             rotational_factor = rot_45,
                             symmetry_factor = 1.0,
                             group_factor = 1.0,
                             info = {'angle': 45.0, 'symmetric': False,
                                     'scale_to': 25, 'is_scaled': True})
        LF4_2_2 = LoadFactor(load = l4_2,
                             scale_factor = scale_factor,
                             rotational_factor = rot_45,
                             symmetry_factor = 1.0,
                             group_factor = 1.0,
                             info = {'angle': 45.0, 'symmetric': False,
                                     'scale_to': 25, 'is_scaled': True})
        LF4_3 = LoadFactor(load = l4_2,
                           scale_factor = scale_factor,
                           rotational_factor = 1.0,
                           symmetry_factor = 1.0,
                           group_factor = 1.0,
                           info = {'angle': 90.0, 'symmetric': False,
                                   'scale_to': 25, 'is_scaled': True})
        LF4_4_1 = LoadFactor(load = l4_2, base_factor = 1.0,
                             scale_factor = scale_factor,
                             rotational_factor = rot_45,
                             symmetry_factor = 1.0,
                             group_factor = 1.0,
                             info = {'angle': 135.0, 'symmetric': False,
                                     'scale_to': 25, 'is_scaled': True})
        LF4_4_2 = LoadFactor(load = l4_3, base_factor = 1.0,
                             scale_factor = scale_factor,
                             rotational_factor = rot_45,
                             symmetry_factor = 1.0,
                             group_factor = 1.0,
                             info = {'angle': 135.0, 'symmetric': False,
                                     'scale_to': 25, 'is_scaled': True})

        LG1 = LoadGroup(group_name = group_name, loads = loads, abbrev = abbrev)
        LG2 = FactoredGroup(group_name = group_name2,
                            loads = loads2,
                            factors = factors2,
                            abbrev = abbrev2)
        LG3 = ScaledGroup(group_name = group_name3,
                          loads = loads3,
                          factors = factors3,
                          scale_to = 5,
                          abbrev = abbrev3)
        LG4 = WindGroup(group_name = group_name4, loads = loads4,
                        factors = factors4, scale_speed = 25, scale = True,
                        req_angles = req_angles4, abbrev = abbrev4)

        case_name = 'Test Case'
        case_no = 1
        LGs = [GroupFactor(load_group = LG1, group_factor = 1.0),
               GroupFactor(load_group = LG2, group_factor = 2.0),
               GroupFactor(load_group = LG3, group_factor = 1.0),
               GroupFactor(load_group = LG4, group_factor = 1.0)]
        abbrev = 'TC'

        LC = LoadCase(case_name = case_name, case_no = case_no,
                      load_groups = LGs, abbrev = abbrev)

        C1 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_1, LF3_1, LF4_1])
        C2 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_2, LF3_1, LF4_1])
        C3 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_1, LF3_2, LF4_1])
        C4 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_2, LF3_2, LF4_1])

        C5 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_1, LF3_1, LF4_2_1, LF4_2_2])
        C6 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_2, LF3_1, LF4_2_1, LF4_2_2])
        C7 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_1, LF3_2, LF4_2_1, LF4_2_2])
        C8 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_2, LF3_2, LF4_2_1, LF4_2_2])

        C9 = Combination(load_case_no = 1, load_case = case_name,
                         load_case_abbrev = abbrev,
                         load_factors = [LF1, LF2_1, LF3_1, LF4_3])
        C10 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_2, LF3_1, LF4_3])
        C11 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_1, LF3_2, LF4_3])
        C12 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_2, LF3_2, LF4_3])

        C13 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_1, LF3_1, LF4_4_1, LF4_4_2])
        C14 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_2, LF3_1, LF4_4_1, LF4_4_2])
        C15 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_1, LF3_2, LF4_4_1, LF4_4_2])
        C16 = Combination(load_case_no = 1, load_case = case_name,
                          load_case_abbrev = abbrev,
                          load_factors = [LF1, LF2_2, LF3_2, LF4_4_1, LF4_4_2])


        expected = [C1, C2, C3, C4, C5, C6, C7, C8, C9, C10, C11, C12, C13, C14,
                    C15, C16]

        self.assertEqual(first = list(LC.generate_cases()), second = expected)
