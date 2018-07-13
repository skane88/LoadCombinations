# coding=utf-8

"""
Tests for the RotationalGroup class.
"""
import math
from unittest import TestCase
from LoadCombination.LoadGroup import RotationalGroup
from LoadCombination.Load import RotatableLoad
from LoadCombination.HelperFuncs import sine_interp, linear_interp
from LoadCombination.exceptions import LoadExistsException, AngleExistsException
from LoadCombination.LoadFactor import LoadFactor

class TestRotationalGroup(TestCase):

    def test_RotationalGroup_basic(self):
        """
        Test the initialisation and __str__ and __repr__ methods.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 1,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 22.5,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        # can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        # does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))

    def test_RotationalGroup_add_load(self):
        """
        Test the add_load method.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 1,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 22.5,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = {}
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        self.assertEqual(first = LG.loads, second = loads)

        LG.add_load(l1)
        loads = {1: l1}

        self.assertEqual(first = LG.loads, second = loads)

        LG.add_load(l2)
        loads = {1: l1, 2: l2}

        self.assertEqual(first = LG.loads, second = loads)

        LG.add_load(l3)
        loads = {1: l1, 2: l2, 3: l3}

        self.assertEqual(first = LG.loads, second = loads)

    def test_RotationalGroup_add_load_errors(self):
        """
        Test the add_load method raises errors.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 1,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 22.5,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 5 kPa', load_no = 2,
                           load_value = 7.5, angle = 350.0, symmetrical = True,
                           abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R4 - Rotating Load, 1 kPa', load_no = 4,
                           load_value = 1.0, angle = 45.0, symmetrical = True,
                           abbrev = 'R4')

        group_name = 'Group 1'
        loads = {1: l1, 2: l2}
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        # the following should fail because the load already exists in the
        # dictionary
        self.assertRaises(LoadExistsException, LG.add_load, l2)

        # the following should fail because the load_no already exists in the
        # dictionary
        self.assertRaises(LoadExistsException, LG.add_load, l3)

        # the following should fail because the angle already exists in the
        # dictionary
        self.assertRaises(AngleExistsException, LG.add_load, l4)

    def test_RotationalGroup_angles(self):
        """
        Test the angles property
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1, load_value = 1.25, angle = 0.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 90,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 10.0, angle = 180.0,
                           symmetrical = True, abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R4 - Rotating Load, 2.5 kPa',
                           load_no = 4, load_value = 2.5, angle = 270.0,
                           symmetrical = True, abbrev = 'R4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (0.0, 90.0, 180.0, 270.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        angles = {0.0: 1, 90.0: 2, 180.0: 3, 270.0: 4}

        self.assertEqual(first = LG.angles, second = angles)

    def test_RotationalGroup_angles_with_symmetry(self):
        """
        Test the angles_with_symmetry property
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1,
                           load_value = 2.5, angle = 0.0,
                           symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2,
                           load_value = 2.5, angle = 90, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3,
                           load_value = 2.5, angle = 180.0,
                           symmetrical = True,
                           abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 4,
                           load_value = 2.5, angle = 35.0,
                           symmetrical = True,
                           abbrev = 'R4')

        group_name = 'Group 1'
        loads = [l1, l3, l2, l4]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (45.0, 135.0, 225.0, 315.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        angles_with_symmetry = {0.0: (1, 1.0, False), 90.0: (2, 1.0, False),
                                180.0: (3, 1.0, False), 270.0: (2, -1.0, True),
                                360: (1, 1.0, False),
                                35.0: (4, 1.0, False), 215.0: (4, -1.0, True)}

        print(LG.angles_with_symmetry)
        print(angles_with_symmetry)

        self.assertEqual(first = LG.angles_with_symmetry,
                         second = angles_with_symmetry)

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1,
                           load_value = 2.5, angle = 360.0,
                           symmetrical = True,
                           abbrev = 'R1')


        loads = [l1, l3, l2]
        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        angles_with_symmetry = {0.0: (1, 1.0, False), 90.0: (2, 1.0, False),
                                180.0: (3, 1.0, False), 270.0: (2, -1.0, True),
                                360: (1, 1.0, False)}

        print(LG.angles_with_symmetry)
        print(angles_with_symmetry)

        self.assertEqual(first = LG.angles_with_symmetry,
                         second = angles_with_symmetry)

    def test_RotationalGroup_req_angles(self):
        """
        Test the getter / setter
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 1,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 22.5,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0, symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        self.assertEqual(first = LG.req_angles, second = req_angles)

        req_angles = (0.0, 25.0, 145.0, 210.0, 450.0, -90.0, 570.0)

        LG.req_angles = req_angles

        req_angles = (0.0, 25.0, 90.0, 145.0, 210.0, 270.0)

        self.assertEqual(first = LG.req_angles, second = req_angles)

    def test_RotationalGroup_interp_func(self):
        """
        Test the interp_func getter / setter
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 1,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 22.5,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 7.5, angle = 135.0,
                           symmetrical = True, abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_to = 4.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        self.assertEqual(first = LG.interp_func, second = sine_interp)

        LG.interp_func = linear_interp

        self.assertEqual(first = LG.interp_func, second = linear_interp)

    def test_RotationalGroup_nearest_angles(self):
        """
        Test the nearest_angles method.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1, load_value = 1.25, angle = 0.0,
                           symmetrical = False, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 90,
                           symmetrical = False, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 10.0, angle = 180.0,
                           symmetrical = False, abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R4 - Rotating Load, 2.5 kPa',
                           load_no = 4, load_value = 2.5, angle = 270.0,
                           symmetrical = False, abbrev = 'R4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (0.0, 90.0, 180.0, 270.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        angle = 0
        expected = {0.0: (1, 1.0, False)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 45
        expected =  {0.0: (1, 1.0, False), 90.0: (2, 1.0, False)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 335
        expected = {270.: (4, 1.0, False), 360.0: (1, 1.0, False)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 360
        expected = {360.0: (1, 1.0, False)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

    def test_RotationalGroup_nearest_angles_with_symmetry(self):
        """
        Test the nearest_angles method when the ``self.loads`` dictionary relies
        on symmetry to return a full list of angles.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1, load_value = 1.25, angle = 15.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 105.0,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 10.0, angle = 180.0,
                           symmetrical = True, abbrev = 'R3')


        group_name = 'Group 1'
        loads = [l1, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (0.0, 90.0, 180.0, 270.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        angle = 0
        expected = {0.0: (3, -1.0, True)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 45
        expected = {15.0: (1, 1.0, False), 105.0: (2, 1.0, False)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 335
        expected = {285.0: (2, -1.0, True), 360.0: (3, -1.0, True)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

        angle = 360
        expected = {360.0: (3, -1.0, True)}

        self.assertEqual(first = LG.nearest_angles(angle), second = expected)

    def test_RotationalGroup_generate_cases_simple(self):
        '''
        Test the generate_groups method which returns the output load
        combinations.

        This test only tests the case where the required angles are already
        in the list of loads.
        '''

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1, load_value = 1.25, angle = 0.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 90,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 10.0, angle = 180.0,
                           symmetrical = True, abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R4 - Rotating Load, 2.5 kPa',
                           load_no = 4, load_value = 2.5, angle = 270.0,
                           symmetrical = True,  abbrev = 'R4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (0.0, 90.0, 180.0, 270.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        LC1_1 = LoadFactor(load = l1,
                           base_factor = load_factors[0],
                           scale_factor = 4.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 0.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC2_1 = LoadFactor(load = l2,
                           base_factor = load_factors[0],
                           scale_factor = 2.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 90.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC3_1 = LoadFactor(load = l3,
                           base_factor = load_factors[0],
                           scale_factor = 0.5,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 180.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC4_1 = LoadFactor(load = l4,
                           base_factor = load_factors[0],
                           scale_factor = 2.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 270.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})

        LC1_2 = LoadFactor(load = l1,
                           base_factor = load_factors[1],
                           scale_factor = 4.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 0.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC2_2 = LoadFactor(load = l2,
                           base_factor = load_factors[1],
                           scale_factor = 2.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 90.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC3_2 = LoadFactor(load = l3,
                           base_factor = load_factors[1],
                           scale_factor = 0.5,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 180.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})
        LC4_2 = LoadFactor(load = l4,
                           base_factor = load_factors[1],
                           scale_factor  = 2.0,
                           symmetry_factor = 1.0,
                           rotational_factor = 1.0,
                           info = {'angle': 270.0,
                                   'symmetric': False,
                                   'scale_to': 5.0,
                                   'is_scaled': True})

        LC1 = (LC1_1,)
        LC2 = (LC2_1,)
        LC3 = (LC3_1,)
        LC4 = (LC4_1,)

        LC5 = (LC1_2,)
        LC6 = (LC2_2,)
        LC7 = (LC3_2,)
        LC8 = (LC4_2,)

        LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

        LC_act = tuple(LG.generate_groups())

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)

    def test_RotationalGroup_generate_cases_rotated(self):
        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1, load_value = 2.5, angle = 0.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2, load_value = 2.5, angle = 90,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 180.0,
                           symmetrical = True, abbrev = 'R3')

        l4 = RotatableLoad(load_name = 'R4 - Rotating Load, 2.5 kPa',
                           load_no = 4,  load_value = 2.5, angle = 270.0,
                           symmetrical = True,  abbrev = 'R4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (45.0, 135.0, 225.0, 315.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        rad45 = math.radians(45.0)

        LC1 = (LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC2 = (LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l3,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC3 = (LoadFactor(load = l3,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l4,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC4 = (LoadFactor(load = l4,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )


        LC5 = (LoadFactor(load = l1,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC6 = (LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l3,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC7 = (LoadFactor(load = l3,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l4,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )
        LC8 = (LoadFactor(load = l4,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l1,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )

        LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

        LC_act = tuple(LG.generate_groups())

        for i in range(len(LC)):
            print(f'LC1_tst[{i}]: ' + str(LC[i]))
            print(f'LC1_act[{i}]: ' + str(LC_act[i]))
            print(LC[i][0].load == LC_act[i][0].load)
            print(LC[i][0].factor == LC_act[i][0].factor)
            print(LC[i][0].info == LC_act[i][0].info)
            print(LC[i] == LC_act[i])

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)

        req_angles = (15.0, 333.0)
        load_factors = (1.0, )

        LG.req_angles = req_angles
        LG.factors = load_factors

        rad15 = math.radians(15)
        rad63 = math.radians(63)

        cos15 = math.cos(rad15)
        sin15 = math.sin(rad15)
        cos63 = math.cos(rad63)
        sin63 = math.sin(rad63)

        LC1 = (LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = cos15,
                          info = {'angle' : 15.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = sin15,
                          info = {'angle': 15.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )

        LC4 = (LoadFactor(load = l4,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = cos63,
                          info = {'angle': 333.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}),
               LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = sin63,
                          info = {'angle': 333.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True})
               )

        LC = (LC1, LC4)

        LC_act = tuple(LG.generate_groups())

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)

    def test_RotationalGroup_generate_cases_symmetric(self):
        """
        Test the generate_groups function with loads that should test its ability
        to handle symmetric loads.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 1,
                           load_value = 2.5, angle = 0.0,
                           symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 2,
                           load_value = 2.5, angle = 90, symmetrical = True,
                           abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, 2.5 kPa',
                           load_no = 3,
                           load_value = 2.5, angle = 180.0,
                           symmetrical = True,
                           abbrev = 'R3')

        group_name = 'Group 1'
        loads = [l1, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 5.0
        scale = True
        req_angles = (45.0, 135.0, 225.0, 315.0)
        abbrev = 'GP 1'

        LG = RotationalGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_to = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = sine_interp, abbrev = abbrev)

        rad45 = math.radians(45.0)

        LC1 = (LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC2 = (LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l3,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC3 = (LoadFactor(load = l3,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = -1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': True,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC4 = (LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = -1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': True,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )

        LC5 = (LoadFactor(load = l1,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 45,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC6 = (LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l3,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 135.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC7 = (LoadFactor(load = l3,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = -1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 225.0,
                                  'symmetric': True,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC8 = (LoadFactor(load = l2,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = -1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': True,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l1,
                          base_factor = load_factors[1],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = math.sin(rad45),
                          info = {'angle': 315.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )

        LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

        LC_act = tuple(LG.generate_groups())

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)

        req_angles = (15.0, 333.0)
        load_factors = (1.0,)

        LG.req_angles = req_angles
        LG.factors = load_factors

        rad15 = math.radians(15)
        rad63 = math.radians(63)

        cos15 = math.cos(rad15)
        sin15 = math.sin(rad15)
        cos63 = math.cos(rad63)
        sin63 = math.sin(rad63)

        LC1 = (LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = cos15,
                          info = {'angle': 15.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = sin15,
                          info = {'angle': 15.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )
        LC4 = (LoadFactor(load = l2,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = -1.0,
                          rotational_factor = cos63,
                          info = {'angle': 333.0,
                                  'symmetric': True,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          ),
               LoadFactor(load = l1,
                          base_factor = load_factors[0],
                          scale_factor = 2.0,
                          symmetry_factor = 1.0,
                          rotational_factor = sin63,
                          info = {'angle': 333.0,
                                  'symmetric': False,
                                  'scale_to': 5.0,
                                  'is_scaled': True}
                          )
               )

        LC = (LC1, LC4)

        LC_act = tuple(LG.generate_groups())

        self.assertEqual(first = tuple(LG.generate_groups()), second = LC)
