# coding=utf-8

"""
This file is intended to contain factory methods that build Loads, LoadGroups
and LoadCases from other input (i.e. text etc.)
"""

from typing import Union, Dict, List, Tuple, Callable, Any
from enum import IntEnum, unique

from LoadCombination.Load import Load, ScalableLoad, RotatableLoad, WindLoad
from LoadCombination.LoadGroup import (LoadGroup, FactoredGroup, ScaledGroup, ExclusiveGroup,
                                       RotationalGroup, WindGroup)

@unique
class ScaledMode(IntEnum):
    SCALED = 1
    ERROR = 0
    EXCLUSIVE = -1

def BuildLoad(*, load_name: str, load_no: int, abbrev: str = '',
              load_type: Load = None, **kwargs) -> Load:
    """
    Builds a ``Load`` object. The type of Load object can be specified directly
    in the ``load_type`` parameter or else is inferred by the arguments
    provided in ``kwargs``.

    :param load_name: The name of the load case.
    :param load_no: The load case no.
    :param abbrev: an abbreviation for the load case.
    :param load_type: Optionally provide a ``Load`` class object to build, or
        one of the following text strings: 'WindLoad', 'RotatableLoad' or
        'ScalableLoad'
    :param kwargs: Provide the additional arguments required by ``WindLoad``,
        ``RotatableLoad`` and ``ScalableLoad`` as named parameters.
    :return: Returns a ``Load`` object.
    """

    if load_type == WindLoad or 'wind_speed' in kwargs:
        return WindLoad(load_name = load_name, load_no = load_no,
                        abbrev = abbrev, **kwargs)
    elif load_type == RotatableLoad or 'angle' in kwargs:
        return RotatableLoad(load_name = load_name, load_no = load_no,
                             abbrev = abbrev, **kwargs)
    elif load_type == ScalableLoad or 'load_value' in kwargs:
        return ScalableLoad(load_name = load_name, load_no = load_no,
                            abbrev = abbrev, **kwargs)
    else:
        return Load(load_name = load_name, load_no = load_no, abbrev = abbrev)

def LoadFromString(load_string: str) -> Load:
    """
    Returns a ``Load`` object when provided a string. It infers the correct
    type of load based on the provided arguments.

    :param load_string: A string of the following format:

        'load_name: load_name_value, load_no: load_no_value...'

        Each parameter required by the constructor of a ``Load`` object must
        be provided, followed by a colon (:) followed by the actual value,
        separated from the next parameter by a comma (,).
    :return: Returns a ``Load`` object.
    """

    kwargs = _string_parser(load_string)

    # now we have the args, need to convert them to appropriate types

    expected = {'load_name': str,
                'load_no': int,
                'abbrev': str,
                'load_value': float,
                'angle': float,
                'symmetrical': bool,
                'wind_speed': float}

    kwargs =  _dict_typer(kwargs, expected)

    return LoadFromDict(kwargs)

def LoadFromDict(load_dict: Dict[str, Union[str, float, int]]) -> Load:
    """
    Returns a ``Load`` object when provided a dict. It infers the correct
    type of load based on the provided arguments.

    :param load_dict: A dictionary of the following format:

        {load_name: load_name_value, load_no: load_no_value...}

        Each parameter required by the constructor of a ``Load`` object must
        be provided.
    :return: Returns a ``Load`` object.
    """

    kwargs = load_dict

    load_name = kwargs.pop('load_name')
    load_no = kwargs.pop('load_no')
    abbrev = kwargs.pop('abbrev')

    return BuildLoad(load_name = load_name, load_no = load_no, abbrev = abbrev,
                     **kwargs)

def BuildGroup(*, group_name: str,
               loads: Union[Dict[int, Load], List[Load], Load],
               abbrev: str, load_type: LoadGroup = None,
               scaled_mode: int = ScaledMode.ERROR,
               **kwargs) -> LoadGroup:

    if load_type == WindGroup or 'scale_speed' in kwargs:
        return WindGroup(group_name = group_name, loads = loads,
                         abbrev = abbrev, **kwargs)
    elif load_type == RotationalGroup or 'req_angles' in kwargs:
        return RotationalGroup(group_name = group_name, loads = loads,
                               abbrev = abbrev, **kwargs)
    elif load_type == ExclusiveGroup:
        return ExclusiveGroup(group_name = group_name, loads = loads,
                              abbrev = abbrev, **kwargs)
    elif load_type == ScaledGroup:
        return ScaledGroup(group_name = group_name, loads = loads,
                           abbrev = abbrev, **kwargs)
    elif 'scale_to' in kwargs:
        if scaled_mode == ScaledMode.SCALED:
            return ScaledGroup(group_name = group_name, loads = loads,
                               abbrev = abbrev, **kwargs)
        elif scaled_mode == ScaledMode.EXCLUSIVE:
            return ExclusiveGroup(group_name = group_name, loads = loads,
                                  abbrev = abbrev, **kwargs)
        else:
            raise ValueError('Not possible to determine whether a ScaledGroup'
                             + ' or ExclusiveGroup is required with the given'
                             + ' arguments.')
    elif load_type == FactoredGroup or 'factors' in kwargs:
        return FactoredGroup(group_name = group_name, loads = loads,
                             abbrev = abbrev, **kwargs)
    else:
        return LoadGroup(group_name = group_name, loads = loads,
                         abbrev = abbrev)

def GroupFromString(*, group_string: str,
                    loads: Union[Dict[int, Load], List[Load], Load],
                    interp_func: Callable = None,
                    scale_func: Callable[[float, float], float] = None,
                    ) -> LoadGroup:

    kwargs = _string_parser(group_string)

    expected = {'scale': bool,
                'group_factor': float,
                'scale_to': float,
                'scale_speed': float}

    kwargs = _dict_typer(kwargs, expected)

    # now need to set a few special variables differently

    if interp_func != None:
        # the only way I know to make a function that is safe is to have the
        # user provide it direct - otherwise we would have to use something like
        # Eval() which is a security risk. It's not necessary anyway with a
        # default value for 99% of cases.
        kwargs['interp_func'] = interp_func
    else:
        # else we need to delete 'interp_func' from kwargs to ensure that the
        # default value can be used.
        if 'interp_func' in kwargs:
            del(kwargs['interp_func'])

    if scale_func != None:
        kwargs['scale_func'] = scale_func
    else:
        if 'scale_func' in kwargs:
            del(kwargs['scale_func'])

    if 'req_angles' in kwargs:
        kwargs['req_angles'] = _tuple_from_string(in_string = kwargs['req_angles'],
                                                  typer = float)

    if 'factors' in kwargs:
        kwargs['factors'] = _tuple_from_string(in_string = kwargs['factors'],
                                               typer = float)

    # finally, the loads will have been brought in as a list or a tuple of loads
    # to be put into the group. Need to get a tuple of ints, and then use these
    # to build a list of loads.

    load_list = _tuple_from_string(in_string = kwargs['loads'],
                                   typer = int, include_lists = True)

    kwargs['loads'] = _get_loads(load_list = load_list, loads = loads)

    return GroupFromDict(**kwargs)

def GroupFromDict(*,
                  group_dict: Dict[str, Union[str, float, int, bool, Callable, Tuple[float, ...], List[Load]]],
                  scaled_mode: int = ScaledMode.ERROR
                  ) -> LoadGroup:

    kwargs = group_dict

    group_name = kwargs.pop('group_name')
    loads = kwargs.pop('loads')
    abbrev = kwargs.pop('abbrev')

    return BuildGroup(group_name = group_name,
                      loads = loads,
                      abbrev = abbrev,
                      scaled_mode = scaled_mode,
                      **kwargs)

def _string_parser(in_string: str) -> Dict[str, str]:
    """
    Builds a dictionary of arguments for use in the methods which build from
    strings.

    :param in_string: A string of the format 'argument_name: argument, ...'
    :return: Returns a dictionary of arguments based on the input string.
    """

    args = in_string.split(',')

    arg_dict = {}

    for a in args:
        a = a.strip()
        a = a.split(":")

        #add to return dictionary
        arg_dict[a[0].strip()] = a[1].strip()

    return arg_dict

def _dict_typer(in_dict: Dict[Any, Any], expected: Dict[Any, Callable[[Any], Any]]) -> Dict[Any, Any]:
    """
    Used to convert the type of values in a dictionary into other types.

    :param in_dict: The dictionary to convert.
    :param expected: A dictionary of the following format:
        {key - these keys are expected to be in ``in_dict``: value - this is a
        callable that takes one argument and is used to convert the value in the
        original Dict}
    :return: A Dictionary with the same keys as the original, but different
        types in the values, depending on the keys & values present in ``expected``.
    """

    for k, v in expected.items():

        if k in in_dict:

            in_dict[k] = v(in_dict[k])

    return in_dict

def _tuple_from_string(*, in_string: str,
                       typer = Callable[[Any], Any],
                       include_lists: bool = False) -> Tuple[Any, ...]:

    in_string = in_string.strip() # remove whitespace

    parans_string = '()'

    if include_lists:
        parans_string += '[]'

    in_string = in_string.strip(parans_string) # remove parantheses

    in_string = in_string.split(',')

    out_string = []

    for i in in_string:
        i = i.strip()

        out_string = out_string + [typer(i)]

    return tuple(out_string)

def _get_loads(*,
               load_list: Union[Tuple[int,...], List[int]],
               loads: Union[Dict[int, Load], List[Load], Load]) -> List[Load]:

    # if loads is a list or a Load, convert to a Dict:
    if not isinstance(loads, Dict):
        if isinstance(loads, Load):
            loads = [Load]
        load_dict = {}

        for l in loads:

            if l in load_dict:
                raise ValueError(f'Expected only 1x instance of each load.'
                                 + f' Current load: {str(l)}')

            load_dict[l.load_no] = l

        loads = load_dict

    out_list = []

    for i in load_list:

        out_list += loads[i]

    return out_list