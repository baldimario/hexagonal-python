"""
Module for example response.
"""

from dataclasses import dataclass
from core.cqrs.query.query import QueryResponseInterface


@dataclass(frozen=True, kw_only=True)
class ExampleResponse(QueryResponseInterface):
    """
    Represents the example query response.
    """

    result: str
