"""
Module for handling example queries.
"""

from core.di import inject
from core.cqrs.query_handler import QueryHandlerInterface
from example.domain.query.example_query import ExampleQuery
from example.domain.query.example_response import ExampleResponse


@inject
class ExampleQueryHandler(  # pylint: disable=too-few-public-methods
    QueryHandlerInterface
):
    """
    Handles ExampleQuery instances.
    """

    def __init__(self, foo):  # pylint: disable=disallowed-name
        self.foo = foo  # pylint: disable=disallowed-name

    def __call__(self, command: ExampleQuery):
        return ExampleResponse(
            result=" ".join([command.parameter_one, command.parameter_two, self.foo])
        )
