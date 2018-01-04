from unittest import TestCase, expectedFailure
from Combination import Combination
from LoadFactor import LoadFactor
from Load import Load

class TestCombination(TestCase):

    @expectedFailure
    def test_basic(self):
        """
        Basic test for the class - can it even be instantiated?
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

        self.fail('Need to implement str & repr methods')

    def test_load_factors(self):
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

    def test_add_load_factor(self):
        self.fail()

    def test_del_load(self):
        self.fail()

    def test_load_exists(self):
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

        C.del_load(load = l1)

        self.assertFalse(C.load_exists(load_no = 1))
        self.assertFalse(C.load_exists(load_name = l1.load_name))
        self.assertFalse(C.load_exists(load = l1))

        C.del_load(load = l2)

        self.assertFalse(C.load_exists(load_no = 2))
        self.assertFalse(C.load_exists(load_name = l2.load_name))
        self.assertFalse(C.load_exists(load = l2))

        self.assertEqual(first = C.load_factors, second = {})

    def test_load_factor_exists(self):
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

        self.assertEqual(C.load_factor_exists(LF1_1), 1)
        self.assertEqual(C.load_factor_exists(LF1_2), 1)
        self.assertEqual(C.load_factor_exists(LF2_1), 2)

        C.del_load_factor(LF1_1)
        C.del_load_factor(LF2_1)
        C.del_load_factor(LF1_2)

        self.assertFalse(C.load_factor_exists(LF1_1))
        self.assertFalse(C.load_factor_exists(LF1_2))
        self.assertFalse(C.load_factor_exists(LF2_1))

    def test_allow_duplicates(self):
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

    def test_load_case(self):
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

    def test_load_case_abbrev(self):
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

    def test_load_case_no(self):
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

    def test_combination_title(self):
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

        print(C.combination_title())

        self.fail()

    def test_list_load_factors(self):
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

    def test_list_loads(self):
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

    def test_list_loads_with_factors(self):
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
