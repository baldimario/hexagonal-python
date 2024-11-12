"""
Module for Dependency Injection Command Bus.
"""

from typing import Type
from core.di import Container
from .command import BaseCommandInterface
from .command_bus import CommandBusInterface
from .types import CommandHandlerType
from .command_handler import CommandHandlerInterface
from .exceptions import CommandAlreadyRegistered, HandlerNotFound


class DICommandBus(CommandBusInterface):
    """
    A command bus implementation that utilizes a dependency injection container.
    """

    def __init__(self, container: Container) -> None:
        self._container = container

    def register_handler(
        self, cq: Type[BaseCommandInterface], handler: CommandHandlerType
    ) -> None:
        if not issubclass(handler.__class__, CommandHandlerInterface):
            raise ValueError("Handler must be a subclass of Handler[TCommand]")

        if cq in self._container:
            raise CommandAlreadyRegistered.for_command(cq.__name__)

        self._container[cq] = handler

    def execute(self, cq: BaseCommandInterface) -> None:
        if type(cq) not in self._container:
            raise HandlerNotFound.for_command(cq)

        handler = self._container[type(cq)]
        handler(cq)  # pyright: ignore
