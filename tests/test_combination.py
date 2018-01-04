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
        self.fail()

    def test_add_load_factor(self):
        self.fail()

    def test_del_load(self):
        self.fail()

    def test_load_exists(self):
        self.fail()

    def test_load_factor_exists(self):
        self.fail()

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
        self.fail()

    def test_load_case_abbrev(self):
        self.fail()

    def test_load_case_no(self):
        self.fail()

    def test_combination_title(self):
        self.fail()

    def test_list_load_factors(self):
        self.fail()

    def test_list_loads(self):
        self.fail()

    def test_list_loads_with_factors(self):
        self.fail()
