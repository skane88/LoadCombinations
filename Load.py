# coding=utf-8

"""
This file creates a "Load" class, that will be used to generate a list of load
combinations.

More complex loads may be implemented later if required.
"""


class Load:
    """
    Creates a basic "Load" class, which will be inherited for more complex load
    classes, but will be acceptable for simple load cases.
    """

    def __init__(self, *, load: str, load_no, abbrev: str = ''):
        """
        Create a Load object.mro

        :param load: The name of the load case.
        :param load_no: The load case no.
        :param abbrev: an abbreviation for the load case.
        """

        self.load = load
        self.load_no = load_no
        self.abbrev = abbrev

    @property
    def load(self) -> str:
        """
        The name of the load case.
        """

        return self._load

    @load.setter
    def load(self, load: str):
        """
        The name of the load case.

        :param load: the name of the load case.
        """

        self._load = load

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
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):
        # Using {type(self).__name} to allow this method to be inherited by
        # sub-classes without having to override it unless additional properties
        # have to go into this method.
        return f'{type(self).__name__}: {self.load}, load no: {self.load_no}'

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
    def __init__(self, *, load: str, load_no, load_value: float,
                 abbrev: str = ''):
        """
        Constructor for a ScalableLoad object.

        :param load: The name of the load case.
        :param load_no: The load case no.
        :param load_value: The value of the load that is input into the
            structural model. I.e. if the load case is based off 10t, then
            load_value should be 10.
        :param abbrev: an abbreviation for the load case.
        """
        super().__init__(load = load, load_no = load_no, abbrev = abbrev)

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

    def scale_factor(self, *, scale_to: float, scale: bool = True) -> float:
        """
        Determines the scale factor required to scale the load to a given value.
        I.e. if the load in the model is 10t, and the scale_to load is 5t, this
        method will return 0.5.

        :param scale_to: The load to scale to.
        :param scale: Should the load be scaled? If False returns 1.0. By
            default this is True.
        :return: Returns a float which is the factor which will scale this load
            to the scale_to load.
        """

        scale_factor = 1.0  # default value

        if scale:
            # if the load needs to scale
            scale_factor = scale_to / self.load_value

        return scale_factor

    def __repr__(self):
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"load_value={repr(self.load_value)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):
        return (super(ScalableLoad, self).__str__()
                + f', load value: {self.load_value}')


class RotatableLoad(ScalableLoad):
    def __init__(self, *, load: str, load_no, load_value: float, angle: float,
                 symmetrical: bool, abbrev: str = ''):
        """
        Constructor for a RotatableLoad object.

        :param load: The name of the load case.
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

        super().__init__(load = load, load_no = load_no,
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
        return (f'{type(self).__name__}(load={repr(self.load)}, '
                + f'load_no={repr(self.load_no)}, '
                + f'load_value={repr(self.load_value)}, '
                + f'angle={repr(self.angle)}, '
                + f'symmetrical={repr(self.symmetrical)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):
        return (super(RotatableLoad, self).__str__()
                + f', angle: {self.angle}')


class WindLoad(Load):
    """
    This class is simply a wrapper around a RotatableLoad object, to allow
    the use of wind_speed instead of load, and to hide the scale_factor
    method. If access to the underlying RotatableLoad object is required,
    use self._rotatableload to access it.

    Note that this approach requires overriding the load, load_no and abbrev
    setters inherited from the Load class, to ensure tha the underlying
    RotatableLoad object maintains its current state. This means accepting a
    limited amount of duplicated code. This does however mean that the
    WindLoad is still a sub-class of Load, which is desired behaviour.
    """

    def __init__(self, *, load: str, load_no, wind_speed: float, angle: float,
                 symmetrical: bool, abbrev: str = ''):
        """
        Constructor for the WindLoad class.

        :param load: The name of the load case.
        :param load_no: The load case no.
        :param wind_speed: The wind speed that the load case in the model is
            based on.
        :param angle: The angle that the load in the model is applied at, in
            degrees. Angles that are >360 or <0 will be converted into the range
            0-360 degrees by taking their modulus with 360.
        :param symmetrical: Is the applied  load symmetrical? I.e. if the load
            were to rotate through 180 degrees can the load factor simply change
            from +1 to -1?
        :param abbrev: An abbreviation for the load case.
        """

        self._rotatableload = RotatableLoad(load = load, load_no = load_no,
                                            load_value = wind_speed,
                                            angle = angle,
                                            symmetrical = symmetrical,
                                            abbrev = abbrev)

        super().__init__(load = load, load_no = load_no, abbrev = abbrev)

    @Load.load.setter
    def load(self, load: str):
        """
        The name of the load case.

        :param load: the name of the load case.
        """

        self._load = load
        self._rotatableload.load = load

    @Load.load_no.setter
    def load_no(self, load_no):
        """
        Setter for the load case no.

        :param load_no: The load case no.
        """

        self._load_no = load_no
        self._rotatableload.load_no = load_no

    @Load.abbrev.setter
    def abbrev(self, abbrev: str):
        """
        An abbreviation for the load case

        :param abbrev: an abbreviation for the load case.
        """

        self._abbrev = abbrev
        self._rotatableload.abbrev = abbrev

    @property
    def wind_speed(self) -> float:
        """
        The wind speed that the load case is based on.

        :return: The wind speed the load case is based on.
        """

        return self._rotatableload.load_value

    @wind_speed.setter
    def wind_speed(self, wind_speed: float):
        """
        The wind speed that the load case is based on.

        :param wind_speed: The wind speed that the load case in the model is
            based on.
        """

        self._rotatableload.load_value = wind_speed

    @property
    def angle(self) -> float:
        """
        The angle that the load in the model is applied at.

        :return: Returns the load angle in degrees, between 0 and 360.
        """

        return self._rotatableload.angle

    @angle.setter
    def angle(self, angle: float):
        """
        The angle that the load in the model is applied at.

        :param angle: The angle that the load in the model is applied at, in
            degrees. Angles that are >360 or <0 will be converted into the range
            0-360 degrees by taking their modulus with 360.
        """

        self._rotatableload.angle = angle

    @property
    def symmetrical(self) -> bool:
        """
        Is the applied  load symmetrical? I.e. if the load were to rotate
        through 180 degrees can the load factor simply change from +1 to -1?

        :return: a boolean indicating if the load is symmetrical or not.
        """

        return self._rotatableload.symmetrical

    @symmetrical.setter
    def symmetrical(self, symmetrical: bool):
        """
        Is the applied  load symmetrical? I.e. if the load were to rotate
        through 180 degrees can the load factor simply change from +1 to -1?

        :param symmetrical: Is the applied  load symmetrical? I.e. if the load
            were to rotate through 180 degrees can the load factor simply change
            from +1 to -1?
        """

        self._rotatableload.symmetrical = symmetrical

    def scale_speed(self, *, wind_speed_to: float, scale: bool = True) -> float:
        """
        Determines the scale factor required to scale the load to a given value.
        Note that wind load scales to the square of the wind speed.
        I.e. if the load in the model is based on a 69m/s wind speed, and the
        wind speed to scale to is 25m/s, this method will return
        25^2 / 69^2 = 0.131.

        :param wind_speed_to: The wind speed to scale the load to.
        :param scale: Should the load be scaled? If False returns 1.0. By
            default this is True.
        :return: Returns a float which is the factor which will scale this load
            to the wind_speed_to.
        """

        scale_speed = 1.0  # default value

        if scale:
            # if the load needs to be scaled
            scale_speed = ((wind_speed_to * wind_speed_to) /
                           (self.wind_speed * self.wind_speed))

        return scale_speed

    def __repr__(self):
        return (f'{type(self).__name__}(load={repr(self.load)}, '
                + f'load_no={repr(self.load_no)}, '
                + f'wind_speed={repr(self.wind_speed)}, '
                + f'angle={repr(self.angle)}, '
                + f'symmetrical={repr(self.symmetrical)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):
        return (super(WindLoad, self).__str__()
                + f', wind_speed: {self.wind_speed}'
                + f', angle: {self.angle}')
