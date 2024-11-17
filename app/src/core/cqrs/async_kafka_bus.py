"""
Module for asynchronous command bus implementation.
"""

import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Union, List
from core.cqrs.bus import BusInterface
from core.broker.kafka import KafkaBroker
from core.cqrs.async_protocol import AsyncProtocol
from core.cqrs.exceptions import HandlerNotFound

T = TypeVar("T")  # pylint: disable=invalid-name
H = TypeVar("H")  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class KafkaBusInterface(BusInterface[T, H, R], ABC):
    """
    Abstract base class for asynchronous event buses.

    Provides a register_handler method for registering event handlers.
    """

    def __init__(self, broker: KafkaBroker):
        """
        Initializes the event bus with a broker.
        """
        self.broker = broker
        self.handlers = {}

    @abstractmethod
    async def register_handler(  # pylint: disable=invalid-overridden-method # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:  # pylint: disable=arguments-renamed # pyright: ignore
        """
        Registers a handler for a specific event.
        """

    @abstractmethod
    async def execute(  # pylint: disable=invalid-overridden-method # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed # pyright: ignore
    ) -> Union[str, None]:
        """
        Execute a event asynchronously.
        """

    @abstractmethod
    async def listen(self) -> None:
        """
        Listens for incoming events.
        """

    async def _listen(self, send_response: bool = False) -> None:
        """
        Listens for incoming events from kafka and executes their handlers asynchronously
        """
        queue_names: List[str] = list(self.handlers.keys())

        await self.broker.connect(queue_names)

        if self.broker.connection is None:
            raise BrokenPipeError("Kafka not connected")

        producer = self.broker.connection["producer"]
        consumer = self.broker.connection["consumer"]

        # Start consuming messages from each queue
        # logging.debug('Listening to %s', queue_names)
        # consumer.subscribe(queue_names)

        try:
            for event in consumer:
                queue_name = event.topic
                message = event.value

                logging.debug("Event %s %s", queue_name, message.decode())
                if queue_name not in self.handlers:
                    raise HandlerNotFound.for_command(queue_name)

                ap = AsyncProtocol.from_json(message)
                cq = ap.to_cq()

                handler = self.handlers[queue_name]
                result = handler(cq)

                logging.debug("Send Response? %s", "yes" if send_response else "no")
                if send_response:
                    response_ap = AsyncProtocol.from_cq(result, uuid=ap.uuid)
                    response_fqdn = ap.cq + "-Response"
                    data = response_ap.to_json()

                    logging.debug("Sending response back to %s %s", response_fqdn, data)
                    await self.broker.send(response_fqdn, data)
                    producer.flush()
                else:
                    if result is not None:
                        return await result

        except asyncio.CancelledError:
            # Gracefully handle generator closure
            await self.broker.connection["producer"].close()
            await self.broker.connection["consumer"].close()
            raise
