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