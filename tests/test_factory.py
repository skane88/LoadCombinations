from unittest import TestCase

from LoadCombination import Factory
from LoadCombination.Load import Load, WindLoad, RotatableLoad, ScalableLoad

class TestBuildLoad(TestCase):

    def test_BuildLoad(self):

        load_name = 'Load'
        load_no = 1
        abbrev = ''

        basic_load = Load(load_name = load_name, load_no = load_no,
                          abbrev = abbrev)

        load_value = 5.0

        scale_load = ScalableLoad(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value)

        angle = 90.0
        symmetrical = True

        rotate_load = RotatableLoad(load_name = load_name, load_no = load_no,
                                    abbrev = abbrev, load_value = load_value,
                                    angle = angle, symmetrical = symmetrical)

        wind_speed = 69.0

        wind_load = WindLoad(load_name = load_name, load_no = load_no,
                             abbrev = abbrev, wind_speed = wind_speed,
                             angle = angle, symmetrical = symmetrical)

        build_load = Factory.build_load

        with self.subTest('Test basic Load'):

            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev)

            self.assertEqual(first = test_load, second = basic_load)

        with self.subTest('Test ScalableLoad'):

            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value)

            self.assertEqual(first = test_load, second = scale_load)

        with self.subTest('Test RotatableLoad'):

            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value,
                                  angle = angle, symmetrical = symmetrical)

            self.assertEqual(first = test_load, second = rotate_load)

        with self.subTest('Test WindLoad'):

            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, wind_speed = wind_speed,
                                  angle = angle, symmetrical = symmetrical)

            self.assertEqual(first = test_load, second = wind_load)

        with self.subTest('Test Load with load_type param'):
            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_type = Load)

            self.assertEqual(first = test_load, second = basic_load)

        with self.subTest('Test ScalableLoad with load_type param'):

            test_load = build_load(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value,
                                  load_type = ScalableLoad)

            self.assertEqual(first = test_load, second = scale_load)


    def test_LoadFromDict(self):
        load_name = 'Load'
        load_no = 1
        abbrev = ''

        basic_load = Load(load_name = load_name, load_no = load_no,
                          abbrev = abbrev)

        load_value = 5.0

        scale_load = ScalableLoad(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value)

        angle = 90.0
        symmetrical = True

        rotate_load = RotatableLoad(load_name = load_name, load_no = load_no,
                                    abbrev = abbrev, load_value = load_value,
                                    angle = angle, symmetrical = symmetrical)

        wind_speed = 69.0

        wind_load = WindLoad(load_name = load_name, load_no = load_no,
                             abbrev = abbrev, wind_speed = wind_speed,
                             angle = angle, symmetrical = symmetrical)

        load_from_dict = Factory.load_from_dict

        with self.subTest('Test basic Load'):

            test_dict = {'load_name': load_name, 'load_no': load_no,
                         'abbrev': abbrev}

            test_load = load_from_dict(test_dict)

            self.assertEqual(first = test_load, second = basic_load)

        with self.subTest('Test ScalableLoad'):

            test_dict = {'load_name': load_name, 'load_no': load_no,
                         'abbrev': abbrev, 'load_value': load_value}

            test_load = load_from_dict(test_dict)

            self.assertEqual(first = test_load, second = scale_load)

        with self.subTest('Test RotatableLoad'):

            test_dict = {'load_name': load_name, 'load_no': load_no,
                         'abbrev': abbrev, 'load_value': load_value,
                         'angle': angle, 'symmetrical': symmetrical}

            test_load = load_from_dict(test_dict)

            self.assertEqual(first = test_load, second = rotate_load)

        with self.subTest('Test WindLoad'):

            test_dict = {'load_name': load_name, 'load_no': load_no,
                         'abbrev': abbrev, 'wind_speed': wind_speed,
                         'angle': angle, 'symmetrical': symmetrical}

            test_load = load_from_dict(test_dict)

            self.assertEqual(first = test_load, second = wind_load)


    def testLoadFromString(self):
        load_name = 'Load'
        load_no = 1
        abbrev = ''

        basic_load = Load(load_name = load_name, load_no = load_no,
                          abbrev = abbrev)

        load_value = 5.0

        scale_load = ScalableLoad(load_name = load_name, load_no = load_no,
                                  abbrev = abbrev, load_value = load_value)

        angle = 90.0
        symmetrical = True

        rotate_load = RotatableLoad(load_name = load_name, load_no = load_no,
                                    abbrev = abbrev, load_value = load_value,
                                    angle = angle, symmetrical = symmetrical)

        wind_speed = 69.0

        wind_load = WindLoad(load_name = load_name, load_no = load_no,
                             abbrev = abbrev, wind_speed = wind_speed,
                             angle = angle, symmetrical = symmetrical)

        load_from_string = Factory.load_from_string

        with self.subTest('Test basic Load'):
            test_string = (f'load_name: {load_name}, load_no: {load_no},'
                           + f'abbrev: {abbrev}')

            test_load = load_from_string(test_string)

            self.assertEqual(first = test_load, second = basic_load)

        with self.subTest('Test ScalableLoad'):
            test_string = (f'load_name: {load_name}, load_no: {load_no},'
                           + f'abbrev: {abbrev}, load_value: {load_value}')

            test_load = load_from_string(test_string)

            self.assertEqual(first = test_load, second = scale_load)

        with self.subTest('Test RotatableLoad'):
            test_string = (f'load_name: {load_name}, load_no: {load_no},'
                           + f'abbrev: {abbrev}, load_value: {load_value},'
                           + f'angle: {angle}, symmetrical: {symmetrical}')

            test_load = load_from_string(test_string)

            self.assertEqual(first = test_load, second = rotate_load)

        with self.subTest('Test WindLoad'):
            test_string = (f'load_name: {load_name}, load_no: {load_no},'
                           + f'abbrev: {abbrev}, wind_speed: {wind_speed},'
                           + f'angle: {angle}, symmetrical: {symmetrical}')

            test_load = load_from_string(test_string)

            self.assertEqual(first = test_load, second = wind_load)

    def test_buildGroup(self):
        self.fail()

    def test_groupFromString(self):
        self.fail()

    def test_groupFromDict(self):

        self.fail()

