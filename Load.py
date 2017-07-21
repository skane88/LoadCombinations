
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

    def __init__(self, *, load, load_no, abbrev=''):
        """
        Create a Load object.mro

        :param load: The name of the load case.
        :param abbrev: an abbreviation for the load case.
        """

        self.load = load
        self.load_no = load_no
        self.abbrev = abbrev

    @property
    def load(self):
        """
        The name of the load case.
        """

        return self._load

    @load.setter
    def load(self, load):
        """
        The name of the load case.

        :param load: the name of the load case.
        """

        self._load = load

    @property
    def load_no(self):
        return self._load_no

    @load_no.setter
    def load_no(self, load_no):
        self._load_no = load_no

    @property
    def abbrev(self):
        """
        An abbreviation for the load case
        """

        return self._abbrev

    @abbrev.setter
    def abbrev(self, abbrev):
        """
        An abbreviation for the load case

        :param abbrev: an abbreviation for the load case.
        """
        self._abbrev = abbrev

    def __repr__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return f'{type(self).__name__}: {self.load}, no. {self.load_no}'


#now create subclasses of more specialised loads

class ScalableLoad(Load):

    def __init__(self, *, load, load_no, load_value, abbrev = ''):
        super().__init__(load = load, load_no = load_no, abbrev = abbrev)

        self.load_value = load_value

    @property
    def load_value(self):
        return self._load_value

    @load_value.setter
    def load_value(self, load_value):
        self._load_value = load_value

    def scale_factor(self, *, scale_to, scale: bool = True) -> float:
        '''
        Determines the scale factor required to scale the load to a given value.

        :param scale_to: The load to scale to.
        :param scale: Should the load be scaled? If False returns 1.0. By
            default this is True.
        :return: Returns a float which is the factor which will scale this load
            to the scale_to load.
        '''

        scale_factor = 1.0 #default value

        if scale:
            #if the load needs to scale
            scale_factor = scale_to / self.load_value

        return scale_factor

    def __repr__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"load_value={repr(self.load_value)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f'{type(self).__name__}: {self.load}, no. {self.load_no}, '
                + f'load value: {self.load_value}')


class RotatableLoad(ScalableLoad):

    def __init__(self, *, load, load_no, load_value, angle, abbrev = ''):
        super().__init__(load = load, load_no = load_no,
                         load_value = load_value, abbrev = abbrev)
        self.angle = angle

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):

        self._angle = angle % 360.0

    def __repr__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"load_value={repr(self.load_value)}, "
                + f"angle={repr(self.angle)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f'{type(self).__name__}: {self.load}, no. {self.load_no}, '
                + f'load value: {self.load_value}, initial angle: {self.angle}')


class WindLoad(Load):

    def __init__(self, *, load, load_no, wind_speed, angle, abbrev = ''):
        super().__init__(load = load, load_no = load_no, abbrev = abbrev)
        self.wind_speed = wind_speed
        self.angle = angle

    @property
    def wind_speed(self):
        return self._wind_speed

    @wind_speed.setter
    def wind_speed(self, wind_speed):
        self._wind_speed = wind_speed

    @property
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, angle):

        self._angle = angle % 360.0

    def scale_speed(self, *, wind_speed_to, scale: bool = True) -> float:

        scale_speed = 1.0 # default value

        if scale:
            #if the load needs to be scaled
            scale_speed = ((wind_speed_to * wind_speed_to) /
                            (self.wind_speed * self.wind_speed))

        return scale_speed

    def __repr__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f"{type(self).__name__}(load={repr(self.load)}, "
                + f"load_no={repr(self.load_no)}, "
                + f"wind_speed = {repr(self.wind_speed)}, "
                + f"angle = {repr(self.angle)}, "
                + f"abbrev={repr(self.abbrev)})")

    def __str__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return (f'{type(self).__name__}: {self.load}, '
                + f'no. {self.load_no}, wind_speed: {self.wind_speed}')
