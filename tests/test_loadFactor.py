from unittest import TestCase
from Load import Load
from LoadFactor import LoadFactor

class TestLoadFactor(TestCase):

    def test_basic(self):
        """
        Carry out basic testing - can the object be instantiated and can the
        str() and repr() methods be used?
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        print(LF)

        print(repr(l1))
        print(repr(LF.load))
        print(repr(LF))

        LF2 = eval(repr(LF))

        self.assertEqual(first = LF, second = LF2)

    def test_load(self):
        """
        Test the load getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')
        l2 = Load(load_name = 'Test Load 2',
                  load_no = 2,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        self.assertEqual(first = LF.load, second = l1)

        LF.load = l2

        self.assertEqual(first = LF.load, second = l2)

    def test_base_factor(self):
        """
        Test the base_factor getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        base_factor = 2.0

        LF = LoadFactor(load = l1, base_factor = base_factor)

        self.assertEqual(first = LF.base_factor, second = base_factor)

        base_factor = 3.0

        LF.base_factor = base_factor

        self.assertEqual(first = LF.base_factor, second = base_factor)

    def test_scale_factor(self):
        """
        Test the scale_factor getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        scale_factor = 2.0

        LF = LoadFactor(load = l1, scale_factor = scale_factor)

        self.assertEqual(first = LF.scale_factor, second = scale_factor)

        scale_factor = 3.0

        LF.scale_factor = scale_factor

        self.assertEqual(first = LF.scale_factor, second = scale_factor)

    def test_rotational_factor(self):
        """
        Test the rotational_factor getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        rotational_factor = 2.0

        LF = LoadFactor(load = l1, rotational_factor = rotational_factor)

        self.assertEqual(first = LF.rotational_factor,
                         second = rotational_factor)

        rotational_factor = 3.0

        LF.rotational_factor = rotational_factor

        self.assertEqual(first = LF.rotational_factor,
                         second = rotational_factor)

    def test_symmetry_factor(self):
        """
        Test the symmetry_factor getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        symmetry_factor = 1.0

        LF = LoadFactor(load = l1, symmetry_factor = symmetry_factor)

        self.assertEqual(first = LF.symmetry_factor, second = symmetry_factor)

        symmetry_factor = -1.0

        LF.symmetry_factor = symmetry_factor

        self.assertEqual(first = LF.symmetry_factor, second = symmetry_factor)

        # now test the error checking with a few different values for
        # symmetry factors - these should all fail as symmetry_factor should
        # only be 1.0 or -1.0

        s_factors = [-2.0, -0.5, 0.0, 0.5, 2.0]

        for s in s_factors:

            with self.assertRaises(ValueError):
                LF.symmetry_factor = s

    def test_group_factor(self):
        """
        Test the group_factor getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        group_factor = 2.0

        LF = LoadFactor(load = l1, group_factor = group_factor)

        self.assertEqual(first = LF.group_factor, second = group_factor)

        group_factor = 3.0

        LF.group_factor = group_factor

        self.assertEqual(first = LF.group_factor, second = group_factor)

    def test_factor(self):

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        base_factor = 1.0
        scale_factor = 2.0
        rotational_factor = 3.0
        symmetry_factor = 1.0
        group_factor = 5.0

        LF = LoadFactor(load = l1,
                        base_factor = base_factor,
                        scale_factor = scale_factor,
                        rotational_factor = rotational_factor,
                        symmetry_factor = symmetry_factor,
                        group_factor = group_factor)

        factor = (base_factor * scale_factor * rotational_factor *
                  symmetry_factor * group_factor)


        self.assertEqual(first = LF.factor, second = factor)

        base_factor = 10.0
        scale_factor = -2.0
        rotational_factor = 5.0
        symmetry_factor = -1.0
        group_factor = 8.3

        LF.base_factor = base_factor
        LF.scale_factor = scale_factor
        LF.rotational_factor = rotational_factor
        LF.symmetry_factor = symmetry_factor
        LF.group_factor = group_factor

        factor = (base_factor * scale_factor * rotational_factor *
                  symmetry_factor * group_factor)

        self.assertEqual(first = LF.factor, second = factor)

    def test_info(self):
        """
        Test the info getter / setter
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        info = {'angle': 30.0,
                'symmetric': False,
                'scale_to': 5.0,
                'is_scaled': True}

        LF = LoadFactor(load = l1, info = info)

        self.assertEqual(first = LF.info, second = info)

        info = {'angle': 45.0,
                'symmetric': True,
                'scale_to': 2.0,
                'is_scaled': False}

        LF.info = info

        self.assertEqual(first = LF.info, second = info)

    def test_add_info(self):
        """
        Test the add_info method.
        """

        l1 = Load(load_name = 'Test Load',
                  load_no = 1,
                  abbrev = '')

        LF = LoadFactor(load = l1)

        # get an empty dictionary for testing
        info = {}

        self.assertEqual(first = LF.info, second = info)

        LF.add_info()

        self.fail()
