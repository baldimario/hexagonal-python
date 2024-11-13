"""
Module for example query.
"""

from dataclasses import dataclass
from core.cqrs.query.query import QueryInterface


@dataclass(frozen=True, kw_only=True)
class ExampleQuery(QueryInterface):
    """
    Represents an example query with two parameters.

    Attributes:
        parameter_one (str): The first parameter of the command.
        parameter_two (str): The second parameter of the command.
    """

    parameter_one: str
    parameter_two: str
