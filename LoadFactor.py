# coding=utf-8

"""
This file contains a helper class to associate a ``Load`` with combination
factors.
"""

from typing import Dict, Union
from Load import Load

class LoadFactor:
    """
    This class is a helper class that combines a ``Load`` with factors for the
    final combination.
    """

    def __init__(self, *, load: Load,
                 base_factor: float = 1.0,
                 scale_factor: float = 1.0,
                 rotational_factor: float = 1.0,
                 symmetry_factor: float = 1.0,
                 group_factor: float = 1.0,
                 info: Dict[str, Union[str, float, bool]] = None):
        """
        Constructor for the ``LoadFactor`` object.

        :param base_factor: The base factor to apply to the load
        :param scale_factor: The ``scale_factor`` that adjusts the load for
            scaling effects (such as scaling a 2.5kPa load case to 5kPa).
        :param rotational_factor: The rotational load factor to be applied. This
            is the factor that is applied based on a required angle in a
            ``RotationalGroup``.
        :param symmetry_factor: The symmetry factor based on the required angle
            in a ``RotationalGroup`` - either 1.0 or -1.0.
        :param group_factor: The group combination factor applied to the
            ``LoadGroup`` in the ``LoadCase`` object.
        :param info: Additional information to be stored with the load factor.
            This should be a dictionary of the form {str: str}.
        """

        self.load = load
        self._factors = {}
        self.base_factor = base_factor
        self.scale_factor = scale_factor
        self.rotational_factor = rotational_factor
        self.symmetry_factor = symmetry_factor
        self.group_factor = group_factor
        self.info = info

    @property
    def load(self):
        """
        Getter for the ``load`` property
        :return: The ``Load`` object associated with the factor.
        """

        return self._load

    @load.setter
    def load(self, load: Load):
        """
        Setter for the ``load`` property
        :param load: The ``Load`` to associate with the factors
        """

        self._load = load

    @property
    def base_factor(self) -> float:
        """
        The base_factor is the base load factor.

        Scale & rotation factors will be applied separately.

        :return: Returns the ``base_factor``.
        """
        return self._factors['base_factor']

    @base_factor.setter
    def base_factor(self, base_factor: float = 1.0):
        """
        Sets the ``base_factor``. This is the basic load factor applied to the
        ``load`` object. Other factors such as Scale or Rotational factors will
        be applied separately.

        :param base_factor: The ``base_factor`` to apply to the ``Load``.
        """

        self._factors['base_factor'] = base_factor

    @property
    def scale_factor(self) -> float:
        """
        Gets the ``scale_factor`` for the ``Load``. This is the factor that
        adjusts the load for scaling effects (such as scaling a 2.5kPa load case
        to 5kPa).

        :return: Returns the ``scale_factor``
        """

        return self._factors['scale_factor']

    @scale_factor.setter
    def scale_factor(self, scale_factor: float = 1.0):
        """
        Sets the ``scale_factor`` for the ``Load``. This is the factor that
        adjusts the load for scaling effects (such as scaling a 2.5kPa load case
        to 5kPa).

        :param scale_factor: The ``scale_factor`` that adjusts the load for
            scaling effects (such as scaling a 2.5kPa load case to 5kPa).
        """

        self._factors['scale_factor'] = scale_factor

    @property
    def rotational_factor(self) -> float:
        """
        Gets the rotational factor applied to the load. This is the factor that
        is applied based on a required angle in a ``RotationalGroup``.

        :return: Returns the rotational factor applied
        """

        return self._factors['rot_factor']

    @rotational_factor.setter
    def rotational_factor(self, rotational_factor: float = 1.0):
        """
        Sets the rotational factor applied to the load. This is the factor that
        is applied based on a required angle in a ``RotationalGroup``.

        :param rotational_factor: The rotational load factor to be applied. This
            is the factor that is applied based on a required angle in a
            ``RotationalGroup``.
        """

        self._factors['rot_factor'] = rotational_factor

    @property
    def symmetry_factor(self) -> float:
        """
        Sets the symmetry factor applied to the load. This is the factor that
        is applied based on a required angle in a ``RotationalGroup``.

        This value is either 1.0 or -1.0.

        :return: Returns the symmetry factor that builds up the load factor.
        """

        return self._factors['sym_factor']

    @symmetry_factor.setter
    def symmetry_factor(self, symmetry_factor: float = 1.0):
        """
        Gets the symmetry factor applied to the load. This is the factor that
        is applied based on a required angle in a ``RotationalGroup``.

        This value is either 1.0 or -1.0.

        :param symmetry_factor: The symmetry factor based on the required angle
            in a ``RotationalGroup`` - either 1.0 or -1.0.
        """

        if symmetry_factor not in [-1.0, 1.0]:
            raise ValueError(f'Expected symmetry factor to be -1.0 or 1.0, '
                             + f'actual value: {symmetry_factor}')

        self._factors['sym_factor'] = symmetry_factor

    @property
    def group_factor(self) -> float:
        """
        Gets the group_factor property, applied from the group combination
        factor.
        :return: Returns the group combination factor.
        """

        return self._factors['group_factor']

    @group_factor.setter
    def group_factor(self, group_factor: float = 1.0):
        """
        Sets the group_factor property, applied from the group combination
        factor.

        :param group_factor: The group combination factor.
        """

        self._factors['group_factor'] = group_factor

    @property
    def factor(self) -> float:
        """
        Returns the final load factor to apply to the ``Load``.

        :return: The final load factor incorporating all applied factors.
        """

        f = 1.0

        for k, v in self._factors.items():
            f *= v

        return f


    @property
    def info(self) -> Dict[str, Union[str, float, bool]]:
        """
        Gets the dictionary containing additional information.

        :return: A dictionary containing additional information.
        """

        return self._info

    @info.setter
    def info(self, info: Dict[str, Union[str, float, bool]]):
        """
        Sets the dictionary containing additional information.

        :param info: A dictionary containing the additional information.
        """

        self._info = {}

        if info != None:
               for k, v in info.items():
                    self.add_info(key = k, value = v)

    def add_info(self, *, key: str, value: Union[str, float, bool]):
        """
        Adds information into the ``self.info`` dictionary.

        Done separately to allow for a list of allowable keys.

        :param key: The key for the additional information dictionary.
        :param value: The value to store.
        """

        all_keys = ['scale_to', 'is_scaled', 'angle', 'symmetric']

        if key not in all_keys:
            raise ValueError(f'Key {key} is invalid. Additional information '
                             + f'keys should be in the following list: '
                             + f'{all_keys}')

        self._info[key] = value

    def factor_title(self, *, abbreviate: bool = True,
                     times_sign: str = '×',
                     precision: int = 3,
                     no_type: str = 'f',
                     abs_factor: bool = False,
                     factor_override: float = None):
        """
        Generates a short title for the LoadFactor, intended to be used by the
        Combination class to generate the combination title.

        :param abbreviate: Use the abbreviation for the load, or the full load
            name?
        :param times_sign: The multiplication sign used between the factor and
            the name / abbreviation.
        :param precision: The no. of decimals to use to format the factor.
        :param no_type: The number format type. Corresponds to the format code
            in the standard Python string formatting. Only 'f', 'g' and 'e' are
            accepted.
        :param abs_factor: Use the absolute factor, or use a signed version of
            the factor.
        :param factor_override: Override the self.factor with a different
            value. Use None to continue using self.factor.
        :return: Returns a description of the LoadFactor for use in the
            Combination.combination_title method.
        """

        no_type_allowed = ['f', 'g', 'e']

        if no_type.lower() not in no_type_allowed:
            raise ValueError(f'Parameter no_type should be in the list: '
                             + f'{no_type_allowed}. Value entered was: '
                             +  f'{no_type}.')

        factor_format = '{:-0.' + str(precision) + no_type + '}'

        if factor_override != None:
            factor = factor_override
        else:
            factor = self.factor

        if abs_factor:
            case_factor = factor_format.format(abs(factor))
        else:
            case_factor = factor_format.format(factor)

        if abbreviate:
            case_title = self.load.abbrev
        else:
            case_title = self.load.load_name

        return case_factor + times_sign + case_title

    def __str__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.

        return (f'{type(self).__name__}: '
                + f'load: ({str(self.load)}), '
                + f'factor: {str(self.factor)}'
                )

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadCase without change.

        return (f'{type(self).__name__}('
                + f'load = {repr(self.load)}, '
                + f'base_factor = {repr(self.base_factor)}, '
                + f'scale_factor = {repr(self.scale_factor)}, '
                + f'rotational_factor = {repr(self.rotational_factor)}, '
                + f'symmetry_factor = {repr(self.symmetry_factor)}, '
                + f'group_factor = {repr(self.group_factor)}, '
                + f'info = {repr(self.info)}'
                + ')')

    def __eq__(self, other):
        """
        Override the equality test.
        """

        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__

        return NotImplemented

    def __ne__(self, other):
        """
        Override the non-equality test.
        """

        if isinstance(other, self.__class__):
            return not self.__eq__(other)

        return NotImplemented