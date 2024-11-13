"""
Module for Dependency Injection Query Bus.
"""

from typing import Type, Union
from core.di import Container
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.query.query import QueryInterface, QueryResponseInterface
from core.cqrs.query.query_bus import QueryBusInterface
from core.cqrs.query.types import QueryHandlerType
from core.cqrs.query.query_handler import QueryHandlerInterface
from core.cqrs.exceptions import QueryAlreadyRegistered


class DIQueryBus(QueryBusInterface):
    """
    A query bus implementation that utilizes a dependency injection container.
    """

    def __init__(self, container: Container) -> None:
        self._container = container

    def register_handler(
        self, cq: Type[QueryInterface], handler: QueryHandlerType
    ) -> None:
        """
        Registers a query handler for a given query type.

        Args:
            cq (Type[QueryInterface]): The query type to register the handler for.
            handler (QueryHandlerType): The handler to register.

        Raises:
            ValueError: If the handler is not a subclass of QueryHandlerInterface.
            QueryAlreadyRegistered: If a handler is already registered for the query type.
        """
        if not issubclass(handler.__class__, QueryHandlerInterface):
            raise ValueError("Handler must be a subclass of Handler[TQuery]")

        if cq in self._container:
            raise QueryAlreadyRegistered.for_query(cq.__name__)

        self._container[cq] = handler

    def execute(self, cq: QueryInterface) -> Union[None, QueryResponseInterface]:
        """
        Executes a query and returns the response.

        Args:
            cq (QueryInterface): The query to execute.

        Returns:
            Union[None, QueryResponseInterface]: The query response.

        Raises:
            HandlerNotFound: If no handler is found for the query.
        """
        if type(cq) not in self._container:
            raise HandlerNotFound.for_query(cq)

        handler = self._container[type(cq)]
        return handler(cq)  # pyright: ignore