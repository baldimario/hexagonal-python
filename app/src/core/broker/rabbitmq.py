"""
RabbitMQ broker implementation module.
"""

import aioamqp  # pyright: ignore
from core.broker.broker import BrokerInterface


class RabbitMQBroker(BrokerInterface):
    """
    RabbitMQ broker implementation.
    """

    def __init__(self, host: str, port: int, login: str, password: str):
        """
        Initializes the RabbitMQ broker.

        Args:
            host: The host to connect to.
            port: The port to connect to.
            queue: The queue to use.
        """
        self.host = host
        self.port = port
        self.login = login
        self.password = password
        self.connection = None

    async def connect(self) -> None:
        """
        Establishes a connection to the RabbitMQ broker.
        """
        transport, protocol = await aioamqp.connect(
            self.host, self.port, self.login, self.password
        )
        self.connection = {"transport": transport, "protocol": protocol}

    async def send(self, cq: str, message: str) -> None:
        """
        Sends a message to the RabbitMQ broker.

        Args:
            message: The message to send.
        """
        if not self.connection:
            await self.connect()

        channel = await self.connection["protocol"].channel()  # pyright: ignore
        await channel.queue_declare(cq, durable=True)
        await channel.publish(message, "", cq)

    async def receive(self, cq: str) -> str:
        """
        Receives a message from the RabbitMQ broker.

        Returns:
            The received message.
        """
        if not self.connection:
            await self.connect()

        channel = await self.connection["protocol"].channel()  # pyright: ignore
        await channel.queue_declare(cq)
        message = await channel.basic_get(cq)
        return message.body.decode()
