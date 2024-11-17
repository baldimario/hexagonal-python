"""
Module for handling simple command bus operations.
"""

from typing import Dict, Type, Union
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.query.query import QueryInterface, QueryResponseInterface
from core.cqrs.bus import BusInterface
from core.cqrs.handler import HandlerType
from core.cqrs.exceptions import QueryAlreadyRegistered


class SimpleQueryBus(BusInterface):
    """
    A simple implementation of the Query Bus pattern.

    Attributes:
        _handlers (Dict[Type[QueryInterface], QueryInterface]):
        A dictionary of query handlers.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[QueryInterface], HandlerType] = {}

    def register_handler(self, cq: Type[QueryInterface], handler: HandlerType) -> None:
        """
        Registers a query handler for a specific query type.

        Args:
            cq (Type[QueryInterface]): The query type to register the handler for.
            handler (HandlerType): The handler function to register.

        Raises:
            QueryAlreadyRegistered: If a handler is already registered for the query type.
        """
        if cq in self._handlers:
            raise QueryAlreadyRegistered.for_query(cq.__name__)

        self._handlers[cq] = handler

    def execute(self, cq: QueryInterface) -> Union[None, QueryResponseInterface]:
        """
        Execute a query and return the response.

        Args:
            cq (QueryInterface): The query to execute.

        Returns:
            Union[None, QueryResponseInterface]: The query response, or None if not applicable.

        Raises:
            HandlerNotFound: If no handler is registered for the query type.
        """
        if type(cq) not in self._handlers:
            raise HandlerNotFound.for_query(cq)

        handler = self._handlers[type(cq)]
        return handler(cq)
