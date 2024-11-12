"""
Module containing types for CQRS (Command Query Responsibility Segregation) pattern.
"""

from typing import Any, Callable, Union

from .command import BaseCommandInterface, CommandResponseInterface
from .query import QueryInterface, QueryResponseInterface
from .command_handler import CommandHandlerInterface
from .query_handler import QueryHandlerInterface

CommandHandlerType = Union[
    Callable[[Any], None],
    CommandHandlerInterface[BaseCommandInterface, CommandResponseInterface],
]

QueryHandlerType = Union[
    Callable[[Any], None], QueryHandlerInterface[QueryInterface, QueryResponseInterface]
]
