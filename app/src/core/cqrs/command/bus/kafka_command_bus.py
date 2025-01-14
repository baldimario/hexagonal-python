"""
Module for asynchronous command bus implementation using Kafka.
"""

from abc import ABC
from typing import Type, TypeVar, Union
from core.cqrs.async_kafka_bus import KafkaBusInterface
from core.cqrs.command.command import BaseCommandInterface
from core.cqrs.handler import HandlerInterface
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.async_protocol import AsyncProtocol

T = TypeVar("T", bound=BaseCommandInterface)  # pylint: disable=invalid-name
H = TypeVar("H", bound=HandlerInterface)  # pylint: disable=invalid-name


class KafkaCommandBus(KafkaBusInterface[T, H, None], ABC):
    """
    Asynchronous command bus that uses Kafka as the broker interface.
    """

    async def execute(  # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed # pyright: ignore
    ) -> Union[str, None]:
        """
        Execute a command asynchronously.

        :param command: The command to execute.
        """
        fqdn = ".".join([cq.__module__, cq.__class__.__name__])
        if fqdn not in self.handlers:
            raise HandlerNotFound.for_command(cq)

        ap = AsyncProtocol.from_cq(cq)
        await self.broker.send(fqdn, ap.to_json())
        return ap.uuid

    async def register_handler(  # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:  # pylint: disable=arguments-renamed # pyright: ignore
        """
        Registers a handler for a specific command.

        Args:
            command: The type of command to register the handler for.
            handler: The handler to register for the command.
        """
        fqdn = ".".join([cq.__module__, cq.__name__])
        self.handlers[fqdn] = handler

    async def listen(self) -> None:
        """
        Listens for incoming queries from kafka and executes them asynchronously.
        """
        await self._listen(False)
