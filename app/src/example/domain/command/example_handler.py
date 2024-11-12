"""
Module for handling example commands.
"""

from core.di import inject
from core.cqrs.command_handler import CommandHandlerInterface
from example.domain.command.example_command import ExampleCommand


@inject
class ExampleCommandHandler(CommandHandlerInterface):
    """
    Handles ExampleCommand instances.
    """

    def __init__(self, foo):  # pylint: disable=disallowed-name
        self.foo = foo  # pylint: disable=disallowed-name

    def __call__(self, command: ExampleCommand):
        print("Handler", command.parameter_one)
        print("Handler", command.parameter_two)
        print("Handler", self.foo)
