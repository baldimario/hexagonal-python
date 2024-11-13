"""
Module for handling simple command bus operations.
"""

from typing import Dict, Type
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.command.command_bus import CommandBusInterface
from core.cqrs.command.types import CommandHandlerType
from core.cqrs.exceptions import CommandAlreadyRegistered


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
