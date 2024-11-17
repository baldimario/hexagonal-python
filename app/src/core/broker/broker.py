"""
Module for defining the Broker interface.
"""

from typing import Any
from abc import ABC, abstractmethod


class BrokerInterface(ABC):
    """
    Abstract base class for messaging brokers.
    """

    connection: Any

    @abstractmethod
    async def connect(self) -> None:
        """Establishes a connection to the broker."""

    @abstractmethod
    async def send(self, cq: str, message: str) -> None:
        """
        Sends a message to the broker.

        Args:
            message: The message to send.
        """

    @abstractmethod
    async def receive(self, cq: str) -> str:
        """
        Receives a message from the broker.

        Returns:
            The received message.
        """
