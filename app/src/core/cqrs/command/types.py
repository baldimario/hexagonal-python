"""
Module containing types for CQRS (Command Query Responsibility Segregation) pattern.
"""

from typing import Any, Callable, Union

from .command import BaseCommandInterface, CommandResponseInterface
from .command_handler import CommandHandlerInterface

CommandHandlerType = Union[
    Callable[[Any], None],
    CommandHandlerInterface[BaseCommandInterface, CommandResponseInterface],
]
