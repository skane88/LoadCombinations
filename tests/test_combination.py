# coding=utf-8

import math
from unittest import TestCase
from LoadCombination.Combination import Combination
from LoadCombination.LoadFactor import LoadFactor
from LoadCombination.Load import Load

class TestCombination(TestCase):

    def test_combination_basic(self):
        """
        Basic test for the class - can it even be instantiated?
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'TL1')

        LF = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = False

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF,
                        allow_duplicates = allow_duplicates)

        print(str(C))

        C2 = eval(repr(C))

        self.assertEqual(first = C, second = C2)

    def test_combination_load_factors(self):
        """
        Test the load_factors getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF1_1,
                        allow_duplicates = allow_duplicates)

        load_factors = {1: [LF1_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        load_factors = {1: [LF1_1, LF1_2]}

        C.add_load_factor(LF1_2)

        self.assertEqual(first = C.load_factors, second = load_factors)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1]}

        C.add_load_factor(LF2_1)

        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF1_2)

        load_factors = {1: [LF1_1], 2: [LF2_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

    def test_combination_add_load_factor(self):
        """
        Test the add_load_factor method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_factors, second = load_factors)

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        #test adding LoadFactors by adding a whole dictionary:
        C.add_load_factor(load_factors)
        self.assertEqual(first = C.load_factors, second = load_factors)

        # reset the load_factors dictionary
        load_factors = {}
        C.load_factors = load_factors

        # test adding a list of LoadFactors:
        load_factors = [LF1_1, LF1_2, LF2_1, LF3_1, LF4_1]
        C.add_load_factor(load_factors)

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

        # reset the load_factors dictionary
        load_factors = {}
        C.load_factors = load_factors

        # test adding a tuple of load factors

        load_factors = (LF1_1, LF1_2, LF2_1, LF3_1, LF4_1)
        C.add_load_factor(load_factors)

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

        # reset the load_factors dictionary
        load_factors = {}
        C.load_factors = load_factors

        # test adding individual load factors
        C.add_load_factor(LF1_1)

        load_factors = {1: [LF1_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

        # reset the load_factors dictionary
        load_factors = {}
        C.load_factors = load_factors

        # test an error if a non-load factor object is added
        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}
        C.load_factors = load_factors

        self.assertRaises(ValueError, C.add_load_factor, 2)

        # test an error if attempting to add multiple load factors
        load_factors = {1: [LF1_1], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}
        C.load_factors = load_factors
        C.allow_duplicates = False

        self.assertRaises(ValueError, C.add_load_factor, LF1_1)
        self.assertRaises(ValueError, C.add_load_factor, LF1_2)

    def test_combination_del_load(self):
        """
        Test the del_load method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load(load_no = 4)
        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load(load_name = l3.load_name)
        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load(load_no = 2)
        load_factors = {1: [LF1_1, LF1_2]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load(load = l1)
        load_factors = {}
        self.assertEqual(first = C.load_factors, second = load_factors)

        self.assertRaises(ValueError, C.del_load, 1)

    def test_combination_del_load_factor(self):
        """
        Test the del_load_factor() method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        C.add_load_factor(LF1_1)

        load_factors = {1: [LF1_1, LF1_2, LF1_1],
                        2: [LF2_1],
                        3: [LF3_1],
                        4: [LF4_1]}

        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF4_1)
        load_factors = {1: [LF1_1, LF1_2, LF1_1],
                        2: [LF2_1],
                        3: [LF3_1]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF3_1)
        load_factors = {1: [LF1_1, LF1_2, LF1_1],
                        2: [LF2_1]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF2_1)
        load_factors = {1: [LF1_1, LF1_2, LF1_1]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF1_1)
        load_factors = {1: [LF1_2]}
        self.assertEqual(first = C.load_factors, second = load_factors)

        C.del_load_factor(LF1_2)
        load_factors = {}
        self.assertEqual(first = C.load_factors, second = load_factors)

        self.assertRaises(ValueError, C.del_load_factor, LF1_1)

    def test_combination_load_exists(self):
        """
        Test the load_exists() method
        """


        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True



        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_factors, second = load_factors)

        self.assertTrue(C.load_exists(load_no = 1))
        self.assertTrue(C.load_exists(load_name = l1.load_name))
        self.assertTrue(C.load_exists(load = l1))

        self.assertTrue(C.load_exists(load_no = 2))
        self.assertTrue(C.load_exists(load_name = l2.load_name))
        self.assertTrue(C.load_exists(load = l2))

        self.assertEqual(first = C.load_exists(load = l1), second = 1)
        self.assertEqual(first = C.load_exists(load = l2), second = 2)

        C.del_load(load = l1)

        self.assertFalse(C.load_exists(load_no = 1))
        self.assertFalse(C.load_exists(load_name = l1.load_name))
        self.assertFalse(C.load_exists(load = l1))

        C.del_load(load = l2)

        self.assertFalse(C.load_exists(load_no = 2))
        self.assertFalse(C.load_exists(load_name = l2.load_name))
        self.assertFalse(C.load_exists(load = l2))

        self.assertEqual(first = C.load_factors, second = {})

    def test_combination_load_factor_exists(self):
        """
        Test the load_factor_exists method
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_factors, second = load_factors)

        self.assertTrue(C.load_factor_exists(LF1_1))
        self.assertTrue(C.load_factor_exists(LF1_2))
        self.assertTrue(C.load_factor_exists(LF2_1))

        self.assertEqual(first = C.load_factor_exists(LF1_1), second = 1)
        self.assertEqual(first = C.load_factor_exists(LF1_2), second = 1)
        self.assertEqual(first = C.load_factor_exists(LF2_1), second = 2)

        C.del_load_factor(LF1_1)
        C.del_load_factor(LF2_1)
        C.del_load_factor(LF1_2)

        self.assertFalse(C.load_factor_exists(LF1_1))
        self.assertFalse(C.load_factor_exists(LF1_2))
        self.assertFalse(C.load_factor_exists(LF2_1))

    def test_combination_allow_duplicates(self):
        """
        Test the allow_duplicates getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = False

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = allow_duplicates, second = C.allow_duplicates)

        allow_duplicates = True

        C.allow_duplicates = allow_duplicates

        self.assertEqual(first = allow_duplicates, second = C.allow_duplicates)

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        with self.assertRaises(ValueError):
            C.allow_duplicates = False

        self.assertTrue(C.allow_duplicates)

    def test_combination_load_case(self):
        """
        Test the load_case getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = False

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_case, second = case_name)

        case_name = 'Case 2'

        C.load_case = case_name

        self.assertEqual(first = C.load_case, second = case_name)

    def test_combination_load_case_abbrev(self):
        """
        Test the load_case_abbrev getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                 load_no = 1,
                 abbrev = '')

        LF = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = False

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_case_abbrev, second = case_abbrev)

        case_abbrev = 'C2'

        C.load_case_abbrev = case_abbrev

        self.assertEqual(first = C.load_case_abbrev, second = case_abbrev)

    def test_combination_load_case_no(self):
        """
        Test the load_case_no getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = False

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = LF,
                        allow_duplicates = allow_duplicates)

        self.assertEqual(first = C.load_case_no, second = case_no)

        case_no = 2

        C.load_case_no = case_no

        self.assertEqual(first = C.load_case_no, second = case_no)

    def test_combination_combination_title(self):
        """
        Test the combination_title method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        expected_title = f'3.00×{l1.abbrev} + 1.00×{l2.abbrev} + 1.00×{l3.abbrev} + 1.00×{l4.abbrev}'

        self.assertEqual(first = C.combination_title(), second = expected_title)

        LF4_1 = LoadFactor(load = l4,
                           base_factor = 0.3,
                           scale_factor = 1.7,
                           rotational_factor =  math.pi)

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        expected_title = f'3.00×{l1.abbrev} + 1.00×{l2.abbrev} + 1.00×{l3.abbrev} + {0.3 * 1.7 * math.pi:0.2f}×{l4.abbrev}'

        self.assertEqual(first = C.combination_title(), second = expected_title)

        expected_title = (f'3.00×{l1.load_name} + '
                          + f'1.00×{l2.load_name} + '
                          + f'1.00×{l3.load_name} + '
                          + f'{0.3 * 1.7 * math.pi:0.2f}×{l4.load_name}')

        self.assertEqual(first = C.combination_title(abbreviate = False),
                         second = expected_title)

        expected_title = (f'1.00×{l1.abbrev} + '
                          + f'2.00×{l1.abbrev} + '
                          + f'1.00×{l2.abbrev} + '
                          + f'1.00×{l3.abbrev} + '
                          + f'{0.3 * 1.7 * math.pi:0.2f}×{l4.abbrev}')

        self.assertEqual(first = C.combination_title(combine_same_loads = False),
                         second = expected_title)

        expected_title = (f'3.00×{l1.abbrev}2p1'
                          + f'1.00×{l2.abbrev}2p1'
                          + f'1.00×{l3.abbrev}2p1'
                          + f'{0.3 * 1.7 * math.pi:0.2f}×{l4.abbrev}')

        self.assertEqual(first = C.combination_title(separator = '2p1'),
                         second = expected_title)

        expected_title = (f'3.00-*-{l1.abbrev} + '
                          + f'1.00-*-{l2.abbrev} + '
                          + f'1.00-*-{l3.abbrev} + '
                          + f'{0.3 * 1.7 * math.pi:0.2f}-*-{l4.abbrev}')

        self.assertEqual(first = C.combination_title(times_sign = '-*-'),
                         second = expected_title)

        expected_title = (f'3.00000×{l1.abbrev} + '
                          + f'1.00000×{l2.abbrev} + '
                          + f'1.00000×{l3.abbrev} + '
                          + f'{0.3 * 1.7 * math.pi:0.5f}×{l4.abbrev}')

        self.assertEqual(first = C.combination_title(precision = 5),
                         second = expected_title)

    def test_combination_list_load_factors(self):
        """
        Test the list_load_factors method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = '')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = '')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        load_factors = [LF1_1, LF1_2, LF2_1, LF3_1, LF4_1]
        load_factors = sorted(load_factors, key = lambda x: x.load.load_no)

        self.assertEqual(first = C.list_load_factors, second = load_factors)

    def test_combination_list_loads(self):
        """
        Test the list_loads method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = '')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = '')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        load_list = [l1, l2, l3, l4]
        load_list = sorted(load_list, key = lambda x: x.load_no)

        self.assertEqual(first = C.list_loads, second = load_list)

    def test_combination_list_loads_with_factors(self):
        """
        Test the list_load_factors method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = '')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = '')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True

        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        out_list = {1: (3.0, l1, [LF1_1, LF1_2]),
                    2: (1.0, l2, [LF2_1]),
                    3: (1.0, l3, [LF3_1]),
                    4: (1.0, l4, [LF4_1])}

        self.assertEqual(first = C.list_loads_with_factors, second = out_list)

    def test_combination_count_load_factors(self):
        """
        Test the count_load_factors property.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True
        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        C.add_load_factor(LF1_1)
        C.add_load_factor(LF1_1)
        C.add_load_factor(LF3_1)

        count = [(LF1_1, 3), (LF1_2, 1), (LF2_1, 1), (LF3_1, 2), (LF4_1, 1)]

        self.assertEqual(first = C.count_load_factors, second = count)

    def test_combination_count_load_factors_per_load(self):
        """
        Test the count_load_factors_per_load property.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = 'l1')

        LF1_1 = LoadFactor(load = l1)
        LF1_2 = LoadFactor(load = l1, base_factor = 2.0)

        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = 'l2')

        LF2_1 = LoadFactor(load = l2)

        l3 = Load(load_name = 'Test Load 3',
                  load_no = 3,
                  abbrev = 'l3')

        LF3_1 = LoadFactor(load = l3)

        l4 = Load(load_name = 'Test Load 4',
                  load_no = 4,
                  abbrev = 'l4')

        LF4_1 = LoadFactor(load = l4)

        case_no = 1
        case_name = 'Case 1'
        case_abbrev = 'C1'
        allow_duplicates = True
        load_factors = {1: [LF1_1, LF1_2], 2: [LF2_1], 3: [LF3_1], 4: [LF4_1]}

        C = Combination(load_case_no = case_no,
                        load_case = case_name,
                        load_case_abbrev = case_abbrev,
                        load_factors = load_factors,
                        allow_duplicates = allow_duplicates)

        C.add_load_factor(LF1_1)
        C.add_load_factor(LF1_1)
        C.add_load_factor(LF3_1)

        count = {1: 4, 2: 1, 3: 2, 4: 1}

        self.assertEqual(first = C.count_load_factors_per_load, second = count)

    def test_copy(self):

        self.fail()
