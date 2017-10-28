# coding=utf-8

"""
Tests for the RotationalGroup class.
"""
import math
from unittest import TestCase
from LoadGroup import RotationalGroup, LoadFactor
from Load import RotatableLoad
from HelperFuncs import sine_interp, linear_interp

class TestRotationalGroup(TestCase):

    def test_basic(self):
        """
        Test the initialisation and __str__ and __repr__ methods.
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 22.5,
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


    def test_loads(self):
        '''
        Test the load getter / setter.
        '''

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 22.5,
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

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 25 kPa',
                           load_no = 3, load_value = 25, angle = 75.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 33.3,
                           symmetrical = True, abbrev = 'R2')

        l3 = RotatableLoad(load_name = 'R3 - Rotating Load, -5 kPa',
                           load_no = 3, load_value = -5, angle = -25,
                           symmetrical = True, abbrev = 'R3')

        loads = [l1, l2, l3]

        LG.loads = loads

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)


    def test_req_angles(self):
        """
        Test the getter / setter
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 22.5,
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


    def test_interp_func(self):
        """
        Test the interp_func getter / setter
        """

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 5 kPa', load_no = 3,
                           load_value = 5, angle = 45.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 22.5,
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


    def test_generate_cases_simple(self):
        '''
        Test the generate_cases method which returns the output load
        combinations.

        This test only tests the case where the required angles are already
        in the list of loads.
        '''

        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 1.25, angle = 0.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 90,
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

        LC1_1 = LoadFactor(l1, -4.0, '(Rotated: 0.0)')
        LC2_1 = LoadFactor(l2, -2.0, '(Rotated: 90.0)')
        LC3_1 = LoadFactor(l3, -0.5, '(Rotated: 180.0)')
        LC4_1 = LoadFactor(l4, -2.0, '(Rotated: 270.0)')

        LC1_2 = LoadFactor(l1, 4.0, '(Rotated: 0.0)')
        LC2_2 = LoadFactor(l2, 2.0, '(Rotated: 90.0)')
        LC3_2 = LoadFactor(l3, 0.5, '(Rotated: 180.0)')
        LC4_2 = LoadFactor(l4, 2.0, '(Rotated: 270.0)')

        LC1 = (LC1_1,)
        LC2 = (LC2_1,)
        LC3 = (LC3_1,)
        LC4 = (LC4_1,)

        LC5 = (LC1_2, )
        LC6 = (LC2_2,)
        LC7 = (LC3_2,)
        LC8 = (LC4_2,)

        LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

        LC_act = tuple(LG.generate_cases())

        for i in range(len(LC)):
            print(f'LC1_tst[{i}]: ' + str(LC[i]))
            print(f'LC1_act[{i}]: ' + str(LC_act[i]))
            print(LC[i][0].load == LC_act[i][0].load)
            print(LC[i][0].load_factor == LC_act[i][0].load_factor)
            print(LC[i][0].add_info == LC_act[i][0].add_info)
            print(LC[i] == LC_act[i])

        self.assertEqual(first = tuple(LG.generate_cases()), second = LC)


    def test_generate_cases_rotated(self):
        l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 0.0,
                           symmetrical = True, abbrev = 'R1')

        l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                           load_no = 3, load_value = 2.5, angle = 90,
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

        LC1 = (LoadFactor(l1, -2.0 * math.sin(rad45), '(Rotated: 45.0)'),
               LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 45.0)'))
        LC2 = (LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 135.0)'),
               LoadFactor(l3, -2.0 * math.sin(rad45), '(Rotated: 135.0)'))
        LC3= (LoadFactor(l3, -2.0 * math.sin(rad45), '(Rotated: 225.0)'),
               LoadFactor(l4, -2.0 * math.sin(rad45), '(Rotated: 225.0)'))
        LC4 = (LoadFactor(l4, -2.0 * math.sin(rad45), '(Rotated: 315.0)'),
               LoadFactor(l1, -2.0 * math.sin(rad45), '(Rotated: 315.0)'))


        LC5 = (LoadFactor(l1, 2.0 * math.sin(rad45), '(Rotated: 45.0)'),
               LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 45.0)'))
        LC6 = (LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 135.0)'),
               LoadFactor(l3, 2.0 * math.sin(rad45), '(Rotated: 135.0)'))
        LC7= (LoadFactor(l3, 2.0 * math.sin(rad45), '(Rotated: 225.0)'),
               LoadFactor(l4, 2.0 * math.sin(rad45), '(Rotated: 225.0)'))
        LC8 = (LoadFactor(l4, 2.0 * math.sin(rad45), '(Rotated: 315.0)'),
               LoadFactor(l1, 2.0 * math.sin(rad45), '(Rotated: 315.0)'))

        LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

        LC_act = tuple(LG.generate_cases())

        for i in range(len(LC)):
            print(f'LC1_tst[{i}]: ' + str(LC[i]))
            print(f'LC1_act[{i}]: ' + str(LC_act[i]))
            print(LC[i][0].load == LC_act[i][0].load)
            print(LC[i][0].load_factor == LC_act[i][0].load_factor)
            print(LC[i][0].add_info == LC_act[i][0].add_info)
            print(LC[i] == LC_act[i])

        self.assertEqual(first = tuple(LG.generate_cases()), second = LC)

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

        LC1 = (LoadFactor(l1, 2.0 * cos15, '(Rotated: 15.0)'),
               LoadFactor(l2, 2.0 * sin15, '(Rotated: 15.0)'))
        LC4 = (LoadFactor(l4, 2.0 * cos63, '(Rotated: 333.0)'),
               LoadFactor(l1, 2.0 * sin63, '(Rotated: 333.0)'))

        LC = (LC1, LC4)

        LC_act = tuple(LG.generate_cases())

        for i in range(len(LC)):
            print(f'LC1_tst[{i}]: ' + str(LC[i]))
            print(f'LC1_act[{i}]: ' + str(LC_act[i]))
            print(LC[i][0].load == LC_act[i][0].load)
            print(LC[i][0].load_factor == LC_act[i][0].load_factor)
            print(LC[i][0].add_info == LC_act[i][0].add_info)
            print(LC[i] == LC_act[i])

        self.assertEqual(first = tuple(LG.generate_cases()), second = LC)


    def test_generate_cases_symmetric(self):
            l1 = RotatableLoad(load_name = 'R1 - Rotating Load, 2.5 kPa',
                               load_no = 3,
                               load_value = 2.5, angle = 0.0,
                               symmetrical = True,
                               abbrev = 'R1')

            l2 = RotatableLoad(load_name = 'R2 - Rotating Load, 2.5 kPa',
                               load_no = 3,
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

            LC1 = (LoadFactor(l1, -2.0 * math.sin(rad45), '(Rotated: 45.0)'),
                   LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 45.0)'))
            LC2 = (LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 135.0)'),
                   LoadFactor(l3, -2.0 * math.sin(rad45), '(Rotated: 135.0)'))
            LC3 = (LoadFactor(l3, -2.0 * math.sin(rad45), '(Rotated: 225.0)'),
                   LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 225.0)'))
            LC4 = (LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 315.0)'),
                   LoadFactor(l1, -2.0 * math.sin(rad45), '(Rotated: 315.0)'))

            LC5 = (LoadFactor(l1, 2.0 * math.sin(rad45), '(Rotated: 45.0)'),
                   LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 45.0)'))
            LC6 = (LoadFactor(l2, 2.0 * math.sin(rad45), '(Rotated: 135.0)'),
                   LoadFactor(l3, 2.0 * math.sin(rad45), '(Rotated: 135.0)'))
            LC7 = (LoadFactor(l3, 2.0 * math.sin(rad45), '(Rotated: 225.0)'),
                   LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 225.0)'))
            LC8 = (LoadFactor(l2, -2.0 * math.sin(rad45), '(Rotated: 315.0)'),
                   LoadFactor(l1, 2.0 * math.sin(rad45), '(Rotated: 315.0)'))

            LC = (LC1, LC2, LC3, LC4, LC5, LC6, LC7, LC8)

            LC_act = tuple(LG.generate_cases())

            for i in range(len(LC)):
                print(f'LC1_tst[{i}]: ' + str(LC[i]))
                print(f'LC1_act[{i}]: ' + str(LC_act[i]))
                print(LC[i][0].load == LC_act[i][0].load)
                print(LC[i][0].load_factor == LC_act[i][0].load_factor)
                print(LC[i][0].add_info == LC_act[i][0].add_info)
                print(LC[i] == LC_act[i])

            self.assertEqual(first = tuple(LG.generate_cases()), second = LC)

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

            LC1 = (LoadFactor(l1, 2.0 * cos15, '(Rotated: 15.0)'),
                   LoadFactor(l2, 2.0 * sin15, '(Rotated: 15.0)'))
            LC4 = (LoadFactor(l2, -2.0 * cos63, '(Rotated: 333.0)'),
                   LoadFactor(l1, 2.0 * sin63, '(Rotated: 333.0)'))

            LC = (LC1, LC4)

            LC_act = tuple(LG.generate_cases())

            for i in range(len(LC)):
                print(f'LC1_tst[{i}]: ' + str(LC[i]))
                print(f'LC1_act[{i}]: ' + str(LC_act[i]))
                print(LC[i][0].load == LC_act[i][0].load)
                print(LC[i][0].load_factor == LC_act[i][0].load_factor)
                print(LC[i][0].add_info == LC_act[i][0].add_info)
                print(LC[i] == LC_act[i])

            self.assertEqual(first = tuple(LG.generate_cases()), second = LC)
