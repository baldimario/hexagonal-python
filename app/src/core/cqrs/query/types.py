"""
Module containing types for CQRS (Command Query Responsibility Segregation) pattern.
"""

from typing import Any, Callable, Union

from .query import QueryInterface, QueryResponseInterface
from .query_handler import QueryHandlerInterface

QueryHandlerType = Union[
    Callable[[Any], None], QueryHandlerInterface[QueryInterface, QueryResponseInterface]
]
