"""
Module for handling example commands.
"""

import logging
from core.di import inject
from core.cqrs.handler import HandlerInterface
from example.domain.command.example_command import ExampleCommand


@inject
class ExampleCommandHandler(HandlerInterface):
    """
    Handles ExampleCommand instances.
    """

    def __init__(self, foo):  # pylint: disable=disallowed-name
        self.foo = foo  # pylint: disable=disallowed-name

    def __call__(self, command: ExampleCommand):
        logging.info("Handler %s", command.parameter_one)
        logging.info("Handler %s", command.parameter_two)
        logging.info("Handler %s", self.foo)
