"""
Kafka broker implementation module.
"""

import logging
from typing import List, Union
from kafka import KafkaConsumer, KafkaProducer  # pyright: ignore
from core.broker.broker import BrokerInterface


class KafkaBroker(BrokerInterface):
    """
    Kafka broker implementation.
    """

    def __init__(
        self, servers: List[str], consumer_group: str, offset: str = "earliest"
    ):
        """
        Initializes the Kafka broker.

        Args:
            host: The host to connect to.
            port: The port to connect to.
            queue: The queue to use.
        """
        self.servers = servers
        self.connection = None
        self.consumer_group = consumer_group
        self.offset = offset

    async def connect(self, topics: Union[List[str], None] = None) -> None:
        """
        Establishes a connection to the Kafka broker.
        """

        subscriptions = []
        if topics is not None:
            for topic in topics:
                if topic is not None:
                    subscriptions.append(topic)

        logging.debug("Listening to %s", subscriptions)
        # Note: Kafka does not require a login or password for connection
        self.connection = {
            "producer": KafkaProducer(  # pyright: ignore
                bootstrap_servers=self.servers
            ),
            "consumer": KafkaConsumer(  # pyright: ignore
                ",".join(subscriptions),
                bootstrap_servers=self.servers,
                group_id=self.consumer_group,
                auto_offset_reset=self.offset,
            ),
        }

    async def send(self, cq: str, message: str) -> None:
        """
        Sends a message to the Kafka broker.

        Args:
            message: The message to send.
        """
        if not self.connection:
            await self.connect()

        producer = self.connection["producer"]
        logging.debug("Sending msg %s %s", cq, message)
        return producer.send(cq, value=message.encode())

    async def receive(self, cq: str) -> str:
        """
        Receives a message from the Kafka broker.

        Returns:
            The received message.
        """
        if not self.connection:
            await self.connect()

        consumer = self.connection["consumer"]
        consumer.subscribe(cq)
        message = consumer.recv()
        return message.value.decode()
