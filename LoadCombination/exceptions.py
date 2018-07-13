# coding=utf-8

"""
This file defines custom exceptions as required.
"""

class LoadCombinationException(Exception):
    """
    Creates a base excepction for the LoadCombination project, so that all
    custom exceptions can be inherited, allowing other users to catch all
    exceptions from this library in one place.
    """

    pass

class LoadExistsException(LoadCombinationException):
    """
    This exception is raised when a load already exists in a LoadGroup object.
    """

    pass

class LoadNotPresentException(LoadCombinationException):
    """
    This exception is raised when a load does not exist in a LoadGroup object
    but is expected by a method.
    """

    pass

class AngleExistsException(LoadExistsException):
    """
    This exception is raised in a RotationalGroup when a load with the same
    angle already exists in the RotationalGroup.
    """

    pass

class LoadGroupExistsException(LoadCombinationException):
    """
    This exception is raised when a ``LoadGroup`` already exists in a
    ``LoadCase`` object.
    """

    pass

class LoadGroupNotPresentException(LoadCombinationException):
    """
    This exception is raised when a ``LoadGroup`` does not exist in a
    ``LoadCase`` object but is expected by a method.
    """

    pass

class InvalidCombinationFactor(LoadCombinationException):
    """
    This exception is raised when the value passed into a ``LoadCase`` for the
    ``(LoadGroup, combination_factor)`` is not a ``Tuple[LoadGroup, float]``.
    """

    pass