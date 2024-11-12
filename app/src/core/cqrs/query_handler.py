"""Module containing base interfaces for query handlers."""

from typing import Union, TypeVar
from .handler import HandlerInterface
from .query import QueryInterface, QueryResponseInterface

T = TypeVar("T", bound=QueryInterface)  # pylint: disable=invalid-name
R = TypeVar("R", bound=QueryResponseInterface)  # pylint: disable=invalid-name


class QueryHandlerInterface(
    HandlerInterface[T, R]
):  # pylint: disable=too-few-public-methods
    """Base interface for query handlers."""

    # it should be async
    def __call__(self, query: T) -> Union[None, R]:
        """Handles a query."""
