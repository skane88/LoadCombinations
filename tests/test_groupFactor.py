from unittest import TestCase
from GroupFactor import GroupFactor
from LoadGroup import LoadGroup
from Load import Load

class TestGroupFactor(TestCase):

    def test_basic(self):
        """
        Test whether the GroupFactor can be instantiated and whether str & repr
        methods work.
        """

        load_1= Load(load_name = "Test Load", load_no = 1, abbrev = "TL")
        group_1 = LoadGroup(group_name  ="Test Group",
                            loads = load_1,
                            abbrev = "")

        GF = GroupFactor(load_group = group_1, group_factor = 2.0)

        print(GF)

        GF2 = eval(repr(GF))

        print(GF2)

        self.assertEqual(first = str(GF), second = str(GF2))

    def test_load_group(self):
        """
        Test the load_group getter and setter function
        """


        load_1= Load(load_name = "Test Load", load_no = 1, abbrev = "TL")
        group_1 = LoadGroup(group_name  ="Test Group",
                            loads = load_1,
                            abbrev = "")

        GF = GroupFactor(load_group = group_1, group_factor = 2.0)

        self.assertEqual(first = group_1, second = GF.load_group)

        load_2 = Load(load_name = 'Test Load 2', load_no = 2, abbrev = 'TL2')
        group_2 = LoadGroup(group_name = "Test Group 2",
                            loads = load_2,
                            abbrev = "")

        GF.load_group = group_2

        self.assertEqual(first = group_2, second = GF.load_group)

    def test_group_factor(self):
        """
        Test the group_factor getter & setter
        """

        load_1= Load(load_name = "Test Load", load_no = 1, abbrev = "TL")
        group_1 = LoadGroup(group_name  ="Test Group",
                            loads = load_1,
                            abbrev = "")
        factor = 2.0

        GF = GroupFactor(load_group = group_1, group_factor = factor)

        self.assertEqual(first = factor, second = GF.group_factor)

        factor = 3.0
        GF.group_factor = factor

        self.assertEqual(first = factor, second = GF.group_factor)

