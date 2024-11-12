"""
Module for example command.
"""

from dataclasses import dataclass
from core.cqrs.command import CommandInterface


@dataclass(frozen=True, kw_only=True)
class ExampleCommand(CommandInterface):
    """
    Represents an example command with two parameters.

    Attributes:
        parameter_one (str): The first parameter of the command.
        parameter_two (str): The second parameter of the command.
    """

    parameter_one: str
    parameter_two: str
