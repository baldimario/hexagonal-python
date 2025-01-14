"""
Module for handling example queries.
"""

from core.di import inject
from core.cqrs.handler import HandlerInterface
from example.domain.query.example_query import ExampleQuery
from example.domain.query.example_response import ExampleResponse


@inject
class ExampleQueryHandler(HandlerInterface):  # pylint: disable=too-few-public-methods
    """
    Handles ExampleQuery instances.
    """

    def __init__(self, foo):  # pylint: disable=disallowed-name
        self.foo = foo  # pylint: disable=disallowed-name

    def __call__(self, command: ExampleQuery):
        return ExampleResponse(
            result=" ".join([command.parameter_one, command.parameter_two, self.foo])
        )
