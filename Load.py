# coding=utf-8

"""
This file creates a "Load" class, that will be used to generate a list of load
combinations.

More complex loads may be implemented later if required.
"""

from typing import Callable

class Load:
    """
    Creates a basic "Load" class, which will be inherited for more complex load
    classes, but will be acceptable for simple load cases.
    """

    def __init__(self, *, load_name: str, load_no, abbrev: str = ''):
        """
        Create a Load object.mro

        :param load_name: The name of the load case.
        :param load_no: The load case no.
        :param abbrev: an abbreviation for the load case.
        """

        self.load_name = load_name
        self.load_no = load_no
        self.abbrev = abbrev

    @property
    def load_name(self) -> str:
        """
        The name of the load case.
        """

        return self._load_name

    @load_name.setter
    def load_name(self, load_name: str):
        """
        The name of the load case.

        :param load_name: the name of the load case.
        """

        self._load_name = load_name

    @property
    def load_no(self):
        """
        The load case no.

        :return: Returns the load case number.
        """

        return self._load_no

    @load_no.setter
    def load_no(self, load_no):
        """
        Setter for the load case no.

        :param load_no: The load case no.
        """

        self._load_no = load_no

    @property
    def abbrev(self) -> str:
        """
        An abbreviation for the load case
        """

        return self._abbrev

    @abbrev.setter
    def abbrev(self, abbrev: str):
        """
        An abbreviation for the load case

        :param abbrev: an abbreviation for the load case.
        """

        self._abbrev = abbrev

    def __repr__(self):
        # Using {type(self).__name} to allow this method to be inherited by
        # sub-classes without having to override it unless additional properties
        # have to go into this method.
        return (f"{type(self).__name__}("
                + f"load_name={repr(self.load_name)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):
        # Using {type(self).__name} to allow this method to be inherited by
        # sub-classes without having to override it unless additional properties
        # have to go into this method.
        return (f'{type(self).__name__}:'
                + f' {self.load_name}, '
                + f'load no: {self.load_no}')

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

# now create subclasses of more specialised loads

class ScalableLoad(Load):
    """
    Scalable loads come with a pre-defined load_value that they can be scaled
    against.

    For example, if the load were entered with a value of 2.5 (kPa for instance)
    but the load combination calls for a value of 5 (kPa) then the ScalableLoad
    will provide an appropriate scale_factor to scale the load up or down.
    """

    def __init__(self, *, load_name: str, load_no, load_value: float,
                 abbrev: str = ''):
        """
        Constructor for a ScalableLoad object.

        :param load_name: The name of the load case.
        :param load_no: The load case no.
        :param load_value: The value of the load that is input into the
            structural model. I.e. if the load case is based off 10t, then
            load_value should be 10.
        :param abbrev: an abbreviation for the load case.
        """
        super().__init__(load_name = load_name, load_no = load_no, abbrev = abbrev)

        self.load_value = load_value

    @property
    def load_value(self) -> float:
        """
        The value of the load that is input into the structural model. I.e. if
        the load case is based off 10t, then load_value should be 10.

        :return: The load value.
        """

        return self._load_value

    @load_value.setter
    def load_value(self, load_value: float):
        """
        The value of the load that is input into the structural model. I.e. if
        the load case is based off 10t, then load_value should be 10.

        :param load_value: The value of the load that is input into the
            structural model. I.e. if the load case is based off 10t, then
            load_value should be 10.
        """

        self._load_value = load_value

    def scale_factor(self, *, scale_to: float,
                     scale_func: Callable[[float, float], float] = None,
                     scale: bool = True) -> float:
        """
        Determines the scale factor required to scale the load to a given value.
        I.e. if the load in the model is 10t, and the scale_to load is 5t, this
        method will return 0.5.

        :param scale_to: The load to scale to.
        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :param scale: Should the load be scaled? If False returns 1.0. By
            default this is True.
        :return: Returns a float which is the factor which will scale this load
            to the scale_to load.
        """

        scale_factor = 1.0  # default value

        if scale:
            #only calculate a scale factor if required.
            if scale_func == None:
                # if the load needs to scale
                scale_factor = scale_to / self.load_value
            else:
                scale_factor = scale_func(scale_to, self.load_value)

        return scale_factor

    def __repr__(self):
        return (f'{type(self).__name__}('
                + f'load_name={repr(self.load_name)}, '
                + f'load_no={repr(self.load_no)}, '
                + f'load_value={repr(self.load_value)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):
        return (super(ScalableLoad, self).__str__()
                + f', load value: {self.load_value}')


class RotatableLoad(ScalableLoad):
    """
    RotatableLoads are scalable loads, but also have an assigned angle to them
    so that they can be scaled as loads are rotated around.
    """

    def __init__(self, *, load_name: str, load_no, load_value: float,
                 angle: float,
                 symmetrical: bool, abbrev: str = ''):
        """
        Constructor for a RotatableLoad object.

        :param load_name: The name of the load case.
        :param load_no: The load case no.
        :param load_value: The value of the load that is input into the
            structural model. I.e. if the load case is based off 10t, then
            load_value should be 10.
        :param angle: The angle that the load in the model is applied at, in
            degrees. Angles that are >360 or <0 will be converted into the range
            0-360 degrees by taking their modulus with 360.
        :param symmetrical: Is the applied  load symmetrical? I.e. if the load
            were to rotate through 180 degrees can the load factor simply change
            from +1 to -1?
        :param abbrev: An abbreviation for the load case.
        """

        super().__init__(load_name = load_name, load_no = load_no,
                         load_value = load_value, abbrev = abbrev)
        self.angle = angle
        self.symmetrical = symmetrical

    @property
    def angle(self) -> float:
        """
        The angle that the load in the model is applied at.

        :return: Returns the load angle in degrees, between 0 and 360.
        """

        return self._angle

    @angle.setter
    def angle(self, angle: float):
        """
        The angle that the load in the model is applied at.

        :param angle: The angle that the load in the model is applied at, in
            degrees. Angles that are >360 or <0 will be converted into the range
            0-360 degrees by taking their modulus with 360.
        """

        self._angle = angle % 360.0

    @property
    def symmetrical(self) -> bool:
        """
        Is the applied  load symmetrical? I.e. if the load were to rotate
        through 180 degrees can the load factor simply change from +1 to -1?

        :return: a boolean indicating if the load is symmetrical or not.
        """

        return self._symmetrical

    @symmetrical.setter
    def symmetrical(self, symmetrical: bool):
        """
        Is the applied  load symmetrical? I.e. if the load were to rotate
        through 180 degrees can the load factor simply change from +1 to -1?

        :param symmetrical: Is the applied  load symmetrical? I.e. if the load
            were to rotate through 180 degrees can the load factor simply change
            from +1 to -1?
        """

        self._symmetrical = symmetrical

    def __repr__(self):
        return (f'{type(self).__name__}('
                + f'load_name={repr(self.load_name)}, '
                + f'load_no={repr(self.load_no)}, '
                + f'load_value={repr(self.load_value)}, '
                + f'angle={repr(self.angle)}, '
                + f'symmetrical={repr(self.symmetrical)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):
        return (super(RotatableLoad, self).__str__()
                + f', angle: {self.angle}')


class WindLoad(RotatableLoad):
    """
    WindLoad is a sub-class of RotatableLoad, however it has an additional
    method to scale the load based on the windspeed, and the load can be entered
    as either load or wind_speed.
    """

    def __init__(self, *, load_name: str, load_no, wind_speed: float,
                 angle: float, symmetrical: bool, abbrev: str = ''):
        """
        Constructor for a WindLoad object.

        :param load_name: The name of the load case.
        :param load_no: The load case no.
        :param wind_speed: The windspeed the load is based on. This is simply an
            alias for the property load_value.
        :param angle: The angle that the load in the model is applied at, in
            degrees. Angles that are >360 or <0 will be converted into the range
            0-360 degrees by taking their modulus with 360.
        :param symmetrical: Is the applied  load symmetrical? I.e. if the load
            were to rotate through 180 degrees can the load factor simply change
            from +1 to -1?
        :param abbrev: An abbreviation for the load case.
        """

        super().__init__(load_name = load_name, load_no = load_no,
                         load_value = wind_speed, angle = angle,
                         symmetrical = symmetrical, abbrev = abbrev)

    @property
    def wind_speed(self) -> float:
        """
        The wind speed the load is based on. This is simply an alias for the
        property load_value.

        :return: The wind speed the load is based on.
        """
        return self._load_value

    @wind_speed.setter
    def wind_speed(self, wind_speed: float):
        """
        The wind speed the load is based on. This is simply an alias for the
        property load_value.

        :param wind_speed: The windspeed the load is based on. This is simply an
            alias for the property load_value.
        """

        self._load_value = wind_speed

    def scale_speed(self, wind_speed_to, scale):
        """
        Determines the scale factor required to scale the load by a given
        windspeed. Wind load scales based on the square of the windspeed.
        Therefore for a wind_load that is based on a 10m/s windspeed, and
        scaling to a windspeed of 20m/s will return a scale factor of 4.0.

        :param wind_speed_to: The wind speed to scale to.
        :param scale: Should the load be scaled? If False returns 1.0. By
            default this is True.
        :return: Returns a float which is the factor which will scale this load
            to the desired wind speed.
        """

        def scale_func(scale_to, scale_from):
            return (scale_to ** 2) / (scale_from ** 2)

        return self.scale_factor(scale_to = wind_speed_to,
                                 scale_func = scale_func,
                                 scale = scale)

    def __repr__(self):
        return (f'{type(self).__name__}('
                + f'load_name={repr(self.load_name)}, '
                + f'load_no={repr(self.load_no)}, '
                + f'wind_speed={repr(self.wind_speed)}, '
                + f'angle={repr(self.angle)}, '
                + f'symmetrical={repr(self.symmetrical)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):
        return (super(WindLoad, self).__str__()
                + f', wind_speed: {self.wind_speed}'
                + f', angle: {self.angle}')
