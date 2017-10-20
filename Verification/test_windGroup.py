# coding=utf-8

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


    def test_loads(self):
        """
        Test the load getter / setter.
        """

        l1 = WindLoad(load = 'W1 - Wind Load, 25m/s', load_no = 3,
                      wind_speed = 25, angle = 45.0, symmetrical = True,
                      abbrev = 'W1')

        l2 = WindLoad(load = 'W2 - Wind Load, 50m/s', load_no = 3,
                      wind_speed = 50, angle = 22.5, symmetrical = True,
                      abbrev = 'W2')

        l3 = WindLoad(load = 'W3 - Wind Load, 75m/s', load_no = 3,
                      wind_speed = 75, angle = 135.0, symmetrical = True,
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

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)

        l1 = WindLoad(load = 'R1 - Rotating Load, 25 kPa', load_no = 3,
                           wind_speed = 25.0, angle = 75.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = WindLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           wind_speed = 25.0, angle = 33.3, symmetrical = True,
                           abbrev = 'R2')

        l3 = WindLoad(load = 'R3 - Rotating Load, -5 kPa', load_no = 3,
                           wind_speed = -25.0, angle = -25, symmetrical = True,
                           abbrev = 'R3')

        self.assertEqual(first = l2.wind_speed, second = l3.wind_speed)

        loads = [l1, l2, l3]

        LG.loads = loads

        loads = [l2, l1, l3]

        self.assertEqual(first = LG.loads, second = loads)


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


    def test_scale(self):
        """
                Test the scale getter / setter
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

        self.assertEqual(first = LG.scale, second = scale)

        scale = False
        LG.scale = scale

        self.assertEqual(first = LG.scale, second = scale)


    def test_req_angles(self):
        """
        Test the getter / setter
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

        self.assertEqual(first = LG.req_angles, second = req_angles)

        req_angles = (0.0, 25.0, 145.0, 210.0, 450.0, -90.0, 570.0)

        LG.req_angles = req_angles

        req_angles = (0.0, 25.0, 90.0, 145.0, 210.0, 270.0)

        self.assertEqual(first = LG.req_angles, second = req_angles)


    def test_interp_func(self):
        """
        Test the interp_func getter / setter
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

        self.assertEqual(first = LG.interp_func, second = wind_interp_85)

        LG.interp_func = sine_interp

        self.assertEqual(first = LG.interp_func, second = sine_interp)


    def test_generate_cases_simple (self):

        l1 = WindLoad(load = 'R1 - Rotating Load, 2.5 kPa', load_no = 3,
                           wind_speed = 25.0, angle = 0.0, symmetrical = True,
                           abbrev = 'R1')

        l2 = WindLoad(load = 'R2 - Rotating Load, 2.5 kPa', load_no = 3,
                           wind_speed = 40.0, angle = 90, symmetrical = True,
                           abbrev = 'R2')

        l3 = WindLoad(load = 'R3 - Rotating Load, 2.5 kPa', load_no = 3,
                           wind_speed = 50.0, angle = 180.0, symmetrical = True,
                           abbrev = 'R3')

        l4 = WindLoad(load = 'R4 - Rotating Load, 2.5 kPa', load_no = 4,
                           wind_speed = 69.0, angle = 270.0, symmetrical = True,
                           abbrev = 'R4')

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
                             interp_func = sine_interp, abbrev = abbrev)

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
        self.fail()


    def test_generate_cases_symmetric (self):
        self.fail()

