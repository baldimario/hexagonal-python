"""
This file is used to setup the container with the necessary dependencies.
"""

from typing import Union
from core.di import di, Container

# from core.cqrs.command.bus.di_command_bus import DICommandBus
from core.cqrs.command.bus.rabbitmq_command_bus import RabbitMQCommandBus
from core.cqrs.query.bus.rabbitmq_query_bus import RabbitMQQueryBus
from core.broker.rabbitmq import RabbitMQBroker
from example.infrastructure.cli.main import Main
from example.domain.query.example_query import ExampleQuery
from example.domain.query.example_handler import ExampleQueryHandler
from example.domain.command.example_command import ExampleCommand
from example.domain.command.example_handler import ExampleCommandHandler


async def container_setup(container: Union[Container, None]) -> None:
    """
    This function is used to setup the container with the necessary dependencies.
    """
    if container is None:
        container = di

    container["foo"] = "bar"
    container["baz"] = "qux"

    container["broker"] = RabbitMQBroker("rabbitmq", 5672, "root", "root")

    # query_bus = DIQueryBus(container)
    query_bus = RabbitMQQueryBus(container["broker"])
    await query_bus.register_handler(
        ExampleQuery,
        ExampleQueryHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    command_bus = RabbitMQCommandBus(container["broker"])
    await command_bus.register_handler(
        ExampleCommand,
        ExampleCommandHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    di["query_bus"] = query_bus
    di["command_bus"] = command_bus

    di["example.infrastructure.cli.main"] = (
        Main()  # pylint: disable=no-value-for-parameter # pyright: ignore
    )
