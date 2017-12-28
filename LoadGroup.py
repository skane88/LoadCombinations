# coding=utf-8

"""
Creates a LoadGroup class, that stores multiple Loads and can generate an
appropriate list of loads through an iterator method.
"""

from typing import Dict, List, Tuple, Union, Callable
from collections import namedtuple
from Load import Load, ScalableLoad, RotatableLoad
from HelperFuncs import sine_interp_90, wind_interp_85, req_angles_list
from exceptions import LoadExistsException, LoadNotPresentException
from exceptions import AngleExistsException
from LoadFactor import LoadFactor

# define a named tuple for returning results.

class LoadGroup:
    """
    This class stores collections of Load objects in groups and determines the
    appropriate return cases.

    This is the base class, and will be inherited by other sorts of load groups.

    This class simply returns all loads in its self.loads method in a single
    valued iterator, with load factors of 1.0.
    """

    def __init__(self, *, group_name: str,
                 loads: Union[Dict[int, Load], List[Load], Load],
                 abbrev: str = ''):
        """
        Creates a LoadGroup object.mro

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param abbrev: An abbreviation for the load group.
        """

        self.group_name = group_name

        self.loads = loads

        self.abbrev = abbrev



    @property
    def group_name(self) -> str:
        """
        The name of the load group.
        """

        return self._group_name


    @group_name.setter
    def group_name(self, group_name: str):
        """
        The name of the load group.

        :param group_name: the name of the load group.
        """

        self._group_name = group_name


    @property
    def loads(self) -> Dict[int, Load]:
        """
        The loads included in the load group. Note that when set via the
        setter this completely overwrites the loads dictionary. If a single load
        is meant to be added use the add_load method instead.
        """

        return self._loads


    @loads.setter
    def loads(self, loads: Union[Dict[int, Load], List[Load], Load]):
        """
        The loads included in the load group. Note that when set via the
        setter this completely overwrites the loads dictionary. If a single load
        is meant to be added use the add_load method instead.

        :param loads: A ``Dict[int, Load]`, ``List[Load]`` or a ``Load`` object
            to make up the LoadGroup loads.
        """

        self._loads = {}

        self.add_load(loads) # for simplicity, call add_load which is written
                             # to handle adding multiple loads at once etc.


    def add_load(self, load: Union[Dict[int, Load], List[Load], Load]):
        """
        A method to add loads into the self.loads that make up the group,
        without having to overwrite the entire self.loads dictionary.

        :param load: The load to add. Can be a single ``Load`` object, a
            ``Dict[int, Load]`` or a ``List[Load]``.
        """

        if isinstance(load, Dict):

            # iterate through all the dictionary items and add_load
            for k in load:
                self.add_load(load[k])

        elif isinstance(load, List):
            # if the load is a List then iterate through the List and add all
            # loads.

            for l in load:
                self.add_load(l)

        else:
            #first check if the load exists in the self._loads dictionary

            if self.load_exists(load = load) == False:
                self._loads[load.load_no] = load
            else:
                raise LoadExistsException(f'Attempted to add a load to the '
                                          + f'LoadGroup that already exists. '
                                          + f'Load: {str(load)}, '
                                          + f'self.loads: {str(self._loads)}.')


    def del_load(self, *, load_no: int = None, load_name: str = None,
                 abbrev: str = None, load: Load = None):
        """
        A method to delete a single load from the self.loads property.

        The load to delete can be specified by either the ``load_no``,
        ``load_name`` or ``abbrev`` properties of the ``Load``, or a ``Load``
        object can be passed in directly. It should be noted that if
        more than one parameter is given the search will only be carried out
        based on the first provided parameter - providing multiple parameters
        does not result in a search by multiple parameters.

        This method does not curently return information on the status of the
        deletion operation. If it is necessary to know if the deletion was
        successful or not the user should ensure they check for it directly.

        :param load_no: The load_no of the load to delete.
        :param load_name: The load_name of the load to delete.
        :param abbrev:  The abbrev of the load to delete.
        :param load: A ``Load`` object to check for.
        """

        load_present = self.load_exists(load_no = load_no,
                                        load_name = load_name,
                                        abbrev = abbrev,
                                        load = load)

        if load_present != False:

            self._loads.pop(load_present)

        else:
            raise LoadNotPresentException(f'To delete a Load a Load needs to be'
                             + f'present. Load not present.')


    def load_exists(self, *, load_no: int = None, load_name: str = None,
                    abbrev: str = None, load: Load = None) -> Union[bool, int]:
        """
        This method searches the self.loads property of the ``LoadGroup`` to
        determine if a ``Load`` exists in it. It will search by either the
        ``load_no``, ``load_name`` or ``abbrev`` properties of the ``Load``, or
        can search using a given ``Load`` object. It should be noted that if
        more than one parameter is given the search will only be carried out
        based on the first provided parameter - providing multiple parameters
        does not result in a search by multiple parameters.

        :param load_no: The ``load_no`` of the load to check.
        :param load_name: The ``load_name`` of the load to check.
        :param abbrev: The ``abbrev`` of the load to check.
        :param load: A ``Load`` object to look for.
        :return: Returns the ``load_no`` of the load if the load is found,
            ``False`` otherwise.
        """

        # can shortcut this method if the self._loads method is empty.
        if len(self._loads) == 0:
            # by default the load cannot exist in an empty dictionary.
            return False

        if load_no != None:
            # if provided the load no. the search is via the key of the
            # self._load dictionary

            if load_no in self._loads:
                return load_no
            else:
                return False

        elif load_name != None:
            # if provided with the load name, the search needs to go through all
            # the items in the dictionary

            for k, l in self._loads.items():

                if load_name == l.load_name:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        elif abbrev != None:
            # similar with abbrev, the search needs to go through all the items
            # in the dictionary

            for k, l in self._loads.items():
                if abbrev == l.abbrev:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        elif load != None:
            # if provided a load we have to search through all the items in the
            # self._loads dictionary to check for it.

            for k, l in self._loads.items():

                # to avoid silently closing this method if loads share the same
                # load_no we need to return the load_no if either of the
                # following are true:
                # the load_no is the same as an existing load_no OR
                # the load is == to an existing load.

                if load.load_no == k or load == l:
                    return k

            # if haven't found in the dictionary, return False.
            return False

        else:
            raise ValueError(f'To check if a Load exists a Load needs to be'
                             + f'provided. No load information provided.')


    @property
    def abbrev(self) -> str:
        """
        An abbreviation for the LoadGroup.

        :return: Returns the abbreviation.
        """

        return self._abbrev

    @abbrev.setter
    def abbrev(self, abbrev: str):
        """
        An abbreviation for the LoadGroup.

        :param abbrev: An abbreviation for the load group.
        """

        self._abbrev = abbrev

    def generate_groups(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own named tuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        results = []
        for k, l in self.loads.items():
            lf = LoadFactor(load = l, base_factor = 1.0)
            results.append(lf)

        results = tuple(results)

        yield results

    def __repr__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}('
                + f'group_name = {repr(self.group_name)}, '
                + f'loads = {repr(self.loads)}, '
                + f'abbrev = {repr(self.abbrev)}'
                + ')')

    def __str__(self):
        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return f'{type(self).__name__}: {self.group_name}, loads: {self.loads}'

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


# next define more complex load groups as subclasses.
class FactoredGroup(LoadGroup):
    """
    A subclass of LoadGroup. In a FactoredGroup the loads are treated as a group
    (i.e. all will be returned in the generated result loads, but they can be
    returned with a given list of load factors.
    """

    def __init__(self, *, group_name: str, loads: List[Load],
                 factors: Tuple[float, ...] = (1.0,), abbrev: str = ''):
        """
        Creates a LoadGroup object.

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param factors: the list of load factors.
        :param abbrev: An abbreviation for the load group.
        """

        super().__init__(group_name = group_name, loads = loads,
                         abbrev = abbrev)
        self.factors = factors

    @property
    def factors(self) -> Tuple[float, ...]:
        """
        load_factors contains the list of load factors in the group.

        :return: the list of load factors.
        """

        return self._factors

    @factors.setter
    def factors(self, factors: Tuple[float, ...]):
        """
        load_factors contains the list of load factors in the group.

        :param factors: the list of load factors.
        """
        self._factors = factors

    def generate_groups(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        for f in self.factors:
            # first iterate through the factors, so that all loads in the group
            # have the same factor

            results = []
            for k, l in self.loads.items():
                # then iterate through the load_factors

                lf = LoadFactor(load = l, base_factor = f)
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, factors: {self.factors}')


class ScaledGroup(FactoredGroup):
    """
    A ScaledGroup is a subclass of factored groups and has the following
    properties:

    * A single factor can be applied to all loads.
    * A scaling factor can be applied to scale loads that may be based on
        different real life values (i.e. different floor loads) to a common
        value - for example, scaling all floor loads to 2.5kPa.
    """

    def __init__(self, *, group_name: str, loads: List[ScalableLoad],
                 factors: Tuple[float, ...], scale_to: float,
                 scale: bool = True,
                 abbrev: str = ''):
        """
        A constructor for a ScaledGroup object.

        :param group_name: The name of the load group.
        :param loads: The list of loads.
        :param factors: the list of load factors.
        :param scale_to: The load the group should be scaled to.
        :param scale: Should the group scale. by default this is True.
        :param abbrev: An abbreviation for the load group.
        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, abbrev = abbrev)

        self.scale_to = scale_to
        self.scale = scale

    @property
    def scale_to(self) -> float:
        """
        The value to scale all the loads to.

        :return: The value to which all loads will be scaled to.
        """
        return self._scale_to

    @scale_to.setter
    def scale_to(self, scale_to: float):
        """
        The value to scale all the loads to.

        :param scale_to: The value to which all loads will be scaled to.
        """
        self._scale_to = scale_to

    @property
    def scale(self) -> bool:
        """
        Should the scale factor be used. If False, this is effectively the same
        as the factored load group.

        :return: Is the group scaled?
        """
        return self._scale

    @scale.setter
    def scale(self, scale: bool):
        """
        Should the scale factor be used. If False, this is effectively the same
        as the factored load group.

        :param scale: Should the scale factor be used. If False, this is
            effectively the same as the factored load group.
        """
        self._scale = scale

    def scale_factors(self,
                      scale_func: Callable[[float, float], float] = None)\
            -> Dict[int, float]:
        """
        This function returns a dictionary containing all the scale factors that
        will be applied to the loads in the group.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a dictionary of loads mapped against the scale factor
            that will be applied to them: ``{load_no: scale_factor}``.
        """

        return {k: l.scale_factor(scale_to = self.scale_to,
                                  scale_func = scale_func,
                                  scale = self.scale)
                for k, l in self.loads.items()}

    def generate_groups(self,
                        scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # get the dictionary of scale_factors for the loads. These are
        # independent of the group factors and can therefore be grabbed
        # early using a separate method to simplify this generator.

        scale_factors = self.scale_factors(scale_func)

        # first iterate through the load factors so that all loads have the same
        # factor
        for f in self.factors:

            results = []

            # then iterate through the loads
            for k, l in self.loads.items():
                # Grab the load's scale factor from the dictionary

                scale_factor = scale_factors[k]

                #generate the return load factor object.

                lf = LoadFactor(load = l,
                                base_factor = f,
                                scale_factor = scale_factor,
                                info = {'scale_to':
                                            f'(scaled: {self.scale_to})'})
                results.append(lf)

            results = tuple(results)

            yield results

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_to={repr(self.scale_to)}, '
                + f'scale={repr(self.scale)}, '
                + f'abbrev={repr(self.abbrev)})')

    def __str__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __str__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_to:  {self.scale_to}')


class ExclusiveGroup(ScaledGroup):
    """
    A subclass of ScaledGroup. In an ExclusiveGroup only 1x load case will be
    reported at any time. The only difference from ScaledGroup is the method
    generate_groups returns exclusive results.
    """

    # no need to call __init__ as it shares all the same properties as a scaled
    # group, only calls the generate_groups method differently.

    def generate_groups(self,
                        scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # get the dictionary of scale_factors for the loads. These are
        # independent of the group factors and can therefore be grabbed
        # early using a separate method to simplify this generator.

        scale_factors = self.scale_factors(scale_func)

        # first iterate through the load factors
        for f in self.factors:

            # then iterate through the loads and get a return.
            for k, l in self.loads.items():
                # get the load's scale factor from the dictionary.
                scale_factor = scale_factors[k]

                lf = LoadFactor(load = l,
                                base_factor = f,
                                scale_factor = scale_factor,
                                info = {'scale_to':
                                            f'(scaled: {self.scale_to})'})

                # yield at this level so each load is yielded exclusively.
                yield (lf,)


class RotationalGroup(ScaledGroup):
    """
    A subclass of a ScaledGroup. in a RotationalGroup the loads are scaled by
    load factors but also between each other depending on a specified angle
    at which the interpolation is carried out.
    """

    def __init__(self, *, group_name: str, loads: List[RotatableLoad],
                 factors: Tuple[float, ...], scale_to: float, scale: bool,
                 req_angles: Tuple[float, ...],
                 interp_func: Callable = sine_interp_90,
                 abbrev: str = ''):
        """
        Constructor for a RotationalGroup object.

        :param group_name: The name of the load group.
        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        :param factors: the list of load factors.
        :param scale_to: The load the group should be scaled to.
        :param scale: Should the group scale. by default this is True.
        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        :param abbrev: An abbreviation for the load group.
        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, scale_to = scale_to,
                         scale = scale, abbrev = abbrev)

        self.interp_func = interp_func
        self.req_angles = req_angles

    def add_load(self, load: Union[Dict[int, Load], List[Load], Load]):
        """
        A method to add loads into the self.loads that make up the group,
        without having to overwrite the entire self.loads dictionary.

        :param load: The load to add. Can be a single ``Load`` object, a
            ``Dict[int, Load]`` or a ``List[Load]``.
        """

        if isinstance(load, Dict):

            # iterate through all the dictionary items and add_load
            for k in load:
                self.add_load(load[k])

        elif isinstance(load, List):
            # if the load is a List then iterate through the List and add all
            # loads.

            for l in load:
                self.add_load(l)

        else:
            #first check if the load exists in the self._loads dictionary
            if self.load_exists(load = load) == False:

                # need to check that the angle does not already exist in the
                # self.loads dictionary.
                if not self.check_angle(load.angle):

                    self._loads[load.load_no] = load
                else:

                    raise AngleExistsException(f'Attempted to add a load to the'
                                     + f' RotationalGroup where a load already '
                                     + f'exists at the given angle. Angle is '
                                     + f'{load.angle}, load being added is: '
                                     + f'{load.load_no}.')
            else:
                raise LoadExistsException(f'Attempted to add a load to the '
                                          + f'LoadGroup that already exists. '
                                          + f'Load: {str(load)}, '
                                          + f'self.loads: {str(self._loads)}.')


    def check_angle(self, angle: float) -> bool:
        """
        Checks if a load already exists in the ``self.loads`` dictionary which
        matches the given angle to check.

        :param angle: An angle to check against the list of loads in the
            ``self.loads`` dictionary.
        :return: ``True`` if the angle exists in a load in the ``self.loads``
            dictionary, ``False`` otherwise.
        """

        if angle in self.angles:
            return True
        else:
            return False

    @property
    def angles(self) -> Dict[float, int]:
        """
        Returns a dictionary of all the angles covered by the loads in the
        ``self.loads`` dictionary, and their corresponding loads.

        Does not return angles which are covered by symmetry - refer to the
        ``self.angles_with_symmetry`` property if these are required.

        :return: a dictionary of all the angles covered by the loads in the
            ``self.loads`` dictionary, and their corresponding loads, in the
            format ``{angle: load_no}``.
        """

        return {l.angle: k for k, l in self.loads.items()}

    @property
    def angles_with_symmetry(self) -> Dict[float, Tuple[int, float]]:
        """
        Returns a dictionary of all the angles covered by the loads in the
        ``self.loads`` dictionary, and their corresponding loads. This includes
        angles that are covered by symmetric properties of loads, however
        preference is always given to directly specified angles.

        :return: a dictionary of all the angles covered by the loads in the
            ``self.loads`` dictionary, and their corresponding loads, in the
            format ``{angle: (load_no, symmetry_factor, is_symmetrical)}``.
            Symmetry factor will either be 1.0 or -1.0.
            is_symmetrical will be a boolean, True if the symmetrical load is
            used.
        """

        #first get a dictionary of angles with their initial symmetry factors.

        return_dict = {l.angle: (k, 1.0, False) for k, l in self.loads.items()}

        # next check the special case of 0.0 and 360.0 which are identical
        # but not handled by the wrapping ability of the % function.

        if 0.0 in return_dict and 360.0 not in return_dict:
            return_dict[360.0] = (return_dict[0.0][0], 1.0, False)

        if 360.0 in return_dict and 0.0 not in return_dict:
            return_dict[0.0] = (return_dict[360.0][0], 1.0, False)

        # next go through all load elements again and test for symmetric angles

        for k, l in self.loads.items():

            if l.symmetrical:

                #get the new angle of the load
                new_angle = (l.angle + 180.0) % 360.0

                #if not already in the dictionary add it in.
                if new_angle not in return_dict:
                    return_dict[new_angle] = (k, -1.0, True)

        return return_dict

    @property
    def interp_func(self) -> Callable[[float, float], Tuple[float, float]]:
        """
        Getter for the interpolation function.

        :return: Returns the interpolation function used to determine the load
            factors for intermediate angles between the Load angles.
        """
        return self._interp_func

    @interp_func.setter
    def interp_func(self, interp_func: Callable[[float, float],
                                                Tuple[float, float]]):
        """
        Setter for the interpolation function.

        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        """

        self._interp_func = interp_func

    @property
    def req_angles(self) -> Tuple[float, ...]:
        """
        The getter for the req_angles.

        :return: A tuple containing the angles that the RotationalGroup will
            generate load combinations for.
        """
        return self._req_angles

    @req_angles.setter
    def req_angles(self, req_angles: Union[List[float], Tuple[float, ...]]):
        """
        The setter for the req_angles list.

        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        """

        self._req_angles = req_angles_list(req_angles)

    def nearest_angles(self, angle: float) -> Dict[float, Tuple[int, float]]:
        """
        Get the loads on either side of a given angle.

        i.e. if the loads list contains angles at 0, 90, 180 and 270 degrees
        and ``angle = 45`` is the input parameter to this function the return
        value will be a dictionary:
        ``{0: (load, symmetry factor), 90.0: (load, symmetry factor)}``.

        Where ``angle`` is already in the ``self.loads`` dictionary the return
        dictionary from this function will only contain the matching load.

        :param angle:
        :return: Returns a dictionary
            ``{angle: (load, symmetry factor, is_symmetrical), angle: (load, symmetry factor, is_symmetrical)}``
            Symmetry factor will be either 1.0 or -1.0.
            is_symmetrical will be True if the symmetrical version of a load is
            used.
        """

        #first get the list of angles with their symmetry
        angles = self.angles_with_symmetry

        # first check for the case that angle is already in the list of angles
        # to shortcut some of the logic in this method.

        if angle in angles:
            # simply return the

            return {angle: angles[angle]}

        # else need to check the full range of 360.0 degrees. First get a list
        # of all the angles already in the dictionary.

        angles_list = sorted(angles.keys())

        # Next check for the case where 0 and 360 are not in the dictionary.
        # as it is necessary that we be able to wrap around the full 0-360deg
        # range.

        if 0.0 not in angles:
            # if 0.0 not in the angles dictionary we need to get the highest
            # angle in the list and wrap it a full -360 degrees

            max_angle = max(angles_list)

            angles[max_angle - 360.0] = angles[max_angle]

            # note that changing the symmetry factor is not necessary as we
            # are rotating through 360.0 degrees.

        if 360.0 not in angles:
            # if 360.0 not in the angles dictionary we need to get the lowest
            # angle in the list and wrap it a full 360 degrees

            min_angle = min(angles_list)

            angles[min_angle + 360.0] = angles[min_angle]

            # note that changing the symmetry factor is not necessary as we
            # are rotating through 360.0 degrees.

        #re-calculate the angles list
        angles_list = sorted(angles.keys())

        # get the angle from the list that is smaller & larger than the
        # input parameter angle
        angle_below =  max([x for x in angles_list if x <= angle])
        angle_above = min([x for x in angles_list if x >= angle])

        return {angle_below: angles[angle_below],
                angle_above: angles[angle_above]}

    def generate_groups(self, scale_func: Callable[[float, float], float] = None):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        The load factor will interpolate between loads based on the given
        list of required return angles.

        :param scale_func: A function can be provided to determine the scale
            factor. This should take 2x inputs: scale_to, load_value, and return
            a float as a return value.
        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        # first get the scale factors required.
        scale_factors = self.scale_factors(scale_func)

        # next iterate through the load factors:
        for f in self.factors:

            # next iterate through the angles that loads are required from
            for a in self.req_angles:

                #then get the nearest angles
                nearest = self.nearest_angles(a)

                # if only 1x element in nearest angles then the return value can
                # be determined directly.

                if len(nearest) == 1:

                    # get the load no, the symmetry factor and the scale factor.
                    load_no = nearest[a][0]
                    sym_fact = nearest[a][1]
                    is_sym = nearest[a][2]

                    scale_fact = scale_factors[load_no]

                    #determine an overall load factor
                    load_factor = sym_fact * scale_fact * f

                    #build a LoadFactor object to return
                    lf1 = LoadFactor(load = self.loads[load_no],
                                     base_factor = f,
                                     scale_factor = scale_fact,
                                     symmetry_factor = sym_fact,
                                     rotational_factor = 1.0,
                                     info = {'angle': a,
                                             'symmetric': is_sym})
                    ret_val = (lf1, ) #final return value

                else:
                    # if there are 2 x elements in the nearest angles dictionary
                    # we need to do a bit more processing

                    # get the minimum and maximum angles.
                    a_min = min(nearest.keys())
                    a_max = max(nearest.keys())

                    # get the load nos.
                    load_min = nearest[a_min][0]
                    load_max = nearest[a_max][0]

                    # get the symmetry and scale factors
                    sym_min = nearest[a_min][1]
                    sym_max = nearest[a_max][1]
                    is_sym_min = nearest[a_min][2]
                    is_sym_max = nearest[a_max][2]

                    scale_min = scale_factors[load_min]
                    scale_max = scale_factors[load_max]

                    # get the interpolation between the angles
                    gap = a_max - a_min
                    x = a - a_min

                    factors = self.interp_func(gap, x)

                    # finally build the return load factors

                    lf_min = LoadFactor(load = self.loads[load_min],
                                        base_factor = f,
                                        scale_factor = scale_min,
                                        symmetry_factor =  sym_min,
                                        rotational_factor =  factors.left,
                                        info = {'angle': a,
                                                'symmetric': is_sym_min})

                    lf_max = LoadFactor(load = self.loads[load_max],
                                        base_factor = f,
                                        scale_factor = scale_max,
                                        symmetry_factor =  sym_max,
                                        rotational_factor = factors.right,
                                        info = {'angle': a,
                                                'symmetric': is_sym_max})

                    # build the final return tuple
                    ret_val = (lf_min, lf_max)

                yield ret_val

    def __str__(self):

        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_to:  {self.scale_to}'
                + f'angles: {self.req_angles}')

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_to={repr(self.scale_to)}, '
                + f'scale={repr(self.scale)}, '
                + f'req_angles={repr(self.req_angles)}, '
                + f'interp_func={repr(self.interp_func.__name__)}, '
                + f'abbrev={repr(self.abbrev)})')


class WindGroup(RotationalGroup):
    """
    A subclass of a RotatableGroup. The only differences are that:

    property scale_speed is provided as an alias to scale_to
    The generate_groups function overrides the parent case to provide a
        scale_func that scales the loads based on the wind speed. Wind load
        scales on the square of wind speed and therefore if a load is input
        at 10m/s and is scaled to 20m/s the scale factor returned is
        4.0, whereas a RotationalGroup object will return 2.
    """

    def __init__(self, *, group_name: str, loads: List[RotatableLoad],
                 factors: Tuple[float, ...], scale_speed: float, scale: bool,
                 req_angles: Tuple[float, ...],
                 interp_func: Callable = wind_interp_85,
                 abbrev: str = ''):
        """
        The constructor for a WindGroup object.

        :param group_name: The name of the load group.
        :param loads: The loads that form part of the group. the loads will be
            sorted, and if half_list is True they must all have angles <=180.
        :param factors: the list of load factors.
        :param scale_speed: The wind_speed the load group is scaled to. This is
            simply an alias for the scale_to property of the parent class
            RotatationalGroup.
        :param scale: Should the group scale. by default this is True.
        :param req_angles: The angles that the resulting load combinations are
            required at. Any duplicates are removed, and all angles are
            taken to be in the range of 0-360 degrees by taking the modulus
            of the angle. The list is sorted.
        :param interp_func: A function used to interpolate between Load angles,
            and determine the load factors used. The function should take a
            gap value, corresponding to the angle between 2x adjacent loads,
            and an angle, corresponding to the angle between the left-hand Load
            and the angle at which the load combination is being determined.
            The function should return a named tuple (left, right) where left
            and right are floats which specify the factors to apply to the
            2x angles.
        :param abbrev: An abbreviation for the load group.


        """

        super().__init__(group_name = group_name, loads = loads,
                         factors = factors, scale_to = scale_speed,
                         scale = scale, req_angles = req_angles,
                         interp_func = interp_func,
                         abbrev = abbrev)


    @property
    def scale_speed(self) -> float:
        """
        The wind_speed that the load group is scaled to. This is simply an alias
        for the scale_to property of the parent class RotatationalGroup.

        :return: Returns the wind_speed that the load group is scaled to.
        """

        return self._scale_to

    @scale_speed.setter
    def scale_speed(self, scale_speed: float):
        """
        The wind_speed that the load group is scaled to. This is simply an alias
        for the scale_to property of the parent class RotatationalGroup.

        :param scale_speed: The wind_speed the load group is scaled to. This is
            simply an alias for the scale_to property of the parent class
            RotatationalGroup.
        """

        self._scale_to = scale_speed

    def generate_groups(self):
        """
        Generates an iterator that iterates through the potential cases that
        this group of loads can generate.

        These cases are both multiplied by any load factors and also scaled to
        a common load.

        The load factor will interpolate between loads based on the given
        list of required return angles.

        Note that this overrides the parent function from RotationalGroup to
        provide a scale_func that scales the loads based on the wind speed.
        Wind load scales on the square of wind speed and therefore if a load
        is input at 10m/s and is scaled to 20m/s the scale factor returned is
        4.0, whereas a RotationalGroup object will return 2.0.

        :return: returns a generator which will create a tuple of load factors,
            each of them in their own namedtuple:
            ((load, load_factor, add_info),
            (load, load_factor, add_info), ...)
        """

        def scale_func(scale_to, scale_from):
            return (scale_to ** 2) / (scale_from ** 2)

        return super(WindGroup, self).generate_groups(scale_func)

    def __str__(self):

        return (f'{type(self).__name__}: {self.group_name}, '
                + f'loads: {self.loads}, '
                + f'factors: {self.factors}, '
                + f'scale_speed:  {self.scale_speed}'
                + f'angles: {self.req_angles}')

    def __repr__(self):

        # use the {type(self).__name__} call to get the exact class name. This
        # should allow the __repr__ method to be accepted for subclasses of
        # LoadGroup without change.
        return (f'{type(self).__name__}(group_name={repr(self.group_name)}, '
                + f'loads={repr(self.loads)}, '
                + f'factors={repr(self.factors)}, '
                + f'scale_speed={repr(self.scale_speed)}, '
                + f'scale={repr(self.scale)}, '
                + f'req_angles={repr(self.req_angles)}, '
                + f'interp_func={repr(self.interp_func.__name__)}, '
                + f'abbrev={repr(self.abbrev)})')
