"""
Module for handling simple command bus operations.
"""

from typing import Dict, Type, Union
from .query import QueryInterface, QueryResponseInterface
from .query_bus import QueryBusInterface
from .types import QueryHandlerType
from .exceptions import QueryAlreadyRegistered, HandlerNotFound


class SimpleQueryBus(QueryBusInterface):
    """
    A simple implementation of the Query Bus pattern.

    Attributes:
        _handlers (Dict[Type[QueryInterface], QueryInterface]):
        A dictionary of query handlers.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[QueryInterface], QueryHandlerType] = {}

    def register_handler(
        self, cq: Type[QueryInterface], handler: QueryHandlerType
    ) -> None:
        if cq in self._handlers:
            raise QueryAlreadyRegistered.for_query(cq.__name__)

        self._handlers[cq] = handler

    def execute(self, cq: QueryInterface) -> Union[None, QueryResponseInterface]:
        if type(cq) not in self._handlers:
            raise HandlerNotFound.for_query(cq)

        handler = self._handlers[type(cq)]
        return handler(cq)
