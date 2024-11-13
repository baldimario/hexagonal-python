"""
Module for handling command bus operations.
"""

from abc import ABC, abstractmethod
from typing import Type, TypeVar

from core.cqrs.bus import BusInterface
from .command import BaseCommandInterface
from .command_handler import CommandHandlerInterface

T = TypeVar("T", bound=BaseCommandInterface)  # pylint: disable=invalid-name
H = TypeVar("H", bound=CommandHandlerInterface)  # pylint: disable=invalid-name


class CommandBusInterface(BusInterface[T, H, None], ABC):
    """
    Abstract base class for command buses.

    Provides a register_handler method for registering command handlers.
    """

    @abstractmethod
    def register_handler(  # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:  # pylint: disable=arguments-renamed # pyright: ignore
        """
        Registers a handler for a specific command.

        Args:
            command: The type of command to register the handler for.
            handler: The handler to register for the command.
        """

    @abstractmethod
    def execute(  # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed # pyright: ignore
    ) -> None:
        """
        Execute a command.

        :param command: The command to execute.
        """
