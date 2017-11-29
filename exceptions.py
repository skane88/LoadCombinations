# coding=utf-8

"""
This file defines custom exceptions as required.
"""

class LoadExistsException(Exception):
    """
    This exception is raised when a load already exists in a LoadGroup object.
    """

    pass

class LoadNotPresentException(Exception):
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

class LoadGroupExistsException(Exception):
    """
    This exception is raised when a ``LoadGroup`` already exists in a
    ``LoadCase`` object.
    """

    pass

class LoadGroupNotPresentException(Exception):
    """
    This exception is raised when a ``LoadGroup`` does not exist in a
    ``LoadCase`` object but is expected by a method.
    """

    pass

class InvalidCombinationFactor(Exception):
    """
    This exception is raised when the value passed into a ``LoadCase`` for the
    ``(LoadGroup, combination_factor)`` is not a ``Tuple[LoadGroup, float]``.
    """

    pass