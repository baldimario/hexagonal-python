"""
Domain module for the application.
"""

from core.di import inject
from core.cqrs.command_bus import CommandBusInterface
from core.cqrs.query_bus import QueryBusInterface
from example.domain.command.example_command import ExampleCommand
from example.domain.query.example_query import ExampleQuery


@inject
class Main:  # pylint: disable=too-few-public-methods
    """
    Main class.
    """

    def __init__(
        self,
        command_bus: CommandBusInterface,
        query_bus: QueryBusInterface,
        foo: str,  # pylint: disable=disallowed-name
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.foo = foo  # pylint: disable=disallowed-name

    def run(self):
        """Run method."""
        print("Main CLI (di)", self.foo)

        result = self.query_bus.execute(
            ExampleQuery(parameter_one="buz", parameter_two="bax")
        )

        print("Main CLI (qb)", result)

        parameter = result.result if result is not None else "two"

        self.command_bus.execute(
            ExampleCommand(parameter_one="one", parameter_two=parameter)
        )
