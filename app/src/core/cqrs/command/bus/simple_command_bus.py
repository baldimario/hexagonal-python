"""
Module for handling simple command bus operations.
"""

from typing import Dict, Type
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.bus import BusInterface
from core.cqrs.handler import HandlerType
from core.cqrs.exceptions import CommandAlreadyRegistered


class SimpleCommandBus(BusInterface):
    """
    A simple implementation of the Command Bus pattern.

    Attributes:
        _handlers (Dict[Type[BaseCommandInterface], BaseCommandInterface]):
        A dictionary of command handlers.
    """

    def __init__(self) -> None:
        self._handlers: Dict[Type[BaseCommandInterface], HandlerType] = {}

    def register_handler(
        self, cq: Type[BaseCommandInterface], handler: HandlerType
    ) -> None:
        """
        Registers a command handler for a specific command type.

        Args:
            cq (Type[BaseCommandInterface]): The command type to register a handler for.
            handler (CommandHandlerType): The handler function to register.
        """
        if cq in self._handlers:
            raise CommandAlreadyRegistered.for_command(cq.__name__)

        self._handlers[cq] = handler

    def execute(self, cq: BaseCommandInterface) -> None:
        """
        Execute a command by invoking its registered handler.

        Args:
            cq (BaseCommandInterface): The command to execute.

        Raises:
            HandlerNotFound: If no handler is registered for the command.
        """
        if type(cq) not in self._handlers:
            raise HandlerNotFound.for_command(cq)

        handler = self._handlers[type(cq)]
        handler(cq)
