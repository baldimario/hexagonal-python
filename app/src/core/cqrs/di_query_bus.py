"""
Module for Dependency Injection Query Bus.
"""

from typing import Type, Union
from core.di import Container
from .query import QueryInterface, QueryResponseInterface
from .query_bus import QueryBusInterface
from .types import QueryHandlerType
from .query_handler import QueryHandlerInterface
from .exceptions import QueryAlreadyRegistered, HandlerNotFound


class DIQueryBus(QueryBusInterface):
    """
    A query bus implementation that utilizes a dependency injection container.
    """

    def __init__(self, container: Container) -> None:
        self._container = container

    def register_handler(
        self, cq: Type[QueryInterface], handler: QueryHandlerType
    ) -> None:
        if not issubclass(handler.__class__, QueryHandlerInterface):
            raise ValueError("Handler must be a subclass of Handler[TQuery]")

        if cq in self._container:
            raise QueryAlreadyRegistered.for_query(cq.__name__)

        self._container[cq] = handler

    def execute(self, cq: QueryInterface) -> Union[None, QueryResponseInterface]:
        if type(cq) not in self._container:
            raise HandlerNotFound.for_query(cq)

        handler = self._container[type(cq)]
        return handler(cq)  # pyright: ignore
