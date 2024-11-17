"""
Module for asynchronous command bus implementation.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Type, TypeVar, Union, List
from core.cqrs.bus import BusInterface
from core.broker.broker import BrokerInterface
from core.cqrs.async_protocol import AsyncProtocol
from core.cqrs.exceptions import HandlerNotFound

T = TypeVar("T")  # pylint: disable=invalid-name
H = TypeVar("H")  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class RabbitMQBusInterface(BusInterface[T, H, R], ABC):
    """
    Abstract base class for asynchronous event buses.

    Provides a register_handler method for registering event handlers.
    """

    def __init__(self, broker: BrokerInterface):
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
        Listens for incoming events from rabbitmq and executes their handlers asynchronously
        """
        queue_names: List[str] = list(self.handlers.keys())

        await self.broker.connect()

        if self.broker.connection is None:
            raise BrokenPipeError("RabbitMQ not connected")

        channel = await self.broker.connection["protocol"].channel()

        # Create a queue to hold messages for the generator
        message_queue = asyncio.Queue()

        async def callback(
            channel, body, envelope, properties
        ):  # pylint: disable=unused-argument; pyright: ignore
            """Callback to handle incoming messages."""
            queue_name = envelope.routing_key
            message = body.decode()
            await channel.basic_client_ack(envelope.delivery_tag)
            await message_queue.put((queue_name, message))

        # Start consuming messages from each queue
        for queue_name in queue_names:
            await channel.queue_declare(queue_name=queue_name, durable=True)
            await channel.basic_consume(callback, queue_name)

        try:
            while True:
                # Yield messages from the queue
                (queue_name, message) = await message_queue.get()

                if queue_name not in self.handlers:
                    raise HandlerNotFound.for_command(queue_name)

                ap = AsyncProtocol.from_json(message)
                cq = ap.to_cq()

                handler = self.handlers[queue_name]
                result = handler(cq)

                if send_response:
                    response_ap = AsyncProtocol.from_cq(result, uuid=ap.uuid)
                    response_fqdn = ap.cq + "#Response"
                    await self.broker.send(response_fqdn, response_ap.to_json())
                else:
                    if result is not None:
                        return await result

        except asyncio.CancelledError:
            # Gracefully handle generator closure
            await self.broker.connection["protocol"].close()
            self.broker.connection["transport"].close()
            raise
