
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

    def __init__(self, load, abbrev = ''):
        """
        Create a Load object.mro

        :param load: The name of the load case.
        :param abbrev: an abbreviation for the load case.
        """

        self.load = load
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
        return f"{type(self).__name__}('{self.load}', '{self.abbrev}')"

    def __str__(self):

        #Using {type(self).__name} to allow this method to be inherited by
        #sub-classes without having to override it unless additional properties
        #have to go into this method.
        return f'{type(self).__name__}: {self.load}'
