"""
Expose public exceptions & warnings
"""


class AdifParserError(ValueError):
    """
    Base class for exceptions in this module
    """


__all__ = ['AdifParserError']
