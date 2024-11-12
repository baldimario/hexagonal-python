"""
Module for handling bus operations.
"""

from abc import ABC, abstractmethod
from typing import Type, Union, TypeVar, Generic

T = TypeVar("T")  # pylint: disable=invalid-name
H = TypeVar("H")  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class BusInterface(Generic[T, H, R], ABC):
    """
    Abstract base class for buses.

    Provides a register_handler method for registering handlers.
    """

    @abstractmethod
    def register_handler(self, cq: Type[T], handler: H) -> None:
        """
        Registers a handler for a specific query.

        Args:
            cs: The type of cs to register the handler for.
            handler: The handler to register for the query.
        """

    @abstractmethod
    def execute(self, cq: T) -> Union[None, R]:
        """
        Execute a T.

        :param cq: The query to execute.
        """
