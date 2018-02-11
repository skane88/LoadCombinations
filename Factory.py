# coding=utf-8

"""
This file is intended to contain factory methods that build Loads, LoadGroups
and LoadCases from other input (i.e. text etc.)
"""

from typing import Union, Dict, List, Tuple

from Load import Load, ScalableLoad, RotatableLoad, WindLoad

def BuildLoad(*, load_name: str, load_no: int, abbrev: str = '',
              load_type = None, **kwargs) -> Load:
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
    :return: Returns a Load object.
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

    kwargs = _string_parser(load_string)

    # now we have the args, need to convert them to appropriate types

    expected = {'load_name': str,
                'load_no': int,
                'abbrev': str,
                'load_value': float,
                'angle': float,
                'symmetrical': bool,
                'wind_speed': float}

    for k, v in expected.items():

        if k in kwargs:
            kwargs[k] = v(kwargs[k])

    return LoadFromDict(kwargs)

def LoadFromDict(load_dict: Dict[str, Union[str, float, int]]) -> Load:

    kwargs = load_dict

    load_name = kwargs.pop('load_name')
    load_no = kwargs.pop('load_no')
    abbrev = kwargs.pop('abbrev')

    return BuildLoad(load_name = load_name, load_no = load_no, abbrev = abbrev,
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