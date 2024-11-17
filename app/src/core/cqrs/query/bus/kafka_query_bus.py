"""
Module for asynchronous query bus implementation using Kafka.
"""

import logging
from abc import ABC
from typing import Type, TypeVar
import asyncio
from core.cqrs.async_kafka_bus import KafkaBusInterface
from core.cqrs.query.query import QueryInterface, QueryResponseInterface
from core.cqrs.handler import HandlerInterface
from core.cqrs.exceptions import HandlerNotFound
from core.cqrs.async_protocol import AsyncProtocol

T = TypeVar("T", bound=QueryInterface)  # pylint: disable=invalid-name
H = TypeVar("H", bound=HandlerInterface)  # pylint: disable=invalid-name


class KafkaQueryBus(KafkaBusInterface[T, H, None], ABC):
    """
    Asynchronous query bus that uses Kafka as the broker interface.
    """

    async def register_handler(  # pyright: ignore
        self,
        cq: Type[T],  # pylint: disable=arguments-renamed
        handler: H,  # pyright: ignore
    ) -> None:  # pylint: disable=arguments-renamed # pyright: ignore
        """
        Registers a handler for a specific query.
        """
        fqdn = ".".join([cq.__module__, cq.__name__])
        self.handlers[fqdn] = handler

    async def execute(  # pyright: ignore
        self, cq: T  # pylint: disable=arguments-renamed # pyright: ignore
    ) -> QueryResponseInterface:
        """
        Execute a query asynchronously.
        """
        await self.broker.connect(list(self.handlers.keys()))

        fqdn = ".".join([cq.__module__, cq.__class__.__name__])
        if fqdn not in self.handlers:
            raise HandlerNotFound.for_query(cq)

        ap = AsyncProtocol.from_cq(cq)
        await self.broker.send(fqdn, ap.to_json())

        response_fqdn = fqdn + "-Response"
        return await self.get_response(response_fqdn, ap.uuid)

    async def get_response(
        self, response_fqdn, uuid
    ) -> QueryResponseInterface:  # pyright: ignore
        """
        Retrieves a response for a given query.

        Args:
            response_fqdn (str): The fully qualified domain name of the response.
            uuid (str): The unique identifier of the query.

        Returns:
            Any: The response to the query.
        """
        # await self.broker.connect()
        consumer = self.broker.connection["consumer"]

        logging.debug("Subscribing to %s", response_fqdn)
        consumer.subscribe(response_fqdn)

        if self.broker.connection is None:
            raise BrokenPipeError("Kafka not connected")

        logging.debug("Listening to response from %s", response_fqdn)
        for event in consumer:
            try:
                logging.debug(
                    "Event from %s waiting for %s", event.topic, response_fqdn
                )
                if event.topic == response_fqdn:
                    message = event.value.decode()
                    if message is None:
                        # If the queue is empty, wait for a short period and try again
                        # deckde and check uuid
                        await asyncio.sleep(0.1)
                        continue
            except asyncio.CancelledError:
                # Gracefully handle generator closure
                await self.broker.connection["producer"].close()
                await self.broker.connection["consumer"].close()
                raise

            body = event.value.decode()
            ap = AsyncProtocol.from_json(body)

            if ap.uuid == uuid:
                # If the message has the correct UUID, return the response
                consumer.commit()
                response = ap.to_cq()

                return response  # pyright: ignore

            # If the message has a different UUID, reject it and continue waiting
            # await consumer.reject(message, requeue=True)

    async def listen(self) -> None:
        """
        Listens for incoming queries from kafka and executes them asynchronously.
        """

        await self._listen(True)
