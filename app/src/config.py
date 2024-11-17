"""
This file is used to setup the container with the necessary dependencies.
"""

import os
import logging
from typing import Union
from core.di import di, Container

# from core.cqrs.command.bus.di_command_bus import DICommandBus
# from core.cqrs.query.bus.rabbitmq_query_bus import RabbitMQQueryBus
from core.cqrs.command.bus.kafka_command_bus import KafkaCommandBus
from core.cqrs.query.bus.kafka_query_bus import KafkaQueryBus

# from core.broker.rabbitmq import RabbitMQBroker
from core.broker.kafka import KafkaBroker
from example.infrastructure.cli.main import Main
from example.domain.query.example_query import ExampleQuery
from example.domain.query.example_handler import ExampleQueryHandler
from example.domain.command.example_command import ExampleCommand
from example.domain.command.example_handler import ExampleCommandHandler


async def container_setup(
    container: Union[Container, None], consumer_group: str = "python-hexagonal"
) -> None:
    """
    This function is used to setup the container with the necessary dependencies.
    """

    logging.getLogger().setLevel(os.getenv("LOG_LEVEL", "INFO"))

    if container is None:
        container = di

    container["foo"] = "bar"
    container["baz"] = "qux"

    # container["rabbitmq_broker"] = RabbitMQBroker("rabbitmq", 5672, "root", "root")
    container["kafka_broker"] = KafkaBroker(["kafka:9092"], consumer_group, "latest")

    # query_bus = DIQueryBus(container)
    query_bus = KafkaQueryBus(container["kafka_broker"])
    await query_bus.register_handler(
        ExampleQuery,
        ExampleQueryHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    command_bus = KafkaCommandBus(container["kafka_broker"])
    await command_bus.register_handler(
        ExampleCommand,
        ExampleCommandHandler(),  # pylint: disable=no-value-for-parameter # pyright: ignore
    )

    di["query_bus"] = query_bus
    di["command_bus"] = command_bus

    di["example.infrastructure.cli.main"] = (
        Main()  # pylint: disable=no-value-for-parameter # pyright: ignore
    )
