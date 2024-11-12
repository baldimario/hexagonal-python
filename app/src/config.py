"""
This file is used to setup the container with the necessary dependencies.
"""

from typing import Union
from core.di import di, Container
from core.cqrs.di_command_bus import DICommandBus
from core.cqrs.di_query_bus import DIQueryBus
from example.infrastructure.cli.main import Main
from example.domain.query.example_query import ExampleQuery
from example.domain.query.example_handler import ExampleQueryHandler
from example.domain.command.example_command import ExampleCommand
from example.domain.command.example_handler import ExampleCommandHandler


def container_setup(container: Union[Container, None]) -> None:
    """
    This function is used to setup the container with the necessary dependencies.
    """
    if container is None:
        container = di

    container["foo"] = "bar"
    container["baz"] = "qux"

    query_bus = DIQueryBus(container)
    query_bus.register_handler(
        ExampleQuery,
        ExampleQueryHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    command_bus = DICommandBus(container)
    command_bus.register_handler(
        ExampleCommand,
        ExampleCommandHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    di["query_bus"] = query_bus
    di["command_bus"] = command_bus

    di["example.infrastructure.cli.main"] = (
        Main()  # pylint: disable=no-value-for-parameter # pyright: ignore
    )
