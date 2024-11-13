"""
Module for handling query bus operations.
"""

from abc import ABC, abstractmethod
from typing import Type, Union, TypeVar

from core.cqrs.bus import BusInterface
from .query import QueryInterface, QueryResponseInterface
from .query_handler import QueryHandlerInterface

T = TypeVar("T", bound=QueryInterface)  # pylint: disable=invalid-name
H = TypeVar("H", bound=QueryHandlerInterface)  # pylint: disable=invalid-name
R = TypeVar("R", bound=QueryResponseInterface)  # pylint: disable=invalid-name


class QueryBusInterface(BusInterface[T, H, R], ABC):
    """
    Abstract base class for query buses.

    Provides a register_handler method for registering query handlers.
    """

    @abstractmethod
    def register_handler(  # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:
        """
        Registers a handler for a specific query.

        Args:
            query: The type of query to register the handler for.
            handler: The handler to register for the query.
        """

    @abstractmethod
    def execute(  # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed
    ) -> Union[None, R]:  # pyright: ignore
        """
        Execute a query.

        :param query: The query to execute.
        """
