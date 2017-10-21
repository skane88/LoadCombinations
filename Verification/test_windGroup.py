# coding=utf-8

import math
from unittest import TestCase
from LoadGroup import WindGroup, LoadFactor
from Load import WindLoad
from HelperFuncs import sine_interp, wind_interp_85

class TestWindGroup(TestCase):

    def test_basic(self):
        """
        Test the initialisation and __str__ and __repr__ methods.
        """

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                           wind_speed = 25, angle = 45.0, symmetrical = True,
                           abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 50m/s', load_no = 3,
                           wind_speed = 50, angle = 45.0, symmetrical = True,
                           abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 75m/s', load_no = 3,
                           wind_speed = 75, angle = 45.0, symmetrical = True,
                           abbrev = 'W3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_speed = 69.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = WindGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_speed = scale_speed,
                             scale = scale, req_angles = req_angles,
                             interp_func = wind_interp_85, abbrev = abbrev)

        print(LG)
        print(repr(LG))

        # can the __repr__ method instantiate an object?

        LG2 = eval(repr(LG))

        # does the __str__ method result in equal strings

        self.assertEqual(first = str(LG), second = str(LG2))


    def test_scale_speed(self):
        """
        Test the scale_speed method.
        """

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                      wind_speed = 25, angle = 45.0, symmetrical = True,
                      abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 50m/s', load_no = 3,
                      wind_speed = 50, angle = 45.0, symmetrical = True,
                      abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 75m/s', load_no = 3,
                      wind_speed = 75, angle = 45.0, symmetrical = True,
                      abbrev = 'W3')

        group_name = 'Group 1'
        loads = [l1, l2, l3]
        load_factors = (-1.0, 0, 1.0)
        scale_speed = 69.0
        scale = True
        req_angles = (0, 90, 180, 270)
        abbrev = 'GP 1'

        LG = WindGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_speed = scale_speed,
                             scale = scale, req_angles = req_angles,
                             interp_func = wind_interp_85, abbrev = abbrev)

        self.assertEqual(first = LG.scale_speed, second = scale_speed)

        scale_speed = 35.0
        LG.scale_speed = scale_speed

        self.assertEqual(first = LG.scale_speed, second = scale_speed)


    def test_generate_cases_simple (self):

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                           wind_speed = 25.0, angle = 0.0, symmetrical = True,
                           abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 40m/s', load_no = 3,
                           wind_speed = 40.0, angle = 90, symmetrical = True,
                           abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 50m/s', load_no = 3,
                           wind_speed = 50.0, angle = 180.0, symmetrical = True,
                           abbrev = 'W3')

        l4 = WindLoad(load = 'W4 - Wind Load, 69m/s', load_no = 4,
                           wind_speed = 69.0, angle = 270.0, symmetrical = True,
                           abbrev = 'W4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 69.0
        scale = True
        req_angles = (0.0, 90.0, 180.0, 270.0)
        abbrev = 'GP 1'

        LG = WindGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_speed = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = wind_interp_85, abbrev = abbrev)

        LC1_1 = LoadFactor(l1, -((69.0 * 69.0) / (25.0 * 25.0)), '(Rotated: 0.0)')
        LC2_1 = LoadFactor(l2, -((69.0 * 69.0) / (40.0 * 40.0)), '(Rotated: 90.0)')
        LC3_1 = LoadFactor(l3, -((69.0 * 69.0) / (50.0 * 50.0)), '(Rotated: 180.0)')
        LC4_1 = LoadFactor(l4, -((69.0 * 69.0) / (69.0 * 69.0)), '(Rotated: 270.0)')

        LC1_2 = LoadFactor(l1, ((69.0 * 69.0) / (25.0 * 25.0)), '(Rotated: 0.0)')
        LC2_2 = LoadFactor(l2, ((69.0 * 69.0) / (40.0 * 40.0)), '(Rotated: 90.0)')
        LC3_2 = LoadFactor(l3, ((69.0 * 69.0) / (50.0 * 50.0)), '(Rotated: 180.0)')
        LC4_2 = LoadFactor(l4, ((69.0 * 69.0) / (69.0 * 69.0)), '(Rotated: 270.0)')

        LC1 = (LC1_1,)
        LC2 = (LC2_1,)
        LC3 = (LC3_1,)
        LC4 = (LC4_1,)

        LC5 = (LC1_2,)
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


    def test_generate_cases_rotated (self):

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                      wind_speed = 25.0, angle = 0.0, symmetrical = True,
                      abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 40m/s', load_no = 3,
                      wind_speed = 40.0, angle = 90, symmetrical = True,
                      abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 50m/s', load_no = 3,
                      wind_speed = 50.0, angle = 180.0, symmetrical = True,
                      abbrev = 'W3')

        l4 = WindLoad(load = 'W4 - Wind Load, 69m/s', load_no = 4,
                      wind_speed = 69.0, angle = 270.0, symmetrical = True,
                      abbrev = 'W4')

        group_name = 'Group 1'
        loads = [l1, l4, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 69.0
        scale = True
        req_angles = (45.0, 135.0, 225.0, 315.0)
        abbrev = 'GP 1'

        LG = WindGroup(group_name = group_name, loads = loads,
                             factors = load_factors, scale_speed = scale_to,
                             scale = scale, req_angles = req_angles,
                             interp_func = wind_interp_85, abbrev = abbrev)

        rad45 = math.radians(45.0)

        LC1 = (LoadFactor(l1, -((69**2) / (25**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'),
               LoadFactor(l2, -((69**2) / (40**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'))
        LC2 = (LoadFactor(l2, -((69**2) / (40**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'),
               LoadFactor(l3, -((69**2) / (50**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'))
        LC3 = (LoadFactor(l3, -((69**2) / (50**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'),
               LoadFactor(l4, -((69**2) / (69**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'))
        LC4 = (LoadFactor(l4, -((69**2) / (69**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'),
               LoadFactor(l1, -((69**2) / (25**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'))

        LC5 = (LoadFactor(l1, ((69**2) / (25**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'),
               LoadFactor(l2, ((69**2) / (40**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'))
        LC6 = (LoadFactor(l2, ((69**2) / (40**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'),
               LoadFactor(l3, ((69**2) / (50**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'))
        LC7 = (LoadFactor(l3, ((69**2) / (50**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'),
               LoadFactor(l4, ((69**2) / (69**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'))
        LC8 = (LoadFactor(l4, ((69**2) / (69**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'),
               LoadFactor(l1, ((69**2) / (25**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'))

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

        # The floats in the following function are calculated from the
        # wind_interp_85 function.
        LC1 = (LoadFactor(l1, ((69**2) / (25**2)) * 0.9920769026062272,
                          '(Rotated: 15.0)'),
               LoadFactor(l2, ((69**2) / (40**2)) * 0.2658262048829081,
                          '(Rotated: 15.0)'))
        LC4 = (LoadFactor(l4, ((69**2) / (69**2)) * 0.49180807008686556,
                          '(Rotated: 333.0)'),
               LoadFactor(l1, ((69**2) / (25**2)) * 0.9652276850446957,
                          '(Rotated: 333.0)'))

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


    def test_generate_cases_symmetric (self):

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                      wind_speed = 25.0, angle = 0.0, symmetrical = True,
                      abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 40m/s', load_no = 3,
                      wind_speed = 40.0, angle = 90, symmetrical = True,
                      abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 50m/s', load_no = 3,
                      wind_speed = 50.0, angle = 180.0, symmetrical = True,
                      abbrev = 'W3')

        group_name = 'Group 1'
        loads = [l1, l3, l2]
        load_factors = (-1.0, 1.0)
        scale_to = 69.0
        scale = True
        req_angles = (45.0, 135.0, 225.0, 315.0)
        abbrev = 'GP 1'

        LG = WindGroup(group_name = group_name, loads = loads,
                       factors = load_factors, scale_speed = scale_to,
                       scale = scale, req_angles = req_angles,
                       interp_func = wind_interp_85, abbrev = abbrev)

        rad45 = math.radians(45.0)

        LC1 = (LoadFactor(l1, -((69.0**2) / (25.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'),
               LoadFactor(l2, -((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'))
        LC2 = (LoadFactor(l2, -((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'),
               LoadFactor(l3, -((69.0**2) / (50.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 135.0)'))
        LC3 = (LoadFactor(l3, -((69.0**2) / (50.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'),
               LoadFactor(l2, ((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 225.0)'))
        LC4 = (LoadFactor(l2, ((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'),
               LoadFactor(l1, -((69.0**2) / (25.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 315.0)'))

        LC5 = (LoadFactor(l1, ((69.0**2) / (25.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 45.0)'),
               LoadFactor(l2, ((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                          '(Rotated: 45.0)'))
        LC6 = (LoadFactor(l2, ((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 135.0)'),
               LoadFactor(l3, ((69.0**2) / (50.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 135.0)'))
        LC7 = (LoadFactor(l3, ((69.0**2) / (50.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 225.0)'),
               LoadFactor(l2, -((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 225.0)'))
        LC8 = (LoadFactor(l2, -((69.0**2) / (40.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 315.0)'),
               LoadFactor(l1, ((69.0**2) / (25.0**2)) * math.sin(rad45) * 1.20208,
                        '(Rotated: 315.0)'))

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

        LC1 = (LoadFactor(l1, ((69.0**2) / (25.0**2)) * 0.9920769026062272, '(Rotated: 15.0)'),
               LoadFactor(l2, ((69.0**2) / (40.0**2)) * 0.2658262048829081, '(Rotated: 15.0)'))
        LC4 = (LoadFactor(l2, -((69.0**2) / (40.0**2)) * 0.49180807008686556, '(Rotated: 333.0)'),
               LoadFactor(l1, ((69.0**2) / (25.0**2)) * 0.9652276850446957, '(Rotated: 333.0)'))

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


