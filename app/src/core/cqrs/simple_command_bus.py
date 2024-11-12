"""
Module for handling simple command bus operations.
"""

from typing import Dict, Type

from .command import BaseCommandInterface
from .command_bus import CommandBusInterface
from .types import CommandHandlerType
from .exceptions import CommandAlreadyRegistered, HandlerNotFound


class SimpleCommandBus(CommandBusInterface):
    """
    A simple implementation of the Command Bus pattern.

    Attributes:
        _handlers (Dict[Type[BaseCommandInterface], BaseCommandInterface]):
        A dictionary of command handlers.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[BaseCommandInterface], CommandHandlerType] = {}

    def register_handler(
        self, cq: Type[BaseCommandInterface], handler: CommandHandlerType
    ) -> None:
        if cq in self._handlers:
            raise CommandAlreadyRegistered.for_command(cq.__name__)

        self._handlers[cq] = handler

    def execute(self, cq: BaseCommandInterface) -> None:
        if type(cq) not in self._handlers:
            raise HandlerNotFound.for_command(cq)

        handler = self._handlers[type(cq)]
        handler(cq)
