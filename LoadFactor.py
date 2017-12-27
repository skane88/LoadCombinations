# coding=utf-8

"""
This file contains a helper class to associate a ``Load`` with combination
factors.
"""

from typing import Dict
from Load import Load

class LoadFactor:
    """
    This class is a helper class that combines a ``Load`` with factors for the
    final combination.
    """

    def __init__(self):

        self._factors = {}

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

        :param scale_factor: The ``scale_factor``.
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

        :param rotational_factor: The rotational load factor to be applied.
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

        :param symmetry_factor: The symmetry factor - either 1.0 or -1.0.
        """

        if symmetry_factor not in [-1.0, 1.0]:
            raise ValueError(f'Expected symmetry factor to be -1.0 or 1.0, '
                             + f'actual value: {symmetry_factor}')

        self._factors['sym_factor'] = symmetry_factor


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
    def info(self) -> Dict[str, str]:
        """
        Gets the dictionary containing additional information.

        :return: A dictionary containing additional information.
        """

        return self._info

    @info.setter
    def info(self, info: Dict[str, str]):
        """
        Sets the dictionary containing additional information.

        :param info: A dictionary containing the additional information.
        """

        self._info = {}

        for k, v in info.items():
            self.add_info(k, v)

    def add_info(self, key, value):
        """
        Adds information into the ``self.info`` dictionary.

        Done separately to allow for a list of allowable keys.

        :param key: The key for the additional information dictionary.
        :param value: The value to store.
        """

        all_keys = ['scale_to', 'rotate_to', 'symmetric']

        if key not in all_keys:
            raise ValueError(f'Additional information keys should be in the '
                             + f'following list: {all_keys}')

        self._info[key] = value