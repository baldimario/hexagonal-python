"""
Module for asynchronous query bus implementation using RabbitMQ.
"""

from abc import ABC
from typing import Type, TypeVar
import asyncio
from aioamqp.exceptions import EmptyQueue  # pyright: ignore
from core.cqrs.async_rabbitmq_bus import RabbitMQBusInterface
from core.cqrs.query.query import QueryInterface, QueryResponseInterface
from core.cqrs.handler import HandlerInterface
from core.cqrs.exceptions import HandlerNotFound
from core.broker.rabbitmq import RabbitMQBroker
from core.cqrs.async_protocol import AsyncProtocol

T = TypeVar("T", bound=QueryInterface)  # pylint: disable=invalid-name
H = TypeVar("H", bound=HandlerInterface)  # pylint: disable=invalid-name


class RabbitMQQueryBus(RabbitMQBusInterface[T, H, None], ABC):
    """
    Asynchronous query bus that uses RabbitMQ as the broker interface.
    """

    def __init__(self, broker: RabbitMQBroker):
        """
        Initializes the RabbitMQ query bus.

        Args:
            broker: The RabbitMQ broker instance.
        """
        self.broker = broker
        self.handlers = {}
        super().__init__(self.broker)

    async def register_handler(  # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:  # pylint: disable=arguments-renamed # pyright: ignore
        """
        Registers a handler for a specific query.

        Args:
            query: The type of query to register the handler for.
            handler: The handler to register for the query.
        """
        fqdn = ".".join([cq.__module__, cq.__name__])
        self.handlers[fqdn] = handler

    async def execute(  # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed # pyright: ignore
    ) -> QueryResponseInterface:
        """
        Execute a query asynchronously.

        :param query: The query to execute.
        """
        fqdn = ".".join([cq.__module__, cq.__class__.__name__])
        if fqdn not in self.handlers:
            raise HandlerNotFound.for_query(cq)

        ap = AsyncProtocol.from_cq(cq)
        await self.broker.send(fqdn, ap.to_json())

        response_fqdn = fqdn + "#Response"
        return await self.get_response(response_fqdn, ap.uuid)

    async def get_response(self, response_fqdn, uuid) -> QueryResponseInterface:
        """
        Retrieves a response for a given query.

        Args:
            response_fqdn (str): The fully qualified domain name of the response.
            uuid (str): The unique identifier of the query.

        Returns:
            Any: The response to the query.
        """
        await self.broker.connect()

        if self.broker.connection is None:
            raise BrokenPipeError("RabbitMQ not connected")

        channel = await self.broker.connection["protocol"].channel()
        await channel.queue_declare(queue_name=response_fqdn, durable=True)

        while True:
            try:
                message = await channel.basic_get(response_fqdn)
                if message is None:
                    # If the queue is empty, wait for a short period and try again
                    await asyncio.sleep(0.1)
                    continue
            except EmptyQueue as _:
                await asyncio.sleep(0.1)
                continue

            body = message["message"].decode()
            ap = AsyncProtocol.from_json(body)

            if ap.uuid == uuid:
                # If the message has the correct UUID, return the response
                await channel.basic_client_ack(message["delivery_tag"])
                response = ap.to_cq()

                return response  # pyright: ignore

            # If the message has a different UUID, reject it and continue waiting
            # await channel.basic_reject(message[0].delivery_tag, requeue=True)

    async def listen(self) -> None:
        """
        Listens for incoming queries from rabbitmq and executes them asynchronously.
        """
        await self._listen(True)
