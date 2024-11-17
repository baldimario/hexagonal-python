"""
Module for Dependency Injection Command Bus.
"""

from typing import Type
from core.di import Container
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.bus import BusInterface
from core.cqrs.handler import HandlerType, HandlerInterface
from core.cqrs.exceptions import CommandAlreadyRegistered


class DICommandBus(BusInterface):
    """
    A command bus implementation that utilizes a dependency injection container.
    """

    def __init__(self, container: Container) -> None:
        self._container = container

    def register_handler(
        self, cq: Type[BaseCommandInterface], handler: HandlerType
    ) -> None:
        """
        Registers a command handler for a given command type.

        Args:
            cq: The type of command to register the handler for.
            handler: The handler function to register.

        Raises:
            ValueError: If the handler is not a subclass of HandlerInterface.
            CommandAlreadyRegistered: If a handler is already registered for the command.
        """
        if not issubclass(handler.__class__, HandlerInterface):
            raise ValueError("Handler must be a subclass of Handler[TCommand]")

        if cq in self._container:
            raise CommandAlreadyRegistered.for_command(cq.__name__)

        self._container[cq] = handler

    def execute(self, cq: BaseCommandInterface) -> None:
        """
        Executes a command by invoking its registered handler.

        Args:
            cq: The command to execute.

        Raises:
            HandlerNotFound: If no handler is registered for the command.
        """
        if type(cq) not in self._container:
            raise HandlerNotFound.for_command(cq)

        handler = self._container[type(cq)]
        handler(cq)  # pyright: ignore
