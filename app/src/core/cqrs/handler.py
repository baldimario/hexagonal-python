"""Module containing base interfaces for handlers."""

from typing import Union, Generic, TypeVar, Callable, Any

T = TypeVar("T")  # pylint: disable=invalid-name
R = TypeVar("R")  # pylint: disable=invalid-name


class HandlerInterface(Generic[T, R]):  # pylint: disable=too-few-public-methods
    """Base interface for query handlers."""

    # it should be async
    def __call__(self, cq: T) -> Union[None, R]:
        """Handles a query."""


HandlerType = Union[Callable[[Any], None], HandlerInterface[T, Union[None, R]]]
