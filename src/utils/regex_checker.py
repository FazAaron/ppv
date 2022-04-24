"""
This module makes RegexChecker objects available for use when imported
"""
from re import search


class RegexChecker:
    """
    An interface to interact with the built-in re module, only using required
    methods
    """

    def matches(regex_pattern: str, to_match: str) -> bool:
        """
        Checks whether the pattern is equal to the given string or not

        Parameters:
        regex_pattern (str): The pattern to match
        to_match      (str): The data to match against
        """
        found = search(f"{regex_pattern}", to_match)
        return found is not None