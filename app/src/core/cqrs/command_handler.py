"""Module containing base interfaces for command handlers."""

from typing import Union, TypeVar
from .handler import HandlerInterface
from .command import BaseCommandInterface, CommandResponseInterface

T = TypeVar("T", bound=BaseCommandInterface)  # pylint: disable=invalid-name
R = TypeVar("R", bound=CommandResponseInterface)  # pylint: disable=invalid-name


class CommandHandlerInterface(
    HandlerInterface[T, R]
):  # pylint: disable=too-few-public-methods
    """Base interface for command handlers."""

    # it should be async
    def __call__(self, command: T) -> Union[None, R]:
        """Handles a command."""
        raise NotImplementedError
